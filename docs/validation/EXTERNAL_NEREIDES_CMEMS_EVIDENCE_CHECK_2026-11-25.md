# External evidence check: NEREIDES and Copernicus in-situ candidates

**Date checked:** 25 November 2026  
**Purpose:** independently refine the availability and evidential status of OBS-01/02/03 in the HFR pilot validation gate.  
**Scope limitation:** catalogue and institutional metadata review only. No Copernicus account query, subset download, NEREIDES raw-track access, or new observational comparison was performed.

## Executive result

The current validation gate remains **NO-GO for an independent validation claim**. Two candidate descriptions should be sharpened:

1. **NEREIDES (OGS / ARPA FVG):** OGS confirms five 2025 releases and five additional releases planned at approximately bimonthly intervals, with the experiment expected to conclude by December 2026. This makes a late-2026 release plausible, but the public announcement does not provide exact release dates or trajectories. An overlap with 18–25 November 2026 is therefore **not established**.
2. **Copernicus INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048:** this product is a useful multi-source catalogue, but its components must be treated separately. The service page reports the drifter-history component through 30 September 2026 and the latest drifter component as 18 September–18 October 2026. On the metadata currently exposed, it does **not** demonstrate a drifter record overlapping the 18–25 November pilot window. Its radar-total/radial components are HF-radar observations and are not independent of an HFR forcing product if they originate from the same network.
3. **Copernicus INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035:** the product is updated several times daily and its catalogue temporal extent reaches 21–22 November 2026. It includes velocity, waves, sea level, temperature and salinity variables and trajectory/profile/point feature types. However, this catalogue-level evidence does not establish that a current-measuring platform exists inside the pilot bbox during 18–25 November. The product's actual platform inventory and observations must be queried before assigning a validation tier.

## 1. NEREIDES: what is confirmed and what is not

OGS's public announcement for the second year of the OGS–ARPA FVG joint drifter experiment states:
- five releases were carried out during 2025;
- five further releases were planned on a bimonthly basis;
- the activity was expected to conclude by December 2026;
- CODE and Stokes drifters show materially different dynamics;
- CODE drifters are more directly influenced by marine currents and less influenced by wind and waves;
- Stokes drifters respond jointly to currents, wind and waves, and their trajectories diverge from CODE trajectories.

**Implications for RheoMarine**
- Do not state that a November 2026 NEREIDES deployment exists until OGS/ARPA FVG supplies its release log.
- Request exact deployment/recovery timestamps, GPS tracks, drifter IDs and type, drogue/configuration, position-fix cadence, quality flags, wind/wave context, and processing details.
- Prioritise CODE tracks for a first surface-current comparison, subject to confirmation of their effective depth and configuration.
- Treat Stokes tracks as a separate combined-current/wind/wave response. They may be valuable for a later drift model, but they are not interchangeable with CODE tracks or direct current-meter observations.
- A 48-hour deployment (as described for the 2025 releases in the OGS/ARPA FVG press material) can support trajectory comparison only over the actual overlap; it cannot validate the entire seven-day window if no longer deployment exists.

**Tier:** OBS-01 remains *potential Tier A for current-field validation only if* a deployment overlaps the pilot in time and space, its tracks and metadata are shared, and its effective depth is compatible with the HFR measurement layer. Until then it remains a promising, unverified candidate.

## 2. Copernicus global current product: component-level interpretation

Product: INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048  
DOI: 10.48670/moi-00041

The product description identifies three distinct observation families:
- DBCP Global Drifter Program trajectories, with near-surface zonal/meridional velocities and wind-slippage correction information;
- European and US HF-radar total and radial current products, including quality/geometry metadata;
- Argo float velocities at parking depth and at the surface.

The service's data-access page exposes distinct components. At the time checked:
- Drifter, history: 2 June 1986–30 September 2026;
- Drifter, latest: 18 September–18 October 2026;
- Argo history is a separate component;
- radar-total and radar-radial are separate components.

**Implications**
- The catalogue does not currently establish a DBCP drifter observation in 18–25 November 2026. Do not list this product as a demonstrated contemporaneous drifter source for the pilot.
- It remains useful for historical regional drifter context, subject to extracting and checking the actual Gulf of Trieste records.
- The radar-total/radial datasets may be useful for product intercomparison and consistency checks, but they are not independent validation if they reuse the same HFR network or input observations as the RheoMarine forcing.
- Argo observations must not be treated as surface drifters: parking-depth and surface velocities have different measurement contexts and sampling characteristics.

**Tier recommendation:** keep OBS-03 at B/C pending a spatial-temporal extraction; for the November 2026 pilot window, downgrade its *demonstrated contemporaneous drifter overlap* to **not established**.

