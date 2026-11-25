#!/usr/bin/env python3
"""Validate an observational CSV against docs/validation/OBSERVATIONAL_DATA_SCHEMA.md.

Read-only checker: it reports contract violations and coverage statistics;
it never modifies, interpolates or repairs the input file.

Usage:
    python3 scripts/check_observation_file.py observations.csv [--json]

Exit codes: 0 = structurally valid (warnings allowed), 2 = contract
violations found, 1 = file/usage error.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

OBS_TYPES = {
    "eulerian_point", "current_profile", "drifter_position",
    "drifter_velocity", "hfr_vector", "hfr_radial", "env_forcing",
    "particle_sample",
}
DEPTH_REFS = {"below_surface", "below_sea_level", "above_bottom",
              "pressure_dbar"}
DIR_CONVENTIONS = {"nautical_from_north_cw", "oceanographic_from_east_ccw",
                   "math_rad", "other"}
MISSING_REASONS = {"not_sampled", "instrument_gap", "qc_rejected",
                   "out_of_coverage", "fill_value", "unknown", ""}

REQUIRED = ["obs_id", "dataset_id", "instrument_id", "obs_type",
            "time_utc", "longitude", "latitude", "qc_flag",
            "source_dataset", "retrieved_utc", "licence"]

# generous plausibility bounds reported as warnings, never enforced:
# ocean currents rarely exceed ~5 m/s; anything beyond is suspicious but
# not contract-invalid (e.g. wind-forced extremes are still data).
SPEED_WARN_MS = 5.0


def _f(row: dict, key: str):
    v = (row.get(key) or "").strip()
    if v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return "INVALID"


def _parse_utc(s: str):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def check(path: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        missing_cols = [c for c in REQUIRED if c not in fieldnames]
        if missing_cols:
            return [f"missing required columns: {missing_cols}"], {}
        rows = list(reader)

    if not rows:
        return ["file contains no data rows"], {}

    n = len(rows)
    stats = {
        "rows": n,
        "obs_type_counts": {},
        "missing_reason_counts": {},
        "time_min_utc": None,
        "time_max_utc": None,
        "lon_min": None, "lon_max": None,
        "lat_min": None, "lat_max": None,
        "depth_min_m": None, "depth_max_m": None,
        "speed_gt_5ms_count": 0,
        "unparsed_time_count": 0,
    }
    times = []
    lons, lats, deps = [], [], []

    for i, row in enumerate(rows, start=2):  # line 1 = header
        tag = f"line {i}"
        ot = (row.get("obs_type") or "").strip()
        if ot not in OBS_TYPES:
            errors.append(f"{tag}: obs_type '{ot}' not in vocabulary")
        stats["obs_type_counts"][ot] = stats["obs_type_counts"].get(ot, 0) + 1

        t = _parse_utc((row.get("time_utc") or "").strip())
        if t is None:
            stats["unparsed_time_count"] += 1
            errors.append(f"{tag}: time_utc not ISO-8601: "
                          f"'{row.get('time_utc')}'")
        else:
            times.append(t)

        lon, lat = _f(row, "longitude"), _f(row, "latitude")
        if lon == "INVALID" or lat == "INVALID" or lon is None or lat is None:
            errors.append(f"{tag}: longitude/latitude missing or non-numeric")
        else:
            if not (-180 <= lon <= 180):
                errors.append(f"{tag}: longitude {lon} out of range")
            if not (-90 <= lat <= 90):
                errors.append(f"{tag}: latitude {lat} out of range")
            lons.append(lon); lats.append(lat)

        depth = _f(row, "depth_m")
        if depth not in (None, "INVALID"):
            ref = (row.get("depth_reference") or "").strip()
            if ref not in DEPTH_REFS:
                errors.append(f"{tag}: depth_m present but depth_reference "
                              f"'{ref}' missing/invalid")
            deps.append(depth)
        elif depth == "INVALID":
            errors.append(f"{tag}: depth_m non-numeric")

        d = (row.get("direction") or "").strip()
        if d:
            conv = (row.get("direction_convention") or "").strip()
            if conv not in DIR_CONVENTIONS:
                errors.append(f"{tag}: direction present but "
                              f"direction_convention '{conv}' invalid")

        mr = (row.get("missing_reason") or "").strip()
        if mr not in MISSING_REASONS:
            errors.append(f"{tag}: missing_reason '{mr}' not in vocabulary")
        stats["missing_reason_counts"][mr or "(blank)"] = \
            stats["missing_reason_counts"].get(mr or "(blank)", 0) + 1

        spd = _f(row, "speed")
        if isinstance(spd, float) and abs(spd) > SPEED_WARN_MS:
            stats["speed_gt_5ms_count"] += 1

    if times:
        stats["time_min_utc"] = min(times).isoformat()
        stats["time_max_utc"] = max(times).isoformat()
    if lons:
        stats.update(lon_min=min(lons), lon_max=max(lons),
                     lat_min=min(lats), lat_max=max(lats))
    if deps:
        stats.update(depth_min_m=min(deps), depth_max_m=max(deps))

    # temporal gap report: largest gap between consecutive sorted times
    if len(times) > 1:
        ts = sorted(times)
        gaps = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
        stats["max_gap_s"] = max(gaps)
        stats["median_gap_s"] = sorted(gaps)[len(gaps) // 2]
    return errors, stats


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_file", type=Path)
    p.add_argument("--json", action="store_true",
                   help="emit machine-readable report only")
    a = p.parse_args()
    if not a.csv_file.is_file():
        print(f"error: {a.csv_file} not found", file=sys.stderr)
        return 1
    errors, stats = check(a.csv_file)
    report = {"file": str(a.csv_file), "errors": errors, "stats": stats}
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"file: {a.csv_file}")
        for e in errors:
            print(f"  ERROR {e}")
        print(f"rows: {stats.get('rows')}")
        print(f"obs_type_counts: {stats.get('obs_type_counts')}")
        print(f"time range: {stats.get('time_min_utc')} -> "
              f"{stats.get('time_max_utc')}")
        print(f"lon/lat range: {stats.get('lat_min')},{stats.get('lon_min')} "
              f"-> {stats.get('lat_max')},{stats.get('lon_max')}")
        if "max_gap_s" in stats:
            print(f"temporal gaps: median {stats['median_gap_s']} s, "
                  f"max {stats['max_gap_s']} s")
        print(f"missing_reason_counts: {stats.get('missing_reason_counts')}")
        print(f"speed>|5|m/s count (warning only): "
              f"{stats.get('speed_gt_5ms_count')}")
        print("RESULT:", "FAIL" if errors else "PASS (warnings possible)")
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
