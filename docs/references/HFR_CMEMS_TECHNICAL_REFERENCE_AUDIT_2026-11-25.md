# HFR-NAdr and Copernicus Marine — technical reference audit

**Checked:** 25 November 2026  
**Repository:** RheoMarine  
**Purpose:** source-backed corrections for the RheoMarine-SLO presentation and data-request dossier.

## 1. HFR-NAdr: network specifications

The European HFR Node record identifies HFR-NAdr as a WERA network in the Gulf of Trieste, jointly owned/operated by OGS, NIB, ARSO and ARPA FVG. It lists four sites and their central frequencies:

| Site | Frequency |
|---|---:|
| AURI | 24.635 MHz |
| PIRA | 24.525 MHz |
| IZOL | 24.500 MHz |
| TRI1 | 24.525 MHz |

The network-level specifications are: 30-minute temporal averaging, 1.5 km spatial resolution, maximum radial coverage approximately 35–40 km, and surface-current measurements representative of the upper 0.3–2.5 m. The total-current combination history matters: totals used AURI and PIRA until 1 March 2023; IZOL was added on 1 March 2023 and TRI1 on 10 July 2023. Do not describe the four-site configuration as if all four stations contributed to total maps throughout the entire 2021–present record.

**Primary network record:** HFR Node, HFR-NAdr, DOI [10.57762/8RRE-0Z07](https://doi.org/10.57762/8RRE-0Z07).  
URL: https://www.hfrnode.eu/networks/hfr-nadr-2/

OGS independently describes the four-station WERA system, 24.5 MHz, 1.5 km and 30-minute resolution:
https://www.ogs.it/en/gulf-trieste-marine-observatory

### ERDDAP products and variables

The HFR Node ERDDAP exposes distinct radial products for AURI, PIRA, IZOL and TRI1, and a total-current product. The dataset metadata describe 30-minute averaging and the upper 0.3–2.5 m measurement layer. Example endpoints:

- Total velocity: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-Total_v3.html
- PIRA radial: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3.html
- IZOL radial: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.html
- TRI1 radial: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-TRI1_v3.html

The variables used in the RheoMarine data review must be described precisely:

- `EWCT`, `NSCT`: eastward and northward components of total surface current (m s⁻¹).
- `UACC`, `VACC`: uncertainty/standard-deviation information for the velocity components in the relevant product convention; they are **not** additional current components.
- `GDOP`: geometrical dilution of precision, a geometry-related quality indicator.
- `QCflag`: overall quality flag; interpret using the actual variable attributes (`flag_values`, `flag_meanings`) of the downloaded dataset/version. Do not assume identical semantics across products or software versions without checking metadata.

Radial datasets have radial velocity relative to the individual radar site; total maps are reconstructed from multiple radial observations. These are not interchangeable. For a reproducible analysis, retain radial inputs, total product, product version, timestamps, QC variables and global attributes.

**Important qualification:** 30 min / 1.5 km / 0.3–2.5 m are network-level product specifications, not a guarantee that every cell and timestamp is valid. Coverage, station contribution, GDOP and QC must be assessed for the selected polygon and period.

## 2. Literature: Mihanović et al. (2011)

Correct reference:

Mihanović, H., Cosoli, S., Vilibić, I., Ivanković, D., Dadić, V., & Gačić, M. (2011). “Surface current patterns in the northern Adriatic extracted from high-frequency radar data using self-organizing map analysis.” *Journal of Geophysical Research: Oceans*, 116, C08033. https://doi.org/10.1029/2011JC007104

The paper was first published on 26 August 2011. It analyses HF-radar observations from February–August 2008 collected in the NASCUM network, with three radars simultaneously operational during the analysed period. It is a regional scientific reference for circulation-pattern classification, not a technical description of the present HFR-NAdr four-station network.

Related HFR validation reference:

Cosoli, S., Mazzoldi, A., & Gačić, M. (2010). “Validation of Surface Current Measurements in the Northern Adriatic Sea from High-Frequency Radars.” *Journal of Atmospheric and Oceanic Technology*, 27(5), 908–919. https://doi.org/10.1175/2009JTECHO680.1

This paper compares HF-radar currents with a bottom-mounted ADCP in the Venice Lagoon coastal area (40-day period in August–September 2005). It supports the regional HFR validation rationale but is not a direct validation of the current HFR-NAdr deployment or the RheoMarine pilot.

## 3. Copernicus Marine: global current product

Product: `INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048`  
DOI: [10.48670/moi-00041](https://doi.org/10.48670/moi-00041)  
Description: https://data.marine.copernicus.eu/product/INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048/description  
PUM: https://documentation.marine.copernicus.eu/PUM/CMEMS-INS-PUM-013-048.pdf

The product contains distinct observation families/datasets:

1. **Drifters (DBCP / Global Drifter Program):** near-surface zonal and meridional velocities along drifting-buoy trajectories. The PUM specifies that drogued drifters represent approximately 15 m depth, while undrogued drifters are treated as surface drifters; wind-slippage correction and meteorological fields may also be supplied.
2. **HF radar:** total and radial surface-current datasets, with standard deviations, GDOP, QC variables and metadata.
3. **Argo:** velocities along float trajectories at the surface and parking depth.

These components must not be conflated. Argo floats are not surface drifters. HFR data are not independent validation if they reuse the same HFR-NAdr observations or source network used as forcing. Drifter effective depth and drogue state must be checked before comparing them with HFR currents representative of the upper 0.3–2.5 m.

The product-level global extent is not evidence of a platform in the pilot polygon or during the pilot dates. A spatial-temporal extraction and platform-level metadata check are required.

## 4. Copernicus Marine: Mediterranean NRT in-situ product

Product: `INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035`  
DOI: [10.48670/moi-00044](https://doi.org/10.48670/moi-00044)  
Description: https://data.marine.copernicus.eu/product/INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035/description  
Services: https://data.marine.copernicus.eu/product/INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035/services

The catalogue describes near-real-time, quality-controlled in-situ observations, distributed on average within 24–48 hours and updated several times daily. Listed variables include sea-water velocity speed/direction, significant wave height, wave period/direction, water-surface height, temperature and salinity. Feature types include trajectory, profile and point; distribution is NetCDF-4.

The catalogue's spatial and temporal extents describe the product as a whole. They do **not** establish that a current-measuring platform has observations in the RheoMarine pilot polygon and time window. The actual platform/dataset inventory, timestamps, coordinates, depths, variables and QC must be extracted.

## 5. Required platform-level query

For the pilot, query the relevant Copernicus datasets with:

- a documented bbox covering the selected IZOL/PIRA domain and a wider Gulf of Trieste context;
- the exact pilot interval (for the current seven-day subset: 2026-11-18 14:02 UTC to 2026-11-25 14:02 UTC);
- only datasets/platforms with relevant velocity/current variables for the hydrodynamic comparison;
- platform code/type, institution, timestamps, coordinates, depth, drogue/configuration where relevant, variables, QC and data mode.

A no-result query is a valid result. Do not infer local observations from catalogue extent.

## 6. Status wording for the project dossier

| Source | What is documented | What remains open |
|---|---|---|
| HFR-NAdr | Four WERA sites, frequencies, nominal 30-min / 1.5-km sampling, 0.3–2.5-m representative layer, DOI and ERDDAP access | Per-period coverage, cell validity, station contribution, calibration/maintenance history, independent accuracy for the pilot |
| CMEMS Global current NRT | Product and separate drifter/HFR/Argo components identified; PUM describes depth and variable conventions | Extract Gulf records; verify platform/time overlap and provenance; assess independence |
| CMEMS Mediterranean NRT | Product, variables, geometry types, delivery/update characteristics identified | Extract actual platform-level observations in pilot bbox/window and inspect depth/QC |
| Mihanović et al. | Regional HFR circulation-pattern study, 2011 | Do not use as current HFR-NAdr network specification |
| Cosoli et al. | Regional HFR–ADCP validation study, 2010 | Not a direct validation of the current HFR-NAdr system or RheoMarine pilot |

## 7. References

1. HFR Node. *HFR-NAdr – HF Radar Network*. DOI: https://doi.org/10.57762/8RRE-0Z07.
2. OGS. *Gulf of Trieste marine observatory*. https://www.ogs.it/en/gulf-trieste-marine-observatory.
3. Mihanović, H., Cosoli, S., Vilibić, I., Ivanković, D., Dadić, V., & Gačić, M. (2011). *Surface current patterns in the northern Adriatic extracted from high-frequency radar data using self-organizing map analysis*. JGR: Oceans, 116, C08033. https://doi.org/10.1029/2011JC007104.
4. Cosoli, S., Mazzoldi, A., & Gačić, M. (2010). *Validation of Surface Current Measurements in the Northern Adriatic Sea from High-Frequency Radars*. JTECH, 27(5), 908–919. https://doi.org/10.1175/2009JTECHO680.1.
5. Copernicus Marine. *Global Ocean – in-situ Near Real Time Observations of Ocean Currents*. INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048. DOI: https://doi.org/10.48670/moi-00041.
6. Copernicus Marine. *Product User Manual for INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048*. Issue 2.6, November 2025. https://documentation.marine.copernicus.eu/PUM/CMEMS-INS-PUM-013-048.pdf.
7. Copernicus Marine. *Mediterranean Sea – In-Situ Near Real Time Observations*. INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035. DOI: https://doi.org/10.48670/moi-00044.

---
**Evidence boundary:** this document verifies public network/product metadata and bibliographic records. It does not claim that a Copernicus subset has been downloaded, that local platforms have been inventoried, or that independent validation has been completed.
