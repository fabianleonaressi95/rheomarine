#!/usr/bin/env python3
"""Run the M0 Lagrangian pilot on acquired HFR NetCDF subsets.

For each site file this script:
  1. loads the ERDDAP .nc subset via ``rheomarine_hfr.load_erddap_netcdf``;
  2. converts it to QC-masked ``VelocityField`` segments (default: split at
     gaps > 3 h so no trajectory crosses unobserved intervals);
  3. releases a deterministic particle grid inside cells that are QC-valid
     at segment start;
  4. runs ``simulate_m0`` per segment and writes a JSON summary plus a
     compressed .npz of final positions under ``results/hfr_pilot/``.

This is a numerical pilot on surface currents. It is NOT a validation
against observations and says nothing about vertical transport or
seabed deposition.

Usage (from repo root):
    PYTHONPATH=src python scripts/run_hfr_m0_pilot.py \
        --inputs 'data/hfr/raw/*_7d.nc' --out results/hfr_pilot
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from rheomarine_hfr import (crop_field, hfr_valid_mask, load_erddap_netcdf,
                           to_velocity_fields)
from rheomarine_transport import simulate_m0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def release_positions(field, n_side: int = 8):
    """Deterministic particle grid kept only where the t0 stencil is valid."""
    x = np.linspace(field.x[0] + 0.06 * (field.x[-1] - field.x[0]),
                    field.x[-1] - 0.06 * (field.x[-1] - field.x[0]), n_side)
    y = np.linspace(field.y[0] + 0.06 * (field.y[-1] - field.y[0]),
                    field.y[-1] - 0.06 * (field.y[-1] - field.y[0]), n_side)
    pts = np.array([(a, b) for a in x for b in y])
    keep = []
    for px, py in pts:
        ix1 = int(np.clip(np.searchsorted(field.x, px, "right"), 1, len(field.x) - 1))
        iy1 = int(np.clip(np.searchsorted(field.y, py, "right"), 1, len(field.y) - 1))
        ix0, iy0 = ix1 - 1, iy1 - 1
        if field.valid is None or np.all(field.valid[0, iy0:iy1 + 1, ix0:ix1 + 1]):
            keep.append((px, py))
    return np.array(keep)


def _stencil_valid(field, positions, it):
    """True where the bilinear stencil at time index ``it`` is all-valid."""
    ix1 = np.clip(np.searchsorted(field.x, positions[:, 0], "right"),
                  1, len(field.x) - 1)
    iy1 = np.clip(np.searchsorted(field.y, positions[:, 1], "right"),
                  1, len(field.y) - 1)
    ix0, iy0 = ix1 - 1, iy1 - 1
    ok = np.ones(len(positions), dtype=bool)
    for dx in (0, 1):
        for dy in (0, 1):
            ok &= field.valid[it, iy0 + dy, ix0 + dx]
    return ok


def simulate_qc_aware(field, pos0, *, seed: int):
    """Advance particles interval-by-interval on observed timestamps only.

    A particle is marked ``qc_stopped`` (trajectory ends at its last
    fully-observed position) as soon as its bilinear stencil touches a
    QC-invalid cell at either bracketing timestamp. Particles are never
    interpolated through missing data and never see placeholder zeros.
    Returns (final_positions, alive_mask, qc_stopped_mask).
    """
    pos = pos0.copy()
    n = len(pos)
    alive = np.ones(n, dtype=bool)
    qc_stopped = np.zeros(n, dtype=bool)
    for i in range(len(field.times) - 1):
        ids = np.flatnonzero(alive)
        if ids.size == 0:
            break
        t_i, t_j = float(field.times[i]), float(field.times[i + 1])
        ok = (_stencil_valid(field, pos[ids], i)
              & _stencil_valid(field, pos[ids], i + 1))
        stop_ids = ids[~ok]
        qc_stopped[stop_ids] = True
        alive[stop_ids] = False
        ids = ids[ok]
        if ids.size == 0:
            continue
        step = simulate_m0(field, pos[ids], start_time=t_i, end_time=t_j,
                           dt=t_j - t_i, diffusivity=0.0,
                           boundary="reflect", seed=seed)
        pos[ids] = step.final_positions
    return pos, alive, qc_stopped


def best_block(mask2d: np.ndarray, block: int) -> tuple[slice, slice, float]:
    """Locate the ``block`` x ``block`` cell window with highest mean
    temporal validity. Returns (iy_slice, ix_slice, mean_validity)."""
    cf = mask2d.mean(axis=0) if mask2d.ndim == 3 else mask2d
    ny, nx = cf.shape
    cellfrac = cf
    best = (-1.0, slice(0, 0), slice(0, 0))
    for iy in range(ny - block + 1):
        for ix in range(nx - block + 1):
            s = float(cellfrac[iy:iy + block, ix:ix + block].mean())
            if s > best[0]:
                best = (s, slice(iy, iy + block), slice(ix, ix + block))
    return best[1], best[2], best[0]


def run_file(path: Path, *, max_gap_s: float, n_side: int, block: int,
             seed: int) -> dict:
    ds = load_erddap_netcdf(str(path))
    fields = to_velocity_fields(ds, max_gap_s=max_gap_s)
    # restrict the pilot to the highest-coverage sub-region: documented,
    # reproducible, and consistent with the "smallest defensible pilot
    # polygon" requirement in the RISTANC data audit
    full_mask = hfr_valid_mask(ds.qcflag, ds.u, ds.v)
    iy, ix, block_validity = best_block(full_mask, block)
    fields = [crop_field(f, iy, ix) for f in fields]
    import re
    m = re.search(r"HFR-NAdr-([A-Z]+)_v\d+", path.name)
    site = m.group(1) if m else path.stem
    segments = []
    for i, field in enumerate(fields):
        t0, t1 = float(field.times[0]), float(field.times[-1])
        pos0 = release_positions(field, n_side=n_side)
        if len(pos0) == 0:
            segments.append({"segment": i, "start_utc": None,
                             "end_utc": None, "n_particles": 0,
                             "note": "no QC-valid release cells"})
            continue
        final_pos, alive, qc_stopped = simulate_qc_aware(field, pos0,
                                                         seed=seed)
        disp = np.linalg.norm(final_pos - pos0, axis=1)
        segments.append({
            "segment": i,
            "start_utc": datetime.fromtimestamp(t0, timezone.utc).isoformat(),
            "end_utc": datetime.fromtimestamp(t1, timezone.utc).isoformat(),
            "duration_h": round((t1 - t0) / 3600.0, 3),
            "n_timestamps": int(field.times.size),
            "n_particles": int(len(pos0)),
            "valid_fraction_t0": round(float(field.valid[0].mean()), 4),
            "alive_count": int(alive.sum()),
            "qc_stopped_count": int(qc_stopped.sum()),
            "displacement_m_median": round(float(np.median(disp)), 1),
            "displacement_m_max": round(float(disp.max()), 1),
        })
        np.savez_compressed(
            Path(__file__).resolve().parents[1] / "results" / "hfr_pilot" /
            f"{site}_seg{i}_final_positions.npz",
            final_positions=final_pos, initial_positions=pos0,
            alive=alive, qc_stopped=qc_stopped, times=field.times)
    return {
        "site": site,
        "input_file": str(path),
        "input_sha256": sha256(path),
        "n_raw_timestamps": int(ds.times_s.size),
        "time_range_utc": [
            datetime.fromtimestamp(float(ds.times_s[0]), timezone.utc).isoformat(),
            datetime.fromtimestamp(float(ds.times_s[-1]), timezone.utc).isoformat()],
        "parameters": {"max_gap_s": max_gap_s,
                       "integration_step": "one forcing interval (observed timestamps only)",
                       "n_side": n_side, "seed": seed,
                       "diffusivity": 0.0, "boundary": "reflect",
                       "accepted_qc_flags": [1],
                       "subregion_block_cells": block,
                       "subregion_mean_cell_validity": round(block_validity, 4),
                       "subregion_lat_range": [float(ds.latitude[iy][0]),
                                               float(ds.latitude[iy][-1])],
                       "subregion_lon_range": [float(ds.longitude[ix][0]),
                                               float(ds.longitude[ix][-1])]},
        "segments": segments,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--inputs", nargs="+", required=True,
                   help="ERDDAP .nc subset paths (glob allowed)")
    p.add_argument("--out", default="results/hfr_pilot")
    p.add_argument("--max-gap-s", type=float, default=10800.0,
                   help="split segments at observation gaps larger than this")
    p.add_argument("--n-side", type=int, default=8,
                   help="particle grid is n_side x n_side candidates")
    p.add_argument("--block", type=int, default=4,
                   help="pilot sub-region is the best block x block cell window")
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()

    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
              "engine": "simulate_m0 (Euler-Maruyama, K=0)",
              "files": []}
    for pattern in a.inputs:
        for path in sorted(Path(".").glob(pattern)):
            entry = run_file(path, max_gap_s=a.max_gap_s,
                             n_side=a.n_side, block=a.block, seed=a.seed)
            report["files"].append(entry)
            stem = path.stem.replace("EUHFR_NRTcurrent_HFR-NAdr-", "")
            (outdir / f"{stem}_summary.json").write_text(
                json.dumps(entry, indent=2) + "\n")
    (outdir / "pilot_report.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
