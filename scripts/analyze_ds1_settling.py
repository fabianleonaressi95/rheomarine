#!/usr/bin/env python3
"""Second-pass analysis of Mrokowska ds1 (settling in polymer solutions).

Joins settling_velocities.csv with measured particle dimensions, then:

1. particle table: mean L/I/S per spec, volume-equivalent diameter,
   aspect ratios (README_dimensions table used for S_PS; C_* specs have
   no dimension data in the dataset -> flagged, excluded from size stats)
2. retardation factor R = w_fluid / w_AS per solution x particle spec
   (run-level pairing: mean of per-run ratios is NOT used; ratio of
   group means, plus per-run ratios for spread)
3. aggregate retardation by solution, by material, by particle shape
4. orientation dynamics for non-spherical particles: circular spread of
   the recorded projection angle and its correlation with the
   instantaneous vertical velocity (smoothed), per spec x solution

Outputs:
  ds1_particle_dimensions.csv
  ds1_retardation.csv        (one row per spec x solution)
  ds1_analysis_summary.json
"""
from __future__ import annotations
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent / "data" / "ds1_rheology_settling"
VEL_CSV = ROOT / "settling_velocities.csv"
OUT_DIM = ROOT / "ds1_particle_dimensions.csv"
OUT_RET = ROOT / "ds1_retardation.csv"
OUT_JSON = ROOT / "ds1_analysis_summary.json"

# mean dims from README_dimensions_of_particles.txt (manufacturer / not
# re-measured).  C_* specs have NO dimension data in the dataset.
README_DIMS = {
    "S_PS": (1.042, 1.042, 1.042),
}
SOL_ORDER = ["AS", "AS_XG0.5", "AS_XG1", "AS_CR0.5", "AS_CR1",
             "AS_XGCR0.5", "AS_XGCR1"]


def load_dims() -> dict:
    """spec -> (L,I,S) in mm, averaged over measured particles."""
    dims = {}
    for f in ROOT.glob("*.csv"):
        stem = f.stem
        if (stem.startswith("AS") or stem.startswith("settling")
                or stem.startswith("ds1_") or "_run_" in stem):
            continue
        if stem in README_DIMS:
            continue
        try:
            d = np.genfromtxt(f, delimiter=";", skip_header=1)
        except Exception:
            try:
                d = np.genfromtxt(f, delimiter=",", skip_header=1)
            except Exception:
                continue
        if d.ndim != 2 or d.shape[1] < 3:
            continue
        d = d[~np.isnan(d).any(axis=1)]
        if len(d) == 0:
            continue
        dims[stem] = tuple(float(np.mean(d[:, i])) for i in range(3))
    dims.update(README_DIMS)
    return dims


def spec_of(r: dict) -> str:
    s = f"{r['particle_type']}_{r['material']}"
    if r.get("size_ind"):
        s += f"_{r['size_ind']}"
    return s


def circ_stats(angles_deg: np.ndarray) -> dict:
    """Circular spread of orientation angles (deg)."""
    a = np.deg2rad(angles_deg)
    C, S = np.cos(a).mean(), np.sin(a).mean()
    R = math.hypot(C, S)
    # circ std (deg), Mardia
    return {"ang_R": float(R), "ang_circ_std_deg": float(
        math.degrees(math.sqrt(-2 * math.log(max(R, 1e-12)))))}


