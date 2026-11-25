# Priority literature review for RheoMarine-SLO
**Prepared:** 25 November 2026  
**Purpose:** scientific basis for the RISTANC v5 proposal and the 26 November OGS discussion.  
**Scope:** critical synthesis of the ten technical priority readings completed in the first pass, with Marchetto et al. (2022) retained as an additional priority local-field study in the verified bibliography and queued for the next full-text reading pass. This is not a claim that every publisher full text was accessible.

## Executive synthesis

The literature supports a staged project in which (i) high-frequency radar (HFR) observations provide a measured surface-transport baseline, (ii) particle settling and biological aggregation are constrained by independently measured particle/fluid properties, and (iii) rheological corrections are introduced only where laboratory evidence justifies them.

Three conclusions are especially important.

1. **HFR is a surface-current observing system, not a complete three-dimensional circulation or seabed-deposition model.** Its accuracy, coverage and representativeness vary with geometry, sea state, wind, vertical shear, QC and time. A pilot area must therefore be selected from the actual usable data, not from nominal station coverage alone.
2. **Lagrangian particle tracking is sensitive to its forcing and numerical choices.** Hydrodynamic errors, spatial/temporal resolution, stochastic parameterization, settling velocity and coastal boundary treatment can materially alter trajectories. Model output must be validated independently and uncertainty reported.
3. **Rheology can modify microplastic settling and orientation under particular polymer-rich or stratified experimental conditions.** The available studies use controlled xanthan-gum/carrageenan systems as proxies; these are not equivalent to natural EPS or proof that ordinary seawater is generally non-Newtonian. Rheological effects should remain a conditional module, gated by measured samples and laboratory evidence.

These points support the current M0/M1/M2 design: M0 hydrodynamic baseline; M1 independently evidenced biological aggregation/effective particle properties; M2 conditional rheological correction, with a go/no-go decision at M4.

## 1. HFR observations and North Adriatic circulation

### 1.1 Cosoli et al. (2010): validation of coastal HFR currents

