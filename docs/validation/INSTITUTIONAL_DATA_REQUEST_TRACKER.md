# Institutional data-request tracker — NIB and ARSO/ARPA FVG

**Created:** 25 November 2026
**Status legend:** `prepared` → request drafted, not sent · `sent` →
transmitted, no reply · `acknowledged` → reply received, terms pending ·
`received` → data in hand · `unavailable` → institution declined or data
do not exist. **No response dates, permissions or availability are
assumed anywhere in this file.**

Companion documents:
`HFR_PILOT_SCIENTIFIC_VALIDATION_GATE_2026-11-25.md` (PR #7, pending
merge at time of writing) and `hfr_pilot_candidate_observations.csv`.

---

## NIB — National Institute of Biology, Marine Biology Station Piran

Contact route: institutional data request (already sent for the items
below marked *sent*). Do not send duplicate requests; append status here.

| ID | Item | Requested variables | Coverage expected | Status | Metadata still required | Intended use | Limitations / dependencies |
|----|------|--------------------|-------------------|--------|------------------------|--------------|----------------------------|
| NIB-01 | Seabed current profiler off Piran (ADCP, ~45.55N 13.55E, referenced in Giordano et al. 2024, BGO 65:741–742) | eastward/northward velocity profiles, bin depth, timestamps, QC | unknown — confirm operating period and whether it covers 2026-11-18→25 | **sent** | instrument model, mounting depth, bin size, blanking distance, sampling interval, depth range actually valid, QC convention, licence | Eulerian current comparison vs HFR (protocol A) and vs model | Subsurface measurements; near-surface bins typically unreliable — depth compatibility must be established before comparison; may not overlap pilot window |
| NIB-02 | "Vida" buoy (AWAC on seafloor ~22 m + CTD/fluorescence/O₂) | vertical current profiles, T/S, auxiliary channels | continuous telemetered; confirm operational status in window | **sent** | exact position, AWAC firmware/bin configuration, telemetry gaps, depth of valid bins | Eulerian profile comparison; stratification context for HFR-vs-profile shear | Same depth caveat; auxiliary channels secondary |
| NIB-03 | HF radar vector/radial observations (NIB operates HFR assets; TRI1/AURI are same HFR-NAdr network) | radial currents and/or official vector fields, QC flags, antenna geometry | NRT ongoing | **prepared** | which products exist beyond the ERDDAP NRT vectors already used; whether radial (non-interpolated) data are available; processing version | Cross-check of forcing QC; possible independent processing chain comparison | Same instrument family → **not independent validation** of the current field (Tier D); useful only for QC/provenance audit |
| NIB-04 | Gajšt et al. (2016) sample-level microplastic records — 17 epi-neuston trawls, Slovenian Trieste Bay, 20-month period (~2013–2014) | per-trawl date/time, tow track start/end, filtered area or volume, raw counts by size fraction, polymer ID, blanks/corrections | historical; no overlap with 2026 pilot | **sent** | coordinate datum, mesh size confirmation (300 µm), counting protocol, archived vs published values | Tier-C→B regional benchmark; possible comparison with published Markov-model study | No public repository found; if unavailable, endpoint stays Tier C and the published mean must not be used as a spatial field |

## ARSO / ARPA FVG — regional environmental agency (Friuli Venezia Giulia)

The OGS–ARPA FVG collaboration runs bi-monthly CODE/Stokes drifter
releases in the Gulf of Trieste (NEREIDES project; releases Dec-2024,
Mar-2025, then ~every 2 months through 2025–2026 — a Nov-2026 release is
plausible but **unverified**). ARPA FVG also operates the regional
meteorological/marine observing network used in the joint experiments.

| ID | Item | Requested variables | Coverage expected | Status | Metadata still required | Intended use | Limitations / dependencies |
|----|------|--------------------|-------------------|--------|------------------------|--------------|----------------------------|
| ARSO-01 | Oceanographic station inventory (ARPA FVG marine/coastal stations) | station list, coordinates, parameters, sampling intervals, archive period | regional network, multi-year | **prepared** | full station table, which parameters are quality-controlled, public vs restricted access | Candidate source of in-situ T/S/wave/level for forcing evaluation and context | Stations are coastal/fixed; likely no current profiles — treat as environmental forcing context, not current validation |
| ARSO-02 | Current measurements and vertical profiles held by ARPA FVG | any ADCP/current-meter series in the Gulf or N Adriatic | unknown | **prepared** | instrument locations, periods, access terms | Eulerian comparison candidates (protocol A) | ARPA FVG is primarily meteo/wave agency; current assets may be limited — expect mostly waves/level/wind |
| ARSO-03 | Waves, sea level and meteorological forcing | significant wave height, sea-level anomaly, wind speed/direction, pressure | continuous regional network | **prepared** | station list, archive format, temporal resolution, licence | Environmental-forcing context (protocol C) — **must not be used as current validation** | Wind/wave agreement ≠ current agreement; drifter type sensitivity (CODE vs Stokes) documented in OGS/ARPA reports |
| ARSO-04 | Drifter and inter-institutional observations (joint OGS releases) | GPS tracks, drogue type (CODE vs Stokes), deployment/recovery times, positions at native interval | ~48 h campaigns, ~bimonthly 2025–2026 | **prepared** (ARSO side; OGS side tracked under OBS-01) | whether a campaign overlaps 2026-11-18→25; track format; QC applied; drogue loss flags | Lagrangian comparison (protocol B) — the most promising Tier-A route | Tracks are short (~48 h); CODE vs Stokes respond differently to wind/waves — comparison must state drifter type; data not public |

## Cross-institutional dependencies

- NIB-04 (Gajšt data) is independent of the HFR/ADCP asks; it can proceed
  even if oceanographic requests stall.
- ARSO-04 depends on the OGS–ARPA FVG release schedule; a written
  confirmation of the 2026 campaign calendar is itself a deliverable.
- CMEMS INSITU_MED query (OBS-02 in the candidate CSV) requires only a
  free Copernicus Marine account — no institutional permission needed.
- If NIB-01/02 return "instrument not operational in window", the
  fallback is the bounded regional benchmark (MedSVP archive, Tier C)
  plus the sensitivity matrix already published — **not** a validation
  claim.
