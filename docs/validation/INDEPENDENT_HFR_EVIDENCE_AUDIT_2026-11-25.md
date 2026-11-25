# Independent evidence audit for the HFR pilot
**Date:** 25 November 2026  
**Status:** preliminary source audit; no new field data downloaded or analysed.

## Executive decision

| Gate | Decision | Evidence |
|---|---|---|
| HFR forcing source | PASS — documented | OGS documents four WERA stations: Aurisina, Piran, Izola and Trieste; nominal 1.5 km / 30 min product. |
| Independent in-situ current comparison | CONDITIONAL | OGS documents MAMBO-1 buoys with acoustic current meters; raw series, instrument details, depth and overlap not verified. |
| Independent drifter trajectories | OPEN | OGS/NODC offers mobile-platform data routes, but no matching surface-drifter deployment was identified. |
| Historical Slovenian microplastic observations | PASS — regional benchmark | Gajšt et al. (2016): 17 surface trawls over 20 months. |
| Sample-level microplastic validation data | BLOCKED | Public records establish aggregate results, not coordinates, dates and counts per tow. |
| Geographic representativeness of automatic 4x4/8x8 crop | NOT ESTABLISHED | Computational crop is not a coastal pilot polygon. |
| Independent validation of microplastic transport | NO | No compatible independent particle observations have been matched to model output. |

**Conclusion:** current evidence supports a computational transport demonstration and a credible field-validation plan, not an independently validated microplastic forecast.

## 1. HFR network: inspect the integrated product

OGS documents a four-station WERA 24.5 MHz network at Aurisina, Piran, Izola and Trieste. The network maps surface currents at nominal 1.5 km spatial and 30-minute temporal resolution. Total vectors are reconstructed by least-squares mapping of radial measurements from multiple stations onto a Cartesian grid in their overlap area.

Sources:
- OGS observatory: https://www.ogs.it/en/gulf-trieste-marine-observatory
- OGS Italian page with station list: https://www.ogs.it/it/osservatorio-marino-golfo-di-trieste
- European HFR Node catalogue: https://erddap.hfrnode.eu/erddap/wms/index.htmlTable
- IZOL: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.html
- PIRA: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3.html

The catalogue exposes radial variables and total eastward/northward components (EWCT/NSCT), together with QC fields. The station products describe measurements representative of approximately the upper 0.3–2.5 m. HFR does not provide full-depth currents, vertical particle trajectories or seabed-deposition measurements.

**Implication:** inspect the integrated four-station total-vector product and its own QC/coverage, not just the nominal extents of IZOL and PIRA. Station feeds remain useful for provenance and diagnosis. Missing vectors are never zero currents.

## 2. Independent current observations

### 2.1 OGS MAMBO-1 acoustic current meters

OGS states that its FVG marine monitoring network includes three MAMBO-1 buoys with multiparameter probes at 10 m and acoustic current meters measuring the current field, with real-time transmission.

Source: https://www.ogs.it/en/gulf-trieste-marine-observatory

This is a concrete in-situ current-data lead. However, the public description does not establish that the instrument is an ADCP; do not call it one without instrument metadata. The stated 10 m probe depth is not equivalent to the HFR upper 0.3–2.5 m sensing layer. Exact coordinates, instrument model, measurement volume/depth, sampling interval, deployment dates, QC and downloadable raw data remain unverified.

**Permitted use if obtained:** independent subsurface current-field comparison at the actual instrument depth, explicitly accounting for vertical mismatch. It is not direct validation of surface HFR velocity.

**Request to OGS:** buoy coordinates and deployment history; instrument make/model and measurement depth/volume; raw and QC'd east/north time series; sampling interval; calibration and uncertainty; outages; access, licence and citation requirements.

### 2.2 OGS/NODC and mobile platforms

OGS/NODC describes access to controlled marine observations and a real-time fixed-station viewer. OGS separately points to Euro-Argo-Italy for drifters, floats and gliders.

Sources:
- NODC: https://nodc.ogs.it/
- OGS real-time data: https://www.ogs.it/en/real-time-data
- C1-LTER/MAMBO portal: https://www.ogs.it/en/real-time-data/coastal-marine-observatory-site-gulf-trieste-c1-lter-mambo

These are data-discovery routes, not proof that a suitable surface-drifter trajectory exists for the pilot dates and footprint. Argo floats and gliders must not be treated as surface drifters. Verify platform type, drogue/depth and trajectory sampling individually.

A current-meter comparison tests the hydrodynamic field; a drifter may test a Lagrangian trajectory. Neither validates microplastic concentration, polymer composition, settling or beaching.

## 3. Historical microplastic observations: Gajšt et al. (2016)

T. Gajšt, T. Bizjak, A. Palatinus, S. Liubartseva and A. Kržan (2016), “Sea surface microplastics in Slovenian part of the Northern Adriatic,” Marine Pollution Bulletin 113(1–2), 392–399. DOI: https://doi.org/10.1016/j.marpolbul.2016.10.031

Records:
- PubMed: https://pubmed.ncbi.nlm.nih.gov/27771097/
- Publisher: https://www.sciencedirect.com/science/article/abs/pii/S0025326X16308475

The 2016 abstract reports 17 sea-surface trawls over 20 months in the Slovenian part of the Gulf of Trieste, with a mean of 406 × 10^3 particles km⁻² and over 80% polyethylene.

A 2015 MICRO conference abstract by Palatinus et al. reports four sampling events between December 2012 and August 2014, 17 samples using a 300 μm epineuston net, size range 300 μm–5 mm, and a different aggregate mean of 471,903 particles km⁻² (with minimum and maximum values):
https://usiena-air.unisi.it/retrieve/e0feeaa8-d060-44d2-e053-6605fe0a8db0/MICRO2015_book_of_abstract%20%281%29.pdf