## 3. Copernicus Mediterranean NRT in-situ product

Product: INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035  
DOI: 10.48670/moi-00044

The product page reports:
- NRT observations distributed on average within 24–48 hours and updated several times per day;
- catalogue temporal extent reaching 21–22 November 2026 in the page snapshots checked;
- instantaneous temporal resolution;
- variables including sea-water velocity direction/speed, significant wave height, wave period/direction, sea level, temperature and salinity;
- feature types trajectory, profile and point;
- NetCDF-4 distribution.

This is a useful route to investigate for the pilot, but the product-level metadata is not proof of an ADCP, mooring, drifter or other current observation inside the pilot bbox. The exact dataset/platform inventory, timestamps, coordinates, depth and QC must be extracted.

**Required next query**
- spatial bbox covering the actual IZOL/PIRA pilot windows and a wider Gulf of Trieste context;
- time range 2026-11-18 through 2026-11-25 UTC;
- filter to velocity/current variables and platform types that actually measure currents;
- return platform code, platform type, institution, timestamp, coordinates, depth, variables, QC and data mode;
- retain a no-result outcome as a legitimate result; do not infer coverage from product extent.

**Tier recommendation:** retain OBS-02 as an unverified candidate. It should not be described as a confirmed independent contemporaneous observation until the query returns suitable records.

## 4. Minimum matching protocol once records are obtained

For fixed current meters:
- compare vector components only after checking coordinate convention, depth, temporal averaging and instrument QC;
- collocate in time and space with HFR, recording the matching radius and time tolerance;
- report vector bias, vector RMSE, speed error, directional error where speed is sufficient, correlation, sample count and coverage;
- do not compare a subsurface bin to surface HFR without explicitly reporting the vertical-separation/shear limitation.

For CODE drifters:
- compare trajectory-derived velocity over matched intervals with HFR velocity sampled along the track;
- account for position-fix interval, filtering and drifter effective depth;
- report trajectory separation and endpoint error separately from pointwise velocity statistics.

For Stokes drifters:
- keep results separate from CODE;
- do not attribute their full drift to ocean current alone;
- wind and wave contributions require an explicit model or separate analysis.

For Copernicus radar components:
- first establish network/provider provenance;
- if the product contains the same WERA observations used as forcing, classify it as product cross-check, not independent validation.

## 5. Decision and action list

| Candidate | What is now established | What remains necessary | Current decision |
|---|---|---|---|
| OGS/ARPA FVG NEREIDES | five 2025 releases; five further bimonthly releases planned through Dec 2026; CODE/Stokes are physically distinct | exact release log and raw tracks for 18–25 Nov 2026; full metadata | highest-priority request; overlap unverified |
| CMEMS global current NRT | separate drifter, Argo, radar-total and radar-radial components; drifter latest metadata ends 18 Oct 2026 | extract historic Gulf tracks; confirm any subsequent updates and provider provenance | no demonstrated Nov pilot drifter overlap |
| CMEMS Mediterranean NRT | product updated NRT; current/wave/sea-level variables; catalogue extends to 21–22 Nov 2026 | query actual platform observations in bbox/window and inspect QC/depth | unverified candidate, not validation evidence yet |

**Overall:** the conditional GO for a sensitivity pilot is unchanged. The evidence check does not upgrade the pilot to independent validation and does not create any observational result. It narrows the next data-acquisition work to (i) the NEREIDES release log/tracks and (ii) an actual platform-level CMEMS Mediterranean subset query.

## Sources checked

1. OGS, *The second year of joint experimentation between Arpa FVG and OGS is underway: new drifter releases to study the currents of the Gulf of Trieste*:  
   https://www.ogs.it/en/news/second-year-joint-experimentation-between-arpa-fvg-and-ogs-underway-new-drifter-releases-study
2. OGS / ARPA FVG press material (2025 release summary):  
   https://www.ogs.it/sites/default/files/Comunicato%20stampa.pdf
3. Copernicus Marine, Mediterranean Sea – In-Situ Near Real Time Observations:  
   https://data.marine.copernicus.eu/product/INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035/description
4. Copernicus Marine, Mediterranean NRT data access and component listing:  
   https://data.marine.copernicus.eu/product/INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035/services
5. Copernicus Marine, Global Ocean – in-situ Near Real Time observations of ocean currents:  
   https://data.marine.copernicus.eu/product/INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048/description
6. Copernicus Marine, global current NRT component listing and temporal coverage:  
   https://data.marine.copernicus.eu/product/INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048/services
7. Copernicus Marine Product User Manual, INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048, Issue 2.6, November 2025:  
   https://documentation.marine.copernicus.eu/PUM/CMEMS-INS-PUM-013-048.pdf
