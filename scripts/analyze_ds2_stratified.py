#!/usr/bin/env python3
"""Analyze MPs sinking through the rheological interface (Mrokowska ds2).

For every experimental set x interrogation window (IW1/IW2) x particle
type we take the averaged centroid position z(t) (m, z positive downward,
from README_MPs_position: 1 px = 31 um but averaged files are already in
m), compute the instantaneous sinking speed w = dz/dt, and split the
trajectory into three zones relative to the visible interface:

  above    : z <  z_upper
  interface: z_upper <= z <= z_lower
  below    : z >  z_lower

Interface bounds are taken from README_MPs_sinking_dynamics.txt.
We report median w per zone and the retardation ratios
w_below/w_above and w_interface/w_above.  Density contrast across the
interface is estimated from the tanh-fitted density profiles
(Density_RI_fitted): rho_top = median of upper quartile, rho_bot =
median of lower quartile of each profile.

Outputs:
  ds2_interface_transit.csv  - one row per set x IW x particle type
  ds2_interface_summary.json - per-set density jump + aggregate stats
"""
from __future__ import annotations
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent / "data" / "ds2_stratified"
DYN = ROOT / "MPs_sinking_dynamics_x" / "MPs_sinking_dynamics"
DENS = (ROOT / "Density_and_refractive_index_profiles_x"
        / "Density_and_refractive_index_profiles" / "Density_RI_fitted")
OUT_CSV = ROOT / "ds2_interface_transit.csv"
OUT_JSON = ROOT / "ds2_interface_summary.json"

# z bounds of the visible interface [m], from README_MPs_sinking_dynamics
INTERFACE = {
    "set1_1": (0.0323, 0.0380), "set1_2": (0.0267, 0.0350),
    "set1_3": (0.0317, 0.0371), "set2_1": (0.0252, 0.0325),
    "set2_2": (0.0239, 0.0335), "set2_3": (0.0376, 0.0399),
    "set3_1": (0.0184, 0.0295), "set3_2": (0.0300, 0.0400),
    "set3_3": (0.0389, 0.0554),
}
SETS = sorted(INTERFACE)


def smooth(y: np.ndarray, k: int) -> np.ndarray:
    k = max(3, k | 1)
    ker = np.ones(k) / k
    return np.convolve(y, ker, mode="same")


def zone_stats(t, z):
    """Return dict of median speeds per zone for one trajectory."""
    if len(t) < 20:
        return None
    order = np.argsort(t)
    t, z = t[order], z[order]
    # drop non-monotone time duplicates
    keep = np.concatenate([[True], np.diff(t) > 0])
    t, z = t[keep], z[keep]
    w = np.gradient(z, t)
    k = max(5, len(w) // 20)
    w = smooth(w, k)
    m = slice(k, -k)  # trim edge effects of smoothing
    return t[m], z[m], w[m]


def main() -> None:
    rows = []
    for iw in ("IW1", "IW2"):
        base = DYN / "MPs_averaged_position" / iw
        if not base.is_dir():
            continue
        for setdir in sorted(base.iterdir()):
            if not setdir.is_dir() or setdir.name not in INTERFACE:
                continue
            s = setdir.name
            z_up, z_lo = INTERFACE[s]
            for f in sorted(setdir.glob("*.csv")):
                try:
                    d = np.genfromtxt(f, delimiter=",", skip_header=1)
                except Exception:
                    continue
                d = d[~np.isnan(d[:, 0])]
                if d.ndim != 2 or d.shape[1] < 2 or len(d) < 20:
                    continue
                st = zone_stats(d[:, 1], d[:, 0])
                if st is None:
                    continue
                t, z, w = st
                ptype = f.stem.split("_")[-1] if "_" in f.stem else f.stem
                # classify each sample
                above = z < z_up
                inter = (z >= z_up) & (z <= z_lo)
                below = z > z_lo
                rec = {"set": s, "iw": iw, "particle": f.stem,
                       "z_up": z_up, "z_lo": z_lo,
                       "t_max": float(t.max()), "z_max": float(z.max())}
                for name, mask in (("above", above), ("interface", inter),
                                   ("below", below)):
                    if mask.sum() >= 5:
                        rec[f"w_{name}"] = float(np.median(w[mask]))
                        rec[f"n_{name}"] = int(mask.sum())
                    else:
                        rec[f"w_{name}"] = ""
                        rec[f"n_{name}"] = int(mask.sum())
                wa, wb, wi = (rec.get("w_above") or np.nan,
                              rec.get("w_below") or np.nan,
                              rec.get("w_interface") or np.nan)
                finite = lambda v: isinstance(v, float) and np.isfinite(v)
                rec["R_below_vs_above"] = (
                    float(wb / wa) if finite(wa) and finite(wb) and wa != 0
                    else "")
                rec["R_interface_vs_above"] = (
                    float(wi / wa) if finite(wa) and finite(wi) and wa != 0
                    else "")
                rows.append(rec)

    fields = ["set", "iw", "particle", "z_up", "z_lo", "t_max", "z_max",
              "w_above", "n_above", "w_interface", "n_interface",
              "w_below", "n_below", "R_below_vs_above",
              "R_interface_vs_above"]
    with open(OUT_CSV, "w", newline="") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=fields)
        wcsv.writeheader()
        wcsv.writerows(rows)

    # --- density contrast per set --------------------------------------
    dens = {}
    for s in SETS:
        f = DENS / f"{s}.csv"
        if not f.exists():
            continue
        d = np.genfromtxt(f, delimiter=",", skip_header=1)
        d = d[~np.isnan(d).any(axis=1)]
        if d.ndim != 2 or d.shape[1] < 2 or len(d) < 10:
            continue
        z, rho = d[:, 0], d[:, 1]
        n = len(z)
        rho_top = float(np.median(rho[: n // 4]))
        rho_bot = float(np.median(rho[3 * n // 4:]))
        dens[s] = {"rho_top_kgm3": rho_top, "rho_bot_kgm3": rho_bot,
                   "delta_rho": rho_bot - rho_top,
                   "z_range": [float(z.min()), float(z.max())]}

    # aggregate retardation
    agg = defaultdict(list)
    for r in rows:
        if r["R_below_vs_above"] != "":
            agg[r["set"]].append(float(r["R_below_vs_above"]))
    summary = {
        "n_traj": len(rows),
        "interface_bounds_m": INTERFACE,
        "density_profiles": dens,
        "retardation_by_set": {
            s: {"n": len(v), "R_below_mean": float(np.mean(v)),
                "R_below_median": float(np.median(v))}
            for s, v in sorted(agg.items())},
        "notes": [
            "w = dz/dt from averaged centroid position, Savitzky-free "
            "moving average; zones defined by visible interface bounds",
            "set -> fluid composition mapping is in the source paper "
            "(Mrokowska et al. 2025, Water Res. 280:123487), not in "
            "the dataset files",
        ],
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"trajectories: {len(rows)}")
    for s, d in summary["retardation_by_set"].items():
        dd = dens.get(s, {})
        print(f"  {s}: R_below={d['R_below_median']:.3f} "
              f"(n={d['n']})  drho={dd.get('delta_rho', float('nan')):+.2f}")
    print(f"-> {OUT_CSV} / {OUT_JSON}")


if __name__ == "__main__":
    main()
