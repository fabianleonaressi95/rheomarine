# HFR data package — RheoMarine-SLO

Technical integration and reproducibility audit of the European HFR Node
North-Adriatic surface-current datasets, performed 25 November 2026.

**Scope:** data-access verification and sizing only. Nothing here validates
the measurements scientifically, and HFR surface currents are not evidence
of three-dimensional circulation or seabed deposition.

## Contents

| File | Content |
|------|---------|
| `hfr_optimized_queries.md` | Correct ERDDAP constraint syntax, common bbox, variable selection, curl examples |
| `hfr_archive_size_estimate.csv` | Per-window size/time/QC estimates for IZOL and PIRA (30d, 90d, 12mo, max archive) |
| `hfr_download_plan.md` | Phased download plan gated on QC review; no mass download launched |
| `../../data/hfr/IZOL_QCflag_20221024_20261125.nc.zip` | Zipped QCflag-only NetCDF for IZOL (full verified archive span) |
| `../../scripts/audit_hfr_endpoints.py` | Reproducible endpoint benchmark (Python stdlib only) |

## Datasets

| Node | ERDDAP dataset | Operator | Verified span | Grid |
|------|----------------|----------|---------------|------|
| IZOLA | `EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3` | NIB | 2022-11-24 → 2026-11-25 | 20×22 = 440 cells |
| PIRAN | `EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3` | ARSO | 2021-01-01 → 2026-11-25 | 440 cells (same bbox) |

Common bbox: lat 45.52685–45.78333, lon 13.375–13.78056, depth 0.0.
Variables used throughout: `EWCT`, `NSCT`, `QCflag` only.

## How to reproduce the audit

```bash
# 1. Endpoint benchmark (metadata + short subsets; safe, ~seconds)
python scripts/audit_hfr_endpoints.py --days 1 7 30 --timeout 300 \
  > reports/hfr/live_endpoint_check.json

# 2. Manual spot-check of the optimized query (see hfr_optimized_queries.md)
curl -L --fail --show-error --max-time 120 --get \
  --data-urlencode 'EWCT[(2026-11-24T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]' \
  --data-urlencode 'NSCT[(2026-11-24T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]' \
  --data-urlencode 'QCflag[(2026-11-24T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]' \
  'https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.csv0' \
  -o /tmp/IZOL_1d.csv0
```

Notes on reproducibility:

- The audit script anchors windows to `now − 3 h` (NRT feed lag). Re-running on
  a different day shifts the window; compare `requested_start/end_utc` and
  `first/last_returned_time` in the JSON, not absolute timestamps.
- `window_span_covered` is a coarse sanity flag (date-level). Always inspect
  the returned first/last timestamps for partial coverage.
- The 30-day estimates were measured on 25 Nov 2026; response times scale
  roughly with rows but server load varies — treat times as order-of-magnitude.

## How to read the estimates (`hfr_archive_size_estimate.csv`)

Denominators (all percentages use **total cells = n_timestamps × 440**,
including empty cells — missing data cannot be excluded server-side):

- `n_rows_csv` — CSV0 rows returned (every cell of every timestamp).
- `n_qcflag1_est` / `pct_qcflag1_est` — cells with `QCflag == 1` (pass) over
  total cells. **This is the strict-valid fraction.**
- `pct_nonfill_est` — cells with `QCflag != -127` (any flag value present)
  over total cells. Includes flagged-but-present observations.
- `basis` — `measured` = computed from the local QCflag NetCDF (IZOL) or the
  measured 30-day pull (PIRA); `extrapolated_*` = valid fractions carried
  over from the nearest measured window, sizes/times scaled by row count.
  Extrapolated rows are marked with `~` in numeric columns.

Measured vs extrapolated summary:

- **IZOL**: timestamps and QC fractions measured for all windows from the
  local `QCflag` NetCDF; only response times for >30d are extrapolated.
- **PIRA**: only the 30-day window was pulled; all other windows are
  extrapolations and must be re-measured before any large download.

## Temporal coverage caveats

- Nominal PT30M, but timestamps are irregular: median dt 1800 s, p95 1800 s
  (IZOL) / 3600 s (PIRA).
- IZOL: 69 gaps >1 h, max gap ~65 days. PIRA: ~2008 gaps >1 h, max ~51 days.
- PIRA coverage starts 2021-01-01 but is substantially more fragmented than
  IZOL; "longer archive" ≠ "better coverage".
- The NRT feed lags real time ~1–2 h; always clamp `end_time` or ERDDAP
  returns 404.

## Unresolved technical limitations

1. **No scientific validation performed.** Downloadable ≠ accurate. QCflag==1
   fractions (IZOL ~51% recent / ~23% last 12 mo; PIRA ~25%) are raw counts,
   not accuracy estimates. Independent validation (buoys, ADCP, models) is
   required before use in model forcing or skill assessment.
2. **Vector product is surface-only** (upper ~0.3–2.5 m). It cannot constrain
   vertical transport or seabed deposition.
3. **Calibration provenance unresolved**: metadata exposes
   `last_calibration_date` 2023-01-01 (IZOL) and 2015-01-10 (PIRA); operator
   confirmation pending.
4. **PIRA quality is lower and less characterized** — only a 30-day sample
   exists; monthly QC verification is a prerequisite for any >90-day pull.
5. **Spatial representativeness unverified**: 440 cells ≠ 440 valid
   observations; coastal-sector overlap within the Slovenian territorial sea
   still needs per-cell analysis.
6. **IZOL early-archive gap**: catalogue claims coverage from 2022-10-16 but
   the verified NetCDF starts 2022-11-24 (~5 weeks unaccounted).
7. **Server behaviour at scale untested**: >90-day single requests are
   estimated, not measured; chunked `.nc` pulls recommended.
8. **csv0 vs .nc parity not verified**: sizes for `.nc` are rough estimates.
