# HFR live endpoint and calibration-metadata check

**Snapshot inspected:** 25 November 2026  
**Purpose:** distinguish a stale catalogue/feed from slow bulk extraction and old calibration metadata. This is a metadata inspection, not an independent instrument calibration assessment.

## Live ERDDAP result

The current ERDDAP Data Access Form pages for both endpoints were retrieved on 25 November 2026. Both report the latest observation at **2026-11-25 13:00 UTC**, with NetCDF creation at approximately 13:43 UTC.

| Dataset | Operator | Coverage start | Latest observation | Last calibration date in metadata |
|---|---|---|---|---|
| IZOLA | NIB | 2022-10-16 00:03 UTC | 2026-11-25 13:00 UTC | **2023-01-01** |
| PIRAN | ARSO | 2021-01-01 00:00 UTC | 2026-11-25 13:00 UTC | **2015-01-10** |

Sources:
- IZOLA: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.html
- PIRAN: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3.html

Both pages expose the field testOutOfDate as now-1day, time_coverage_resolution as PT30M, and update_interval as void. Actual time-axis spacings are uneven: 32m16s for IZOLA and 37m00s for PIRAN. “Nominal 30-minute product” is accurate; “strictly regular 30-minute observations” is not.

## Interpretation

1. **The feed is not demonstrably stale at the snapshot time.** Both live metadata records advertise a same-day observation. Do not tell the funder that the HFR system had stopped updating.
2. **Calibration traceability is a material question.** The metadata expose last-calibration dates in 2023 (IZOLA) and 2015 (PIRAN). These dates are old, especially for Piran, but metadata alone do not prove inaccurate measurements or exclude later validation/maintenance. Ask the operators to confirm the calibration and validation history.
3. **A slow multi-year request does not prove a stale server.** The supplied IZOLA URL requests five variables over the full 2022–2026 period and full 20×22 grid. Benchmark short windows before diagnosing service performance.
4. **Spatial usability remains unverified.** A 20×22 catalogue grid (440 nominal cells) does not mean every cell has valid vectors at every time. Compute missingness, QC acceptance and spatial overlap from actual data.
5. **The vector product is a surface product.** EWCT and NSCT are eastward/northward surface-current components. Global metadata state that total velocities are least-squares reconstructions from radial measurements in areas where at least two radar stations overlap. Do not conflate radial measurements with complete vector fields.

## Reproducible endpoint benchmark

The script scripts/audit_hfr_endpoints.py uses only the Python standard library. For both datasets it fetches the current DAS metadata and requests 1-day and 7-day CSV subsets for EWCT, NSCT and QCflag. It records HTTP status, elapsed seconds, response size, row count, first/last returned timestamp, valid-value counts and QC flag counts.

Run from the repository root:

\`\`\`bash
python scripts/audit_hfr_endpoints.py --days 1 7 --timeout 120
\`\`\`

Save a local report (do not commit raw data):

\`\`\`bash
mkdir -p reports/hfr
python scripts/audit_hfr_endpoints.py --days 1 7 --timeout 120 > reports/hfr/live_endpoint_check.json
\`\`\`

The script deliberately avoids a multi-year archive. Repeat at different times to assess repeatability and feed latency. A successful short request establishes endpoint responsiveness only for that retrieval; it does not establish continuous availability.

## Application-ready interpretation

> The North Adriatic HFR infrastructure provides a live, publicly catalogued surface-current data stream, but its operational fitness for a microplastic-transport application must be established. The published products have uneven time-axis spacing; cell-level completeness and QC acceptance require quantification; and the catalogue exposes calibration dates that warrant confirmation with the operators (2023 for IZOLA; 2015 for PIRAN). RheoMarine will document data latency, response performance, spatial coverage, QC acceptance and calibration provenance before using the fields for model forcing or validation.

This is a concrete, testable WP1 data-readiness task. It avoids unsupported claims of instrument failure or data inaccuracy.

## Questions for NIB / ARSO / European HFR Node

1. Are the last-calibration dates currently exposed in the metadata still correct? If not, what are the dates and nature of subsequent calibration, validation or maintenance checks?
2. What calibration/validation procedure applies to the Level 2B vector product, and are uncertainty or validation reports available?
3. What explains uneven time-axis spacings and the difference between nominal 30-minute resolution and actual timestamps?
4. Are there known periods, grid cells or station-overlap limitations affecting Ankaran–Koper–Izola–Piran?
5. What QC acceptance rule is recommended for EWCT/NSCT model forcing, including treatment of flags 1, 2, 7 and 8?

## Status

- Live catalogue and same-day advertised observation: **documented at snapshot time**.
- Old calibration dates exposed in metadata: **documented; interpretation requires operator confirmation**.
- Endpoint response-time benchmark: **executed 25 November 2026** for 1/7/30-day windows on both nodes (HTTP 200; see `docs/hfr/` and `scripts/audit_hfr_endpoints.py`).
- Per-cell completeness, QC acceptance and coastal-sector overlap: **partially quantified** — cell-level QCflag fractions measured for both nodes over 30 days (IZOL ~51% flag=1; PIRA ~25%); spatial overlap analysis still pending.
- Instrument obsolescence or measurement inaccuracy: **not established and must not be claimed**.