**Verified reference:** Cosoli, S., Mazzoldi, A., & Gačić, M. (2010). *Validation of Surface Current Measurements in the Northern Adriatic Sea from High-Frequency Radars*. Journal of Atmospheric and Oceanic Technology, 27(5), 908–919. DOI: [10.1175/2009JTECHO680.1](https://doi.org/10.1175/2009JTECHO680.1). The title, authors, journal, volume, issue, pages and DOI match the [American Meteorological Society publisher record](https://journals.ametsoc.org/view/journals/atot/27/5/2009jtecho680_1.xml).  
**Full text consulted:** [OGS repository PDF](https://ricerca.ogs.it/retrieve/a5d78ee5-101e-4863-b5a9-69063bc6177f/1520-0426-2009jtecho680_1.pdf).

The study concerns the coastal area offshore of the Venice Lagoon, not the Gulf of Trieste. It compares HFR currents representative of approximately the first metre of the water column with ADCP measurements at about 2.5 m during a 40-day deployment in August–October 2005. Depending on radar site and antenna-pattern treatment, radial RMS differences span approximately 8.4–20.5 cm/s; the surface-vector comparison reports vector correlation up to 0.78 and a veering angle of about 6 degrees. The authors estimate that wind-driven shear can explain a substantial fraction of the surface–subsurface mismatch. Strong northeasterly wind pulses also degrade radar coverage and can produce substantial current underestimation, reported up to about 50%.

**Use for RheoMarine:** this is a warning against treating HFR vectors as error-free or vertically representative. The numerical error values are specific to the 2005 configuration and cannot be transferred as a calibration claim to the present IZOL/PIRA data. The project should report QC-filtered coverage, compare only genuinely collocated/temporally compatible observations, and separate measurement error from vertical representativeness.

### 1.2 Cosoli et al. (2013): Gulf of Trieste circulation

**Reference:** Cosoli, S. et al. (2013), *Surface circulation in the Gulf of Trieste (Northern Adriatic Sea) from high-frequency radar observations*, Journal of Geophysical Research: Oceans, DOI [10.1002/2013JC009261](https://doi.org/10.1002/2013JC009261).  
**Full text consulted:** [NIB-hosted PDF](https://www.nib.si/mbp/images/pdf/vlado-malacic-publications/cosoli_et_all_jgr_2013.pdf).

The analysis uses hourly HFR surface-current observations from March 2011 to October 2012 at approximately 1.5 km resolution. Temporal coverage was around 80% over much of the Gulf, with a maximum near 86% at an individual grid point. The study also used distance-weighted interpolation to fill spatial gaps; consequently, reported coverage must not be interpreted as meaning every value was a direct radar observation. The circulation is shaped by wind, tides, seasonal thermohaline processes and freshwater input, including the Isonzo/Soča. Model comparisons captured broad circulation features but did not reproduce all observed variability, including aspects of inertial/diurnal variability and stratification-related behaviour.

**Use for RheoMarine:** the Gulf is dynamically heterogeneous; a single uniform forcing assumption is not justified. Preserve flags distinguishing observed, interpolated, missing and rejected cells. Treat river discharge and wind as relevant contextual forcings where data are available. Do not describe gap-filled fields as direct observations.

### 1.3 HFR-NAdr network metadata

**Network record:** [HFR-NAdr](https://www.hfrnode.eu/networks/hfr-nadr-2/), DOI [10.57762/8RRE-0Z07](https://doi.org/10.57762/8RRE-0Z07).

The network metadata identify WERA stations AURI, PIRA, IZOL and TRI1, nominal 30-minute products, approximately 1.5 km spatial resolution and a representative surface layer of roughly 0.3–2.5 m. The network geometry changed over time: AURI and PIRA are listed through 1 March 2023; IZOL was added on 1 March 2023; TRI1 on 10 July 2023.

**Use for RheoMarine:** station availability and geometry must be time-indexed. A coverage map or time series that ignores station commissioning dates risks comparing unlike observing systems. These nominal specifications do not establish the actual usable coverage in the selected project period; that must come from the QC audit.

## 2. HFR-driven particle tracking and validation

### 2.1 Capodici et al. (2024): HFR and microplastic hotspot detection

**Reference:** Capodici, F. et al. (2024), *…* [publisher record](https://doi.org/10.1016/j.marpolbul.2024.117237).  
**Full text consulted:** [open author/institutional PDF](https://iris.unipa.it/retrieve/5320ce7d-620b-448e-90a1-1ddbdcd7bfd7/capodici_etal2024.pdf).

The study combines two 2018/2019 sampling campaigns (manta net, 300 μm mesh) with CALYPSO HFR fields. Turbulent kinetic energy showed a stronger association with total microplastics than eddy kinetic energy (reported R² around 0.70 versus 0.40); the association was particularly strong for fragments (TKE R² around 0.85, p=.0084). HFR-forced TrackMPD trajectories were released three hours before sampling and integrated for three hours; the reported relationship between observed fragments and tracked particles was high (R² around 0.88). In contrast, CMS-forced tracking performed poorly in most sampling periods (one period showed moderate agreement; another reported relationship was near zero).

The key regression sample was small (six observations), and the results are site- and campaign-specific. Correlation does not establish causality or a universal predictive relationship between turbulence and plastic abundance.

**Use for RheoMarine:** this is a relevant precedent for pairing HFR forcing with independent in-situ sampling and testing Eulerian (TKE/EKE) and Lagrangian indicators. It does not justify promising equivalent predictive skill in Slovenian waters. The proposal should describe the method as a testable workflow and define independent validation before model tuning.

### 2.2 Garnier et al. (2025): good practice in coastal particle tracking

**Reference:** Garnier, R. et al. (2025), *Particle tracking modelling in coastal marine environments: recommendations for good practice*, Ecological Modelling 501, 110999, DOI [10.1016/j.ecolmodel.2024.110999](https://doi.org/10.1016/j.ecolmodel.2024.110999).  
**Source consulted:** [Bangor University research record](https://research.bangor.ac.uk/en/publications/particle-tracking-modelling-in-coastal-marine-environments-recomm/). The accepted manuscript link was identified, but the full manuscript could not be retrieved during this review; the synthesis here is limited to the accessible record/abstract.

The paper highlights sensitivity to hydrodynamic forcing accuracy, particle-tracking resolution, stochasticity, behavioural parameterization (including settling speed), differences between tracking implementations and treatment of coastal land boundaries. Boundary handling can significantly affect trajectories.

**Use for RheoMarine:** document the integration timestep, interpolation, release protocol, beaching/reflection/absorption rules, horizontal diffusion, settling parameterization and ensemble design. Conduct sensitivity tests rather than selecting a single convenient parameter set. Record software/version and configuration for reproducibility.

## 3. Rheology, settling and stratified systems

### 3.1 Mrokowska & Krztoń-Maziopa (2024): rheological effects on settling

**Reference:** Mrokowska, M. M. & Krztoń-Maziopa, A. (2024), *Science of the Total Environment* 912, 168767, DOI [10.1016/j.scitotenv.2023.168767](https://doi.org/10.1016/j.scitotenv.2023.168767).  
**Sources consulted:** [PubMed record](https://pubmed.ncbi.nlm.nih.gov/38008323/) and [publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0048969723073953). Full article text was not accessible in this review; interpretation is limited to the abstract/highlights and associated experimental data where available.

The reported findings indicate that EPS-like polymer solutions can form gel-like three-dimensional structures with distinct rheological properties. Their addition reduces sinking velocity and can alter particle orientation; normal stresses in polymer-rich solutions are reported to favour more vertical particle orientation.

**Use for RheoMarine:** this motivates measuring fluid rheology and particle orientation rather than assuming a constant Newtonian settling law. It does not establish the prevalence, concentration or rheological properties of natural EPS in the Slovenian pilot area. Those must be measured or obtained from a suitable independent source.

### 3.2 Mrokowska et al. (2025): rheologically stratified seawater

**Reference:** Mrokowska, M. M. et al. (2025), *Water Research* 280, 123487, DOI [10.1016/j.watres.2025.123487](https://doi.org/10.1016/j.watres.2025.123487).  
**Sources consulted:** [PubMed record](https://pubmed.ncbi.nlm.nih.gov/40120384/), [publisher record](https://www.sciencedirect.com/science/article/pii/S0043135425004002), and the associated [Mendeley dataset](https://data.mendeley.com/datasets/ccm9k8pjft/1). Full article text was not accessible in this review; claims are restricted to accessible highlights and dataset metadata.

The study reports that EPS-rich layers can increase particle residence time and induce reorientation. The effect is linked to the viscosity contrast between Newtonian and non-Newtonian layers and is reported to be stronger than the effect attributable to density stratification in the tested configurations.

The dataset describes nine two-layer experiments using artificial seawater and xanthan-gum dispersion, with POM/PET spheres, disks and rods smaller than 5 mm; six configurations place the xanthan layer above artificial seawater and three reverse the order. Particle tracking velocimetry and rheological measurements are included.

**Use for RheoMarine:** the study supports a conditional interface/stratification experiment and sensitivity analysis. It does not support assuming that the same effect occurs in the field without evidence of comparable rheological contrasts and layer structure.

### 3.3 Mrokowska & Krztoń-Maziopa (2024): experimental dataset and methods

**Reference:** Mrokowska, M. M. & Krztoń-Maziopa, A. (2024), *Data in Brief* 53, 110101, DOI [10.1016/j.dib.2024.110101](https://doi.org/10.1016/j.dib.2024.110101).  
**Full text consulted:** [PubMed Central full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10867605/).  
**Dataset:** [Mendeley Data, version 2](https://data.mendeley.com/datasets/pb7fjnwcw4/2).

The dataset includes 15 microplastic particle groups, including PS, POM, PET and PA6, with spherical, disk-like, rod-like, blade-like and irregular geometries. The fluids include artificial seawater (3.5% salinity), xanthan gum, κ-carrageenan and mixtures at controlled concentrations (including 0.5 and 1 g/L). The experimental setup includes a 0.5 m tank, video tracking, particle tracking/shadowgraphy and rheometric measurements. The rheology protocol includes flow curves, normal-stress measurements, oscillatory amplitude sweeps and gelation-time characterization.

**Use for RheoMarine:** this is a valuable reproducibility/benchmark resource for the user's existing DS1 analysis. It permits testing how material, shape, size and polymer solution interact. The polymer solutions are controlled laboratory surrogates, not natural marine EPS; absolute settling-speed transfer to field conditions requires calibration and dimensional/unit checks.

### 3.4 Mrokowska et al. (2025): stratification dataset

**Dataset:** [Microplastics sinking through rheological stratification, Mendeley Data](https://data.mendeley.com/datasets/ccm9k8pjft/1); [IG PAS data portal](https://dataportal.igf.edu.pl/dataset/microplastics-sinking-through-rheological-stratification). Metadata specify CC BY 4.0 and provide tabular and video data.

This dataset is distinct from the homogeneous-fluid dataset above: it focuses on two-layer systems and transit across an interface. It contains nine experiments and supporting density, refractive-index and rheological measurements. It is suitable for checking interface-crossing behaviour, but dataset metadata alone do not resolve every experimental recipe or justify field extrapolation.

**Use for RheoMarine:** keep DS2 analysis separate from DS1 homogeneous-fluid analysis. Explicitly distinguish the interface zone from the lower-layer reference window and avoid treating a lower-layer window as a replicate of the interface transit.

## 4. Additional high-value North Adriatic references

These were identified during the review and are recommended for the next reading pass because they directly address the local hydrodynamic setting:

- Lorente, P. et al. (2022), *Coastal high-frequency radars in the Mediterranean – Part 1: Status of operations and a framework for future development*, Ocean Science 18, 761–795. [Full text](https://os.copernicus.org/articles/18/761/2022/os-18-761-2022.pdf), DOI [10.5194/os-18-761-2022](https://doi.org/10.5194/os-18-761-2022). Useful for HFR data quality, coverage, validation, harmonization and network limitations.
- Lombardo, A. et al. (2025), *Influence of wind stress and the Isonzo/Soča River outflow on surface currents in the Gulf of Trieste*, Ocean Science 21, 2197–2214. [DOI/full text](https://doi.org/10.5194/os-21-2197-2025). Highly relevant to local wind and river forcing.
- Flora, M. et al. (2025), *Comparing an idealized deterministic–stochastic model (SUP model, version 1) of the tide- and wind-driven sea surface currents in the Gulf of Trieste to high-frequency radar observations*, Geoscientific Model Development 18, 4685–4712. [DOI/full text](https://doi.org/10.5194/gmd-18-4685-2025). Relevant as a local model-versus-HFR comparison.

These three papers have been identified but are not represented as fully reviewed in this document.

### 4.1 Marchetto et al. (2022): local microplastic field evidence — priority reading

**Verified reference:** Marchetto, D., de Ferri, L., Latella, A., & Pojana, G. (2022). *Micro- and mesoplastics in sea surface water from a Northern Adriatic coastal area*. Environmental Science and Pollution Research, 29(25), 37471–37497. DOI: [10.1007/s11356-021-17874-9](https://doi.org/10.1007/s11356-021-17874-9).

This paper is explicitly marked as a priority reading in the verified Appendix B. It is retained in the priority list because it provides geographically relevant field evidence on micro- and mesoplastics in Northern Adriatic surface waters. It was not part of the ten-paper first-pass full-text/abstract synthesis above; its detailed sampling design, analytical methods, particle-size classes, spatial/temporal representativeness and reported concentrations must be extracted from the article before using numerical findings in the proposal. No quantitative result from this paper is asserted here.

## 5. Consequences for the RheoMarine-SLO work plan

| Work element | Literature-based requirement | Practical implication |
|---|---|---|
| WP1 / M0: HFR baseline | HFR is surface-representative; coverage and errors vary in space and time | Select pilot only after QC-aware coverage analysis; retain observed/interpolated/missing/rejected flags |
| Hydrodynamic forcing | Wind, river discharge, tides and stratification influence Gulf circulation | Use available independent forcing/context data; record missing forcings explicitly |
| Particle tracking | Trajectories depend on forcing, resolution, stochasticity, settling and boundaries | Fix and document numerical configuration; run sensitivity/ensemble tests |
| WP2 / M1: biological aggregation | Effective particle properties need independent evidence | Separate measured/observed properties from assumed parameter values; document source and uncertainty |
| WP2 / M2: rheology | Polymer-rich laboratory systems show conditional effects | Measure samples if feasible; keep rheological correction behind an M4 go/no-go gate |
| WP3: validation | A model cannot validate itself against its own forcing | Reserve independent observations/datasets for validation; report RMSE/MAE and spatial/temporal coverage |
| WP4: interpretation | Laboratory proxies are not field equivalence | State transfer limitations and distinguish proof-of-concept from field-confirmed mechanisms |

### Recommended minimum model/validation record

For every run, archive: HFR source and time window; station geometry/version; QC rule and valid-data denominator; direct versus interpolated cells; temporal/spatial resolution; interpolation method; current-field uncertainty; release locations/times; particle number and ensemble seed; timestep; horizontal diffusion; settling/biofouling parameters and provenance; coastal boundary rule; beaching/resuspension assumptions; validation dataset kept independent of calibration; and evaluation metrics.

At minimum, report:
- HFR valid-data fraction by station, grid cell and time window, with missing and rejected values separated;
- trajectory sensitivity to timestep, diffusion, settling speed and boundary treatment;
- independent validation metrics (RMSE, MAE and spatial/temporal coverage);
- uncertainty intervals or ensemble spread, not only a single deterministic track;
- clear separation between surface transport, water-column settling and seabed deposition.

## 6. Explicit limitations and claims to avoid

1. The 2010 HFR validation statistics are historical, instrument/configuration-specific values, not present-day calibration coefficients for IZOL or PIRA.
2. Nominal HFR cadence/resolution and network membership do not guarantee usable observations at every time or grid cell.
3. HFR surface currents alone do not provide vertical circulation, vertical mixing, near-bed flow or direct seabed deposition.
4. The Capodici et al. relationships are based on a small number of field observations and should be treated as a methodological precedent, not a transferable predictive law.
5. The rheology studies use controlled polymer systems (including xanthan gum and carrageenan). They do not establish that natural EPS in the pilot area has the same rheology or concentration.
6. Do not describe ordinary seawater as generally non-Newtonian. Any non-Newtonian correction must be supported by measured sample rheology.
7. Do not claim an OGS/laboratory partnership, access to independent validation data, or field sampling authorization until confirmed.
8. Laboratory settling measurements cannot be transferred directly to field-scale deposition without dimensional calibration, fluid-property matching and a defensible transport model.

## 7. Recommended agenda for the OGS meeting (26 November 2026)

1. **Pilot area and HFR:** ask OGS to assess which coastal sub-area has sufficient QC-valid HFR coverage in the project window; confirm station/time-series caveats and whether independent current observations are available.
2. **Independent validation:** identify datasets that are independent of the HFR forcing and could validate particle transport or sampling-location predictions.
3. **Biological aggregation/EPS:** ask which measurements are feasible, what sample types and volumes are required, and what protocols/authorizations apply.
4. **Laboratory scope:** obtain a bounded quotation or indicative scope for particle/fluid characterization, rheology and settling tests; distinguish essential work from optional work.
5. **Rheology decision gate:** agree what measured evidence would justify adding a rheological correction, and what result would lead to retaining the Newtonian baseline.
6. **Future collaboration/funding:** discuss possible roles and future calls without representing any commitment as already secured.

## 8. Bibliography and access audit

| Reference | Access in this review | Main use |
|---|---|---|
| Cosoli et al. (2010) | Full text and publisher metadata | HFR validation, vertical shear, wind-related coverage/error; Venice Lagoon coastal area |
| Cosoli et al. (2013) | Full text | Gulf circulation, temporal coverage, interpolation, river/wind influence |
| HFR-NAdr network record | Network metadata | Station configuration and temporal changes |
| Capodici et al. (2024) | Full text | HFR-driven tracking and in-situ microplastic comparison |
| Garnier et al. (2025) | Abstract/institutional record; full manuscript not retrieved | Particle-tracking good practice |
| Mrokowska & Krztoń-Maziopa (2024), STOTEN | Abstract/highlights and associated dataset; full article not retrieved | Rheological influence on settling/orientation |
| Mrokowska et al. (2025), Water Research | Abstract/highlights and associated dataset; full article not retrieved | Rheological stratification |
| Mrokowska & Krztoń-Maziopa (2024), Data in Brief | Full text | Experimental design and DS1 dataset |
| Mrokowska et al. (2025), stratification dataset | Dataset metadata/data resource | DS2 experimental structure |
| HFR-NAdr network record | Metadata | Local network configuration |
| Marchetto et al. (2022) | Bibliographic metadata verified; full-text analysis pending | Northern Adriatic field evidence; retained as priority reading |

**Editorial note:** bibliographic metadata for Cosoli et al. (2010) have been reconciled against the publisher's primary record. The title previously used in this review was incorrect and has been replaced. Marchetto et al. (2022) remains a priority item because Appendix B marks it as such; it is explicitly identified above as pending detailed reading rather than being presented as already reviewed. The access audit distinguishes full-text reading from abstract/metadata-level consultation.