The two reported aggregate means must not be averaged or silently substituted. Reconcile the conference abstract with the final paper before quoting a quantitative benchmark.

**Data request to authors / Institute of Water of Slovenia / University of Nova Gorica:**
1. sample ID, date and time per tow;
2. start/end coordinates or tow track, duration and speed;
3. filtered area/volume and calculation method;
4. sample-level counts and concentrations, including zeros/non-detects;
5. size distribution, mesh and retention details;
6. polymer identification per sample and analytical subsampling fraction;
7. blanks, contamination controls, recovery/correction and uncertainty;
8. sampling layer and sea-state conditions;
9. reuse permission/licence and citation requirements.

Until sample-level records and metadata are obtained, classify Gajšt as **Tier C historical regional benchmark**. Do not reconstruct point observations from the aggregate mean. Marchetto et al. observations from the Venice Lagoon are geographically distinct and must not be merged with Slovenian samples.

## 4. Pilot-domain decision

The repository's existing HFR audit identifies IZOL as the initial candidate and PIRA as complementary, with different QC acceptance and temporal fragmentation. The automatic maximum-coverage 4x4 crop is a computational selection criterion, not a defensible geographic boundary. 8x8 is a sensitivity case, not automatically a better scientific domain.

Before selecting a polygon:
1. obtain the integrated four-station vector product and station feeds for one declared period;
2. intersect valid EWCT/NSCT vectors with an authoritative Slovenian territorial-sea/coastline polygon;
3. calculate valid-vector fraction by cell and timestamp;
4. map connected valid regions, gaps and distance to coast;
5. declare minimum coverage/continuity criteria before selection;
6. choose a contiguous polygon with enough valid ocean cells and a meaningful coastal sector; report rejected alternatives;
7. retain 4x4/8x8 outputs as algorithmic sensitivity tests, not geographic evidence.

No polygon should be selected from a municipality name or rectangular crop alone. Continuous coverage of all Slovenian coastal municipalities is not established.

## 5. What the current M0 pilot establishes

The current HFR particle pilot is a K=0, surface, forward-Euler Lagrangian advection exercise with explicit QC and boundary policies. Exact segment-to-cell traversal is a meaningful software-verification improvement: invalid QC cells touched by the implemented straight segment are conservatively rejected.

It does **not** establish:
- HFR velocity accuracy against independent in-situ measurements;
- trajectory accuracy against independently tracked particles;
- validation of an Eulerian advection-diffusion M0 forecast;
- calibrated horizontal diffusivity;
- M1 particle-class, biofouling or aggregation performance;
- a vertical water-column model, settling validation or seabed deposition.

The separate finite-volume transport engine in src/rheomarine_transport is a different implementation. Do not attribute its advection-diffusion capabilities to the K=0 Lagrangian pilot.

Minimum numerical verification before claiming the Eulerian solver is benchmarked:
- uniform-flow translation with analytic solution;
- solid-body rotation / periodic advection test where applicable;
- diffusion benchmark with known solution;
- finite-volume mass budget under closed boundaries;
- time-step and grid-refinement study;
- non-negative concentration and stability checks;
- explicit open-boundary and wet/dry/coastline treatment before coastal claims.

## 6. Evidence tiers and permitted wording

| Evidence | Endpoint | Status | Permitted wording |
|---|---|---|---|
| HFR IZOL/PIRA/integrated network | Near-surface horizontal forcing | Documented forcing; Tier D for particle validation | “QC-screened HFR surface-current forcing” |
| MAMBO acoustic current meter | In-situ current at instrument depth | Independent hydrodynamic candidate; access/overlap pending | “Potential independent current-field comparison, subject to data and depth compatibility” |
| OGS/NODC drifter records | Lagrangian trajectory | Open until matching deployment found | No validation claim |
| Gajšt et al. aggregate publication | Historical regional surface microplastic concentration | Tier C | “Historical regional benchmark” |
| Gajšt sample-level records | Concentration/spatial distribution | Blocked; accessibility unverified | No pointwise validation claim |
| DS1/DS2 laboratory datasets | Laboratory settling/rheology | Tier D for field validation | “Laboratory process evidence / proxy” |
| Synthetic release pilot | Numerical path/QC behaviour | Numerical verification only | “Computational transport/QC pilot” |

## 7. Immediate requests

**OGS / ARPA FVG:** MAMBO buoy locations and deployment dates; acoustic current-meter make/model, measurement depth/volume, raw/QC time series, interval, uncertainty and access terms; any archived surface-drifter deployments overlapping the HFR window.

**NIB / ARSO:** integrated four-station total-vector HFR product; station-level QC/coverage metadata; calibration history for IZOL/PIRA; recommended QC policy and appropriate product for the Slovenian territorial footprint.

**Gajšt et al. authors / data holders:** sample-level metadata listed in Section 3, not merely a map or published mean.

## 8. Next analysis after data access

1. Freeze one pilot time window based on actual valid integrated HFR coverage.
2. Freeze a contiguous spatial polygon using predeclared coverage/continuity thresholds.
3. Compare HFR with contemporaneous MAMBO observations at matched times, explicitly accounting for the 10 m versus upper-0.3–2.5 m depth mismatch.
4. If a compatible surface-drifter dataset exists, compute trajectory separation with predeclared metrics.
5. Compare microplastic concentrations only if sample-level Gajšt data and compatible support are recovered; otherwise report historical context only.
6. Separate calibration and evaluation observations.
7. Publish unavailable data and blocked steps explicitly.

## Audit limitation

This is a source and evidence audit, not a reanalysis of raw HFR, MAMBO, drifter or microplastic sample files. No unverified raw data have been treated as accessed.
