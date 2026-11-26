# M0 HFR pilot — input recovery and reproduction record

**Date:** 26 November 2026
**Status labels:** PILOT-REPRODUCED (Lagrangian K=0 sensitivity pilot);
software verification only — not physical validation.

## 1. Input recovery

The seven-day IZOL/PIRA NetCDF subsets required by the pilot were located
in the working tree at `data/hfr/raw/` (git-ignored by design). They are
the genuine ERDDAP velocity subsets — `EWCT`, `NSCT`, `QCflag` present —
not the QCflag-only archive.

| File | SHA-256 | Coverage (UTC) | nt |
|------|---------|----------------|----|
| `EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3_7d.nc` | `d37844f5…a1adef5d` | 2026-11-18T14:00 → 2026-11-25T14:00 | 337 |
| `EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3_7d.nc` | `908ee53d…4aafc353` | 2026-11-18T14:01 → 2026-11-25T15:00 | 325 |

Checksums match the values recorded in `results/hfr_pilot_audit*/` and
`docs/hfr/M0_HFR_PILOT_2026-11-25.md`. Machine-readable checksums live in
`data/hfr/SHA256SUMS.txt`; the same two files are published as release
assets (`hfr-m0-pilot-inputs-2026-11-25`) so the pilot can be reproduced
without access to the original workstation.

## 2. Schema verification (re-inspected 2026-11-26)

- Dimensions `time × depth=1 × latitude=20 × longitude=22`.
- `time`: s since 1970-01-01T00:00:00Z; irregular sampling (median 1800 s).
- `EWCT`/`NSCT`: m s⁻¹; fill −32.767. `QCflag`: int16, fill −127,
  `flag_values` 0–9 (`flag_meanings` verified: 1 = good_data).
- Observed QCflag values in both subsets: {−127, 1, 4}.
- Source: `https://erddap.hfrnode.eu/erddap/griddap/`, datasets
  `EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3` (NIB) and
  `EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3` (ARSO); retrieval syntax in
  `docs/hfr/hfr_optimized_queries.md`.

## 3. Reproduction

Environment: Python 3.10.12, numpy 2.2.6, scipy 1.15.3 (Linux).

```bash
sha256sum -c data/hfr/SHA256SUMS.txt          # from data/hfr/
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/run_hfr_m0_pilot.py \
  --inputs 'data/hfr/raw/*_7d.nc' --out /tmp/hfr_repro \
  --block 4 --boundary reflect
```

## 4. Verification result

The regenerated run (`--block 4 --boundary reflect`, seed 42, `max_gap_s`
10800 s, `qc_flags=1`) was compared cell-by-cell against the committed
`results/hfr_pilot_audit/` outputs:

- `IZOL_v3_7d_summary.json`, `PIRA_v3_7d_summary.json`: **identical**
  (all fields except `generated_at_utc`).
- All 11 `*_final_positions.npz` segment files: **bit-identical**
  arrays (`initial_positions`, `final_positions`, `alive`,
  `qc_stopped`, `exited`, `times`, `displacement_m`).

Conclusion: the committed audit pilot is exactly reproducible from the
recovered raw inputs on the current `main` code. This upgrades the pilot
evidence from "previously executed" to **PILOT-REPRODUCED** for the
Lagrangian K=0 surface-advection sensitivity experiment. It remains a
software/numerical exercise: no independent observations were compared,
and nothing here validates transport, retention, vertical transport or
deposition.

## 5. What is still missing

- Longer-window subsets (90 d / 12 mo) per `docs/hfr/hfr_download_plan.md`
  — not launched; requires a project decision and PIRA monthly QC review.
- Independent validation observations (ADCP, drifters, buoys, particle
  samples): see `docs/validation/HFR_PILOT_SCIENTIFIC_VALIDATION_GATE_2026-11-25.md`
  §2–§3 — gate remains **BLOCKED** pending data acquisition.
