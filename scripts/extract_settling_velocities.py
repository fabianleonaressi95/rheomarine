#!/usr/bin/env python3
"""Extract terminal settling velocities from Mrokowska ds1 run files.

Each *_run_*.csv has columns x, z, t, angle (README says x,z in pixels;
units are left as recorded -- a pixel/m calibration is NOT in the
dataset and is flagged as an open item).  We fit dz/dt on the terminal
window (last TERMINAL_FRAC of each trajectory) and report slope,
R^2 of the tail fit, trajectory duration and span, plus parsed
experimental metadata from the filename.

Outputs:
  settling_velocities.csv  - one row per run
  settling_summary.json    - aggregate stats per solution x particle
"""
from __future__ import annotations
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent / "data" / "ds1_rheology_settling"
OUT_CSV = ROOT / "settling_velocities.csv"
OUT_JSON = ROOT / "settling_summary.json"
TERMINAL_FRAC = 0.4

NAME_RE = re.compile(
    r"^(AS(?:_(?:XGCR|XG|CR)[0-9.]*|_[0-9.]+)?)_(.+)_run_(\d+)\.csv$"
)


def parse_name(fn: str) -> dict:
    m = NAME_RE.match(fn)
    if not m:
        return {"file": fn, "parse_error": True}
    sol, spec, run = m.group(1), m.group(2), int(m.group(3))
    parts = spec.split("_")
    ptype, mat, ind = parts[0], parts[1] if len(parts) > 1 else "", (
        parts[2] if len(parts) > 2 else ""
    )
    s = sol[3:] if sol.startswith("AS_") else ""
    conc = ""
    mm = re.search(r"(\d+(?:\.\d+)?)$", s)
    if mm:
        conc = mm.group(1)
        base = s[: mm.start()]
    else:
        base = s
    return {
        "file": fn,
        "solution_raw": sol,
        "fluid": base if base else "AS",
        "conc_gL": conc,
        "particle_type": ptype,
        "material": mat,
        "size_ind": ind,
        "run": run,
    }


def terminal_fit(t: np.ndarray, z: np.ndarray):
    n = len(t)
    k = max(5, int(n * TERMINAL_FRAC))
    tt, zz = t[-k:], z[-k:]
    A = np.vstack([tt, np.ones(k)]).T
    slope, intercept = np.linalg.lstsq(A, zz, rcond=None)[0]
    pred = slope * tt + intercept
    ss_res = float(np.sum((zz - pred) ** 2))
    ss_tot = float(np.sum((zz - zz.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    # drift check: slope on first vs second half of the tail window
    h = k // 2
    s1 = np.polyfit(tt[:h], zz[:h], 1)[0] if h > 2 else float("nan")
    s2 = np.polyfit(tt[h:], zz[h:], 1)[0] if k - h > 2 else float("nan")
    return {
        "w_raw": float(slope),
        "tail_r2": float(r2),
        "tail_slope_drift": float(abs(s2 - s1)),
        "n_points": int(n),
        "t_max": float(t.max()),
        "z_span": float(z.max() - z.min()),
        "z_final": float(z[-1]),
    }


def main() -> None:
    rows = []
    files = sorted(ROOT.glob("*_run_*.csv"))
    for f in files:
        meta = parse_name(f.name)
        try:
            d = np.genfromtxt(f, delimiter=",", skip_header=1)
            d = d[~np.isnan(d[:, 0])]
            t, z = d[:, 2], d[:, 1]
            order = np.argsort(t)
            t, z = t[order], z[order]
            fit = terminal_fit(t, z)
        except Exception as exc:  # noqa: BLE001
            meta["error"] = str(exc)
            continue
        rows.append({**meta, **fit})

    # write CSV
    keys = ["file", "solution_raw", "fluid", "conc_gL", "particle_type",
            "material", "size_ind", "run", "w_raw", "tail_r2",
            "tail_slope_drift", "n_points", "t_max", "z_span", "z_final"]
    with open(OUT_CSV, "w") as fh:
        fh.write(",".join(keys) + "\n")
        for r in rows:
            fh.write(",".join(str(r.get(k, "")) for k in keys) + "\n")

    # summary per solution x particle_type x material x size
    groups = {}
    for r in rows:
        key = (r.get("solution_raw"), r.get("particle_type"),
               r.get("material"), r.get("size_ind"))
        groups.setdefault(key, []).append(r["w_raw"])
    summary = {
        k: {
            "n_runs": len(v),
            "w_mean": float(np.mean(v)),
            "w_std": float(np.std(v)),
            "w_cv": float(np.std(v) / abs(np.mean(v))) if np.mean(v) else None,
        }
        for k, v in sorted(groups.items(), key=lambda kv: str(kv[0]))
    }
    OUT_JSON.write_text(json.dumps({
        "n_files": len(files),
        "n_parsed": len(rows),
        "terminal_frac": TERMINAL_FRAC,
        "units_note": "x,z as recorded in source CSV (README claims pixels; "
                      "absolute calibration not present in dataset)",
        "groups": {str(k): v for k, v in summary.items()},
    }, indent=2) + "\n")
    print(f"parsed {len(rows)}/{len(files)} -> {OUT_CSV}")


if __name__ == "__main__":
    main()