def velocity_corr(t, z, angle):
    """Corr(smoothed |w|, angle deviation from circular mean)."""
    if len(t) < 30:
        return float("nan"), float("nan")
    w = -np.gradient(z, t)  # z increases downward -> sinking w positive
    k = max(5, len(w) // 15)
    ker = np.ones(k) / k
    ws = np.convolve(w, ker, mode="same")
    a = np.deg2rad(angle)
    # deviation from circular mean direction
    mu = math.atan2(np.sin(a).mean(), np.cos(a).mean())
    dev = np.angle(np.exp(1j * (a - mu)))
    m = slice(k, -k)
    if np.std(ws[m]) < 1e-12 or np.std(dev[m]) < 1e-12:
        return float("nan"), float("nan")
    c = float(np.corrcoef(np.abs(ws[m]), np.abs(dev[m]))[0, 1])
    # also corr of w (signed) with dev
    c2 = float(np.corrcoef(ws[m], dev[m])[0, 1])
    return c, c2


def main() -> None:
    rows = list(csv.DictReader(open(VEL_CSV)))
    dims = load_dims()

    # --- particle dimension table -------------------------------------
    specs = sorted({spec_of(r) for r in rows})
    dim_rows = []
    for s in specs:
        if s in dims:
            L, I, S = dims[s]
            vol_eq_d = (L * I * S) ** (1 / 3.0)  # cube-root of volume, mm
            dim_rows.append({
                "spec": s, "L_mm": L, "I_mm": I, "S_mm": S,
                "size_mm": vol_eq_d, "aspect_LS": L / S,
                "aspect_LI": L / I, "dims_source": "measured",
            })
        else:
            dim_rows.append({"spec": s, "size_mm": "",
                             "dims_source": "missing_in_dataset"})
    with open(OUT_DIM, "w", newline="") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=list(dim_rows[0].keys()))
        wcsv.writeheader()
        wcsv.writerows(dim_rows)

    # --- retardation per spec x solution -------------------------------
    # group means of w_raw
    grp = defaultdict(list)
    for r in rows:
        grp[(spec_of(r), r["solution_raw"])].append(float(r["w_raw"]))
    mean = {k: float(np.mean(v)) for k, v in grp.items()}

    ret_rows = []
    for s in specs:
        w_as = mean.get((s, "AS"))
        for sol in SOL_ORDER:
            w = mean.get((s, sol))
            if w is None:
                continue
            rec = {"spec": s, "solution": sol, "w_mean": w,
                   "n_runs": len(grp[(s, sol)])}
            if w_as:
                rec["R_vs_AS"] = w / w_as
                # per-run ratio spread
                base = grp.get((s, "AS"), [])
                if sol != "AS":
                    ratios = [x / b for x in grp[(s, sol)] for b in base]
                    rec["R_run_median"] = float(np.median(ratios))
            ret_rows.append(rec)
    with open(OUT_RET, "w", newline="") as fh:
        fields = ["spec", "solution", "w_mean", "n_runs", "R_vs_AS",
                  "R_run_median"]
        wcsv = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        wcsv.writeheader()
        wcsv.writerows(ret_rows)

    # --- aggregate retardation ------------------------------------------
    def agg(keyfn):
        out = defaultdict(lambda: defaultdict(list))
        for rec in ret_rows:
            if "R_vs_AS" not in rec or rec["solution"] == "AS":
                continue
            out[rec["solution"]][keyfn(rec["spec"])].append(rec["R_vs_AS"])
        return {sol: {k: {"n_specs": len(v),
                          "R_mean": float(np.mean(v)),
                          "R_median": float(np.median(v))}
                      for k, v in sorted(d.items())}
                for sol, d in out.items()}

    by_material = agg(lambda s: s.split("_")[1])
    by_shape = agg(lambda s: s.split("_")[0])

    # solution-level R across all specs (equal weight per spec)
    sol_R = defaultdict(list)
    for rec in ret_rows:
        if rec.get("R_vs_AS") is not None and rec["solution"] != "AS":
            sol_R[rec["solution"]].append(rec["R_vs_AS"])
    solution_summary = {sol: {"n_specs": len(v),
                              "R_mean": float(np.mean(v)),
                              "R_median": float(np.median(v)),
                              "R_min": float(np.min(v)),
                              "R_max": float(np.max(v))}
                        for sol, v in sol_R.items()}

    # --- orientation dynamics -------------------------------------------
    # subsample: every run file, but only non-spherical specs (angle is
    # meaningful for all, but spheres have no preferred axis)
    orient = defaultdict(list)
    for r in rows:
        if r["particle_type"] == "S":
            continue
        f = ROOT / r["file"]
        try:
            d = np.genfromtxt(f, delimiter=",", skip_header=1)
        except Exception:
            continue
        d = d[~np.isnan(d[:, 0])]
        if d.shape[0] < 30 or d.shape[1] < 4:
            continue
        order = np.argsort(d[:, 2])
        t, z, ang = d[order, 2], d[order, 1], d[order, 3]
        st = circ_stats(ang)
        c_abs, c_signed = velocity_corr(t, z, ang)
        key = (spec_of(r), r["solution_raw"])
        orient[key].append({**st, "corr_absw_angle": c_abs,
                            "corr_w_angle": c_signed})

    orient_summary = {}
    for (spec, sol), lst in orient.items():
        def m(k):
            v = [x[k] for x in lst if not math.isnan(x[k])]
            return float(np.mean(v)) if v else None
        orient_summary[f"{spec}|{sol}"] = {
            "n_runs": len(lst),
            "ang_R_mean": m("ang_R"),
            "ang_circ_std_mean_deg": m("ang_circ_std_deg"),
            "corr_absw_angle_mean": m("corr_absw_angle"),
            "corr_w_angle_mean": m("corr_w_angle"),
        }

    OUT_JSON.write_text(json.dumps({
        "n_runs": len(rows),
        "solutions": SOL_ORDER,
        "retardation_by_solution": solution_summary,
        "retardation_by_material": by_material,
        "retardation_by_shape": by_shape,
        "orientation": orient_summary,
        "notes": [
            "R = w_fluid / w_AS from group means of terminal-fit slopes",
            "z units as recorded in source CSVs (pixels vs m unresolved)",
            "C_* particle specs have no dimension data in the dataset",
        ],
    }, indent=2) + "\n")

    print(f"dims: {sum(1 for d in dim_rows if d.get('dims_source') == 'measured')}"
          f"/{len(dim_rows)} specs measured")
    print(f"retardation rows: {len(ret_rows)}")
    for sol, d in sorted(solution_summary.items()):
        print(f"  {sol:12s} R_mean={d['R_mean']:.3f} "
              f"[{d['R_min']:.3f},{d['R_max']:.3f}] n={d['n_specs']}")
    print(f"-> {OUT_JSON}")


if __name__ == "__main__":
    main()
