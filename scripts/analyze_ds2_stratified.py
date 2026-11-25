#!/usr/bin/env python3
"""Analyze MPs sinking through the rheological interface (Mrokowska ds2).
v2 — addresses post-merge audit findings.

For every experimental set x interrogation window (IW1/IW2) x particle
type we take the averaged centroid position z(t) (m, z positive downward;
MPs_position README: 1 px = 31 um but averaged files are already in m),
compute the instantaneous sinking speed w = dz/dt (moving-average
smoothed ensemble-averaged tracks -- kinematic analysis, not
single-particle dynamics), and split the trajectory into three zones
relative to the visible interface:

  above    : z <  z_upper
  interface: z_upper <= z <= z_lower
  below    : z >  z_lower

Interface bounds are taken from README_MPs_sinking_dynamics.txt.

v2 changes vs v1:
  * density profiles are explicitly sorted by z before computing
    top/bottom layer densities (rho_upper = median over z<0 samples,
    rho_lower = median over z>0 samples of the *measured* profile;
    fitted profile used as cross-check)
  * zone-coverage rule: a below/above ratio is reported only when
    n_above >= MIN_ZONE and n_below >= MIN_ZONE samples survive
    smoothing-edge trimming; otherwise the row is kept with an
    explicit 'insufficient_zone_coverage' flag
  * outputs are stratified: per-trajectory CSV plus a
    set x IW x particle-type summary CSV
  * set -> layer-order mapping is INFERRED, not from the paper:
    the Mendeley description states 6 experiments "XG overlaid by AS"
    and 3 "AS overlaid by XG"; the set3 series shows the inverted
    velocity signature (slow above / fast below), so we assign
    set1+set2 -> AS_over_XG and set3 -> XG_over_AS with
    confidence='inferred_not_paper_verified'.  Exact fluid recipes
    (salinity, XG g/L) remain an open item -- the Water Research
    paper is paywalled.

Outputs:
  ds2_interface_transit.csv        - one row per trajectory
  ds2_set_iw_particle_summary.csv  - medians per set x IW x particle
  ds2_interface_summary.json       - per-set density/layer metadata
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
        / "Density_and_refractive_index_profiles")
OUT_CSV = ROOT / "ds2_interface_transit.csv"
OUT_SUM = ROOT / "ds2_set_iw_particle_summary.csv"
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

# Inferred layer order -- see module docstring.  "over" = on top of.
LAYER_ORDER = {s: ("AS_over_XG" if s.startswith(("set1", "set2"))
                   else "XG_over_AS") for s in SETS}
MAPPING_NOTE = ("inferred from Mendeley dataset description (6x AS-over-XG, "
                "3x XG-over-AS) + set3 inverted velocity signature; "
                "NOT verified against the paywalled Water Research paper")

MIN_ZONE = 10  # min samples per zone for a reported ratio

# Interrogation-window role, INFERRED from the data (see analysis note):
# IW1 tracks show the full deceleration/acceleration through the
# interface; IW2 tracks are ~uniform in speed and match the IW1
# below-interface terminal speed, i.e. the second window samples only
# the lower layer (its z origin does not share the interface reference,
# so zone splitting is NOT applied to IW2).
WINDOW_ROLE = {"IW1": "interface_crossing", "IW2": "lower_layer"}


def smooth(y: np.ndarray, k: int) -> np.ndarray:
    k = max(3, k | 1)
    ker = np.ones(k) / k
    return np.convolve(y, ker, mode="same")


def zone_stats(t, z, n_grid=None):
    """Return (t, z, w) on a uniform time grid.

    Source timestamps are jittered and contain near-duplicates, so
    per-interval dz/dt produces huge spikes.  We sort by t, drop
    non-increasing samples, interpolate z onto a uniform grid with the
    median sampling interval, then differentiate and smooth.  This is a
    kinematic analysis of ensemble-averaged tracks.
    """
    if len(t) < 20:
        return None
    order = np.argsort(t)
    t, z = t[order], z[order]
    keep = np.concatenate([[True], np.diff(t) > 0])
    t, z = t[keep], z[keep]
    if len(t) < 20:
        return None
    dt_med = float(np.median(np.diff(t)))
    n = n_grid or min(len(t), int((t[-1] - t[0]) / dt_med) + 1)
    n = max(20, n)
    tu = np.linspace(t[0], t[-1], n)
    zu = np.interp(tu, t, z)
    w = np.gradient(zu, tu)
    k = max(5, n // 20)
    # pad edges so the smoothing window does not eat the track ends
    # (deep samples near z_max matter for below-interface coverage)
    wp = np.concatenate([np.full(k, w[0]), w, np.full(k, w[-1])])
    w = np.convolve(wp, np.ones(k) / k, mode="same")[k:-k]
    m = slice(2, -2)
    return tu[m], zu[m], w[m]


def ptype_of(fname: str) -> str:
    """set1_1_D_a.csv -> 'D' ; set1_1_S.csv -> 'S'."""
    parts = Path(fname).stem.split("_")
    # stem like set1_1_D_a -> particle token is parts[2] if len>3 else parts[2]
    return parts[2] if len(parts) >= 3 else parts[-1]


def spec_of(fname: str) -> str:
    """set1_1_D_a.csv -> 'D_a'."""
    parts = Path(fname).stem.split("_")
    return "_".join(parts[2:]) if len(parts) > 3 else parts[2]


def density_profile(setname: str):
    """Return dict with layer densities; z explicitly sorted, z=0 at
    the visible interface, z>0 downward (same convention as tracks)."""
    out = {}
    for kind in ("Density_and_RI_measured", "Density_RI_fitted"):
        f = DENS / kind / f"{setname}.csv"
        if not f.exists():
            continue
        d = np.genfromtxt(f, delimiter=",", skip_header=1)
        d = d[~np.isnan(d).any(axis=1)]
        if d.ndim != 2 or d.shape[1] < 2 or len(d) < 10:
            continue
        o = np.argsort(d[:, 0])
        z, rho = d[o, 0], d[o, 1]
        above = z < 0
        below = z > 0
        rec = {
            "n": int(len(z)),
            "z_min": float(z.min()), "z_max": float(z.max()),
            "rho_upper": float(np.median(rho[above])) if above.any() else None,
            "rho_lower": float(np.median(rho[below])) if below.any() else None,
            "rho_at_interface": float(np.interp(0.0, z, rho)),
            "n_above": int(above.sum()), "n_below": int(below.sum()),
        }
        if rec["rho_upper"] is not None and rec["rho_lower"] is not None:
            rec["delta_rho"] = rec["rho_lower"] - rec["rho_upper"]
        else:
            rec["delta_rho"] = None
        out[kind] = rec
    return out


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
                # columns are Z,t -> t=d[:,1], z=d[:,0]
                st = zone_stats(d[:, 1], d[:, 0])
                if st is None:
                    continue
                t, z, w = st
                rec = {"set": s, "iw": iw, "window_role": WINDOW_ROLE[iw],
                       "particle_file": f.name,
                       "particle_type": ptype_of(f.name),
                       "particle_spec": spec_of(f.name),
                       "layer_order_inferred": LAYER_ORDER[s],
                       "z_up": z_up, "z_lo": z_lo,
                       "interface_thickness_m": z_lo - z_up,
                       "t_max": float(t.max()), "z_max": float(z.max()),
                       "z_end_zone": ("below" if z[-1] > z_lo else
                                      "interface" if z[-1] >= z_up
                                      else "above")}
                if iw == "IW1":
                    above = z < z_up
                    inter = (z >= z_up) & (z <= z_lo)
                    below = z > z_lo
                    for name, mask in (("above", above), ("interface", inter),
                                       ("below", below)):
                        rec[f"n_{name}"] = int(mask.sum())
                        rec[f"w_{name}"] = (float(np.median(w[mask]))
                                            if mask.sum() >= 3 else "")
                    wa = rec["w_above"] if isinstance(rec["w_above"], float) else np.nan
                    wb = rec["w_below"] if isinstance(rec["w_below"], float) else np.nan
                    wi = rec["w_interface"] if isinstance(rec["w_interface"], float) else np.nan
                    ok_above = rec["n_above"] >= MIN_ZONE
                    ok_below = rec["n_below"] >= MIN_ZONE
                    rec["coverage_ok"] = bool(ok_above and ok_below)
                    rec["R_below_vs_above"] = (
                        float(wb / wa) if ok_above and ok_below
                        and np.isfinite(wa) and np.isfinite(wb) and wa != 0 else "")
                    rec["R_interface_vs_above"] = (
                        float(wi / wa) if ok_above and np.isfinite(wa)
                        and np.isfinite(wi) and wa != 0 else "")
                    if not (ok_above and ok_below):
                        rec["flag"] = "insufficient_zone_coverage"
                    elif rec["z_end_zone"] != "below":
                        rec["flag"] = "track_ends_inside_interface"
                    else:
                        rec["flag"] = ""
                else:
                    # IW2: lower-layer window; report overall speed only.
                    for name in ("above", "interface", "below"):
                        rec[f"n_{name}"] = ""
                        rec[f"w_{name}"] = ""
                    m = slice(len(w) // 10, -len(w) // 10)
                    rec["w_lower_layer"] = float(np.median(w[m]))
                    rec["n_samples"] = int(len(w))
                    rec["coverage_ok"] = ""
                    rec["R_below_vs_above"] = ""
                    rec["R_interface_vs_above"] = ""
                    rec["flag"] = "lower_layer_window_no_zone_split"
                rows.append(rec)

    fields = ["set", "iw", "window_role", "particle_file", "particle_type",
              "particle_spec", "layer_order_inferred", "z_up", "z_lo",
              "interface_thickness_m", "t_max", "z_max", "z_end_zone",
              "w_above", "n_above", "w_interface", "n_interface",
              "w_below", "n_below", "w_lower_layer", "n_samples",
              "coverage_ok", "R_below_vs_above", "R_interface_vs_above",
              "flag"]
    with open(OUT_CSV, "w", newline="") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=fields)
        wcsv.writeheader()
        wcsv.writerows(rows)

    # --- summary: median per set x IW x particle_type --------------------
    groups = defaultdict(list)
    for r in rows:
        groups[(r["set"], r["iw"], r["particle_type"])].append(r)
    sum_rows = []
    for (s, iw, pt), lst in sorted(groups.items()):
        def med(key):
            v = [float(r[key]) for r in lst
                 if isinstance(r.get(key), float)
                 and np.isfinite(float(r[key]))]
            return float(np.median(v)) if v else ""
        def cnt(key):
            return sum(1 for r in lst if r.get(key) != "")
        sum_rows.append({
            "set": s, "iw": iw, "particle_type": pt,
            "n_trajectories": len(lst),
            "n_with_below_ratio": cnt("R_below_vs_above"),
            "w_above_med": med("w_above"),
            "w_interface_med": med("w_interface"),
            "w_below_med": med("w_below"),
            "w_lower_layer_med": med("w_lower_layer"),
            "R_below_med": med("R_below_vs_above"),
            "R_interface_med": med("R_interface_vs_above"),
            "layer_order_inferred": LAYER_ORDER[s],
        })
    sf = ["set", "iw", "particle_type", "n_trajectories",
          "n_with_below_ratio", "w_above_med", "w_interface_med",
          "w_below_med", "w_lower_layer_med",
          "R_below_med", "R_interface_med", "layer_order_inferred"]
    with open(OUT_SUM, "w", newline="") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=sf)
        wcsv.writeheader()
        wcsv.writerows(sum_rows)

    # --- density / layer metadata ----------------------------------------
    dens = {}
    for s in SETS:
        prof = density_profile(s)
        dens[s] = {
            "layer_order_inferred": LAYER_ORDER[s],
            "mapping_confidence": "inferred_not_paper_verified",
            "measured": prof.get("Density_and_RI_measured"),
            "fitted": prof.get("Density_RI_fitted"),
        }

    # cross-check: IW2 lower-layer speed vs IW1 below-interface speed
    iw_check = {}
    for s in SETS:
        w1 = [r["w_below"] for r in rows
              if r["set"] == s and r["iw"] == "IW1"
              and isinstance(r.get("w_below"), float)]
        w2 = [r["w_lower_layer"] for r in rows
              if r["set"] == s and r["iw"] == "IW2"
              and isinstance(r.get("w_lower_layer"), float)]
        iw_check[s] = {
            "w_below_IW1_med": float(np.median(w1)) if w1 else None,
            "w_lower_IW2_med": float(np.median(w2)) if w2 else None,
            "ratio_IW2_over_IW1below": (float(np.median(w2) / np.median(w1))
                                      if w1 and w2 else None),
        }

    agg = defaultdict(list)
    for r in rows:
        if r["iw"] == "IW1" and isinstance(r["R_below_vs_above"], float):
            agg[r["set"]].append(r["R_below_vs_above"])
    summary = {
        "n_traj": len(rows),
        "min_zone_samples": MIN_ZONE,
        "interface_bounds_m": INTERFACE,
        "layer_order_mapping": LAYER_ORDER,
        "mapping_note": MAPPING_NOTE,
        "density_profiles": dens,
        "iw_consistency": iw_check,
        "retardation_by_set_IW1": {
            s: {"n": len(v),
                "R_below_median": float(np.median(v)),
                "R_below_mean": float(np.mean(v))}
            for s, v in sorted(agg.items())},
        "notes": [
            "w = dz/dt from ensemble-averaged centroid tracks; "
            "kinematic analysis, not single-particle dynamics",
            "IW1 = interface-crossing window: zone speeds and "
            "R_below_vs_above computed only here",
            "IW2 = lower-layer window (inferred): speeds are uniform "
            "and match IW1 below-interface values; zone split NOT "
            "applied because its z origin does not share the "
            "interface reference",
            "density z sorted explicitly; z=0 at visible interface, "
            "z>0 downward (assumed same convention as tracks)",
            "set3 bottom densities ~1037-1038 kg/m3 are far above "
            "AS42 (~1029); cannot be explained by XG <=1.5 g/L -- "
            "recipe verification against the paper still required",
        ],
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"trajectories: {len(rows)}")
    for s, d in summary["retardation_by_set_IW1"].items():
        c = iw_check[s]
        print(f"  {s}: R_below={d['R_below_median']:.3f} (n={d['n']}) "
              f"IW2/IW1below={c['ratio_IW2_over_IW1below']}")
    print(f"-> {OUT_CSV}\n-> {OUT_SUM}\n-> {OUT_JSON}")


if __name__ == "__main__":
    main()
