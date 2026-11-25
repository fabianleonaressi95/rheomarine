# HFR evidence audit — Slovenian territorial-sea pilot
**Date:** 25 November 2026  
**Purpose:** establish a verifiable territorial-data basis for RheoMarine-SLO without implying an OGS partnership.

## Executive result

A concrete public data route exists through the Slovenian HFR stations at **Izola (NIB)** and **Piran (ARSO)**. The European HFR Node exposes separate datasets for both stations. Their metadata identify the institutional operators, spatial extent, sampling interval, variables and quality flags. This is sufficient to establish a credible *data-access pathway* for the application; it is **not yet a completed spatial coverage/QC analysis** and must not be described as proof that every proposed coastal sector is continuously covered.

## Verified public sources

1. **NIB — HF radar system in the Gulf of Trieste:** https://www.nib.si/mbp/en/oceanographic-data-and-measurements/other-oceanographic-data/hf-radar-2  
   NIB states that the network consists of four nodes: Izola (NIB), Piran (ARSO), Aurisina (OGS) and Trieste (ARPA FVG), with measurements combined into a current-vector representation for the Gulf of Trieste.
2. **Izola HFR-NAdr dataset (NIB):** https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.html  
   Dataset ID: `EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3`. Live metadata inspected on 25 November 2026 report start of coverage 2022-10-16, latest observation 2026-11-25 13:00 UTC, nominal 30-minute resolution, grid bounds 45.52685–45.78333°N and 13.375–13.78056°E, and last_calibration_date 2023-01-01. The latter is an old calibration date exposed by the catalogue and requires confirmation from NIB; it does not alone prove measurement inaccuracy.
3. **Piran HFR-NAdr dataset (ARSO):** https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3.html  
   Dataset ID: `EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3`. Live metadata inspected on 25 November 2026 report start of coverage 2021-01-01, latest observation 2026-11-25 13:00 UTC, nominal 30-minute resolution, the same broad grid bounds, and last_calibration_date 2015-01-10. This is a notably old calibration date exposed by the catalogue and requires confirmation from ARSO; it does not alone prove measurement inaccuracy.
4. **ARPA FVG network description:** https://monitor.meteo.fvg.it/radar_marino.php?ln=-en  
   Describes the four-node HFR-NAdr network and the merged surface-current/wave products.
5. **OGS Gulf of Trieste Marine Observatory:** https://www.ogs.it/en/gulf-trieste-marine-observatory  
   Describes the WERA 24.5 MHz system, nominal 1.5 km spatial and 30-minute temporal resolution, with data distributed through the European HFR node.

## Variables and limitations

The ERDDAP products expose, among other fields:
- `EWCT`, `NSCT`: eastward and northward surface-current components;
- `RDVA`, `DRVA`: radial velocity and direction;
- `QCflag`, `OWTR_QC`, `CSPD_QC`, `VART_QC`, `MDFL_QC`, `AVRB_QC`, `RDCT_QC`, `POSITION_QC`: quality-control fields;
- `HCSS`, `EACC`: variance and radial-accuracy descriptors.

The Izola metadata describes the HFR measurements as representative of the upper 0.3–2.5 m of the ocean. HFR is therefore a surface-current observation source. It does **not** directly provide a full three-dimensional current field, vertical particle trajectories, or seabed-deposition measurements.

The published metadata state that the datasets are publicly accessible and free of charge, require citation, and are subject to the SeaDataNet data policy/licence; commercial use requires contact with the principal investigator. Preserve dataset citations and licence terms in all derived outputs.

## Application-ready territorial wording

> The project is anchored in the Slovenian territorial sea through the publicly catalogued HFR observation nodes at Izola (operated by NIB) and Piran (operated by ARSO). Their surface-current datasets are distributed through the European HFR Node and provide a documented route to observations at nominal 30-minute resolution. During the first project work package, the applicant will download the relevant time series, document the actual temporal availability and quality flags, and select a pilot sub-area within the Slovenian territorial sea according to valid spatial overlap and data completeness. HFR observations will be used as surface-current information only; vertical transport and seabed deposition will be treated as modelled processes requiring additional evidence, not as quantities directly measured by the radar.

## Mandatory M1 data-readiness procedure

Before fixing the pilot polygon or analysis window:
1. Download a time-bounded subset from both Izola and Piran datasets and preserve the retrieval timestamp, query URL, dataset ID and original files.
2. Inspect valid-data fraction by grid cell and time; map missing cells and the overlap area.
3. Apply and document the provider's QC flags; do not treat missing or rejected vectors as zero current.
4. Determine whether the vector product is available over the selected Slovenian coastal cells, or whether only radial products are available there.
5. Select the smallest defensible pilot polygon and time window. If valid coverage is insufficient, narrow the area or use the documented fallback in Section C; do not claim coverage for all four municipalities.
6. Keep a strict separation between calibration data and independent validation data.
7. Archive a data manifest and citation/licence statement.

## Status classification

| Claim | Status | Reason |
|---|---|---|
| Slovenian HFR nodes exist at Izola and Piran | **Documented** | NIB and European HFR Node metadata |
| Public dataset endpoints exist for Izola and Piran | **Documented** | ERDDAP catalogue entries |
| Nominal 30-minute sampling | **Documented** | Dataset metadata |
| HFR measures surface currents, not full-depth circulation | **Documented** | Dataset summary and measurement definition |
| Continuous usable coverage of every proposed coastal sector | **Not yet verified** | Requires data download and QC/spatial-overlap analysis |
| Independent validation dataset is available for all model metrics | **Open** | Must be selected and checked separately |
| OGS is a project partner | **Not claimed** | No partnership is confirmed; public network data do not imply a collaboration |

**Conclusion:** the territorial link is now supported by identifiable Slovenian observation infrastructure and public datasets. The remaining technical task is a reproducible coverage/QC extraction, not finding a hypothetical data source.


## Live endpoint and calibration follow-up (25 November 2026)

A separate live check now records the current metadata, the old calibration dates, and a reproducible short-window response/QC benchmark: [HFR live endpoint and calibration-metadata check](HFR_LIVE_ENDPOINT_AND_CALIBRATION_CHECK_2026-11-25.md). The benchmark script is `scripts/audit_hfr_endpoints.py`. The full multi-year request is not a suitable responsiveness test. Endpoint latency, cell-level completeness, QC acceptance and coastal-sector overlap remain pending execution and analysis. Do not describe the feed as stopped: the current metadata advertise same-day observations at 13:00 UTC on 25 November 2026.
