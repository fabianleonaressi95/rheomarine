# RheoMarine-SLO — independent validation and uncertainty protocol

**Status:** protocol specification for the 8-month pilot; dataset availability and final metrics remain conditional on the M1 data audit.
**Purpose:** prevent circular validation and distinguish model verification, calibration, observational comparison and independent validation.

## 1. Validation principles

1. HFR currents used to force the transport model are not, by themselves, independent validation of the resulting particle trajectories or concentrations.
2. The observation must measure the same quantity as the model output. Concentration data validate concentration predictions; tracked drifters or equivalent trajectory observations validate trajectories; settling-column measurements validate settling parameters under their laboratory conditions.
3. Separate data used for parameter estimation/calibration from data used for evaluation. Record the split before model tuning.
4. Match spatial footprint, depth/surface layer, size cutoff, sampling gear, time window and units before comparing observations.
5. If suitable independent data cannot be obtained, report the model as unvalidated for the affected endpoint. Do not replace validation with visual map agreement.

## 2. Evidence tiers

| Tier | Evidence | Permitted claim |
|---|---|---|
| A | Independent, contemporaneous observations in or close to the pilot area, with metadata and compatible measurement support | Independent validation for the matched endpoint |
| B | Independent regional observations with documented method and partial spatial/temporal mismatch | Regional comparison or external plausibility check, not direct pilot validation |
| C | Historical observations with incomplete metadata or uncertain compatibility | Contextual benchmark only |
| D | Model-forcing data, calibration data, laboratory proxy data, or simulated outputs | Forcing/calibration/process evidence; not independent field validation |

Classify each dataset and endpoint separately. A single dataset may be Tier A for one question and Tier C for another.

## 3. Candidate observations and present limitations

### 3.1 Slovenian surface microplastics

Gajšt et al. (2016), *Sea surface microplastics in Slovenian part of the Northern Adriatic*, is the most geographically relevant historical field reference identified so far. The published article reports 17 surface trawls over a 20-month period, using a 300 μm epineuston net, and a mean concentration of 406,000 particles km⁻² (approximately 5.41 particles m⁻³ as reported by the paper). This is a historical regional benchmark, not a present-day measurement of the selected IZOL/KOPER/PIRAN pilot polygon.

Before quantitative use, seek the original sampling coordinates, dates, tow tracks, sample-level counts, size distribution, blank/correction protocol, filtered area or volume and analytical metadata. Without these, use as Tier C context only. Do not infer sample-level space-time fields from the published mean.

Marchetto et al. (2022) sampled the Venice Lagoon inlet area, not the Slovenian coast. It is a regional process/context reference and not direct validation for the Slovenian pilot. Its comparison table cites Slovenian observations; cite Gajšt et al. directly for those data and keep the two publications' reported averages distinct.

### 3.2 HFR currents

HFR is the hydrodynamic forcing source. Comparison with ADCP or drifter observations, if accessible and contemporaneous, can evaluate the velocity field itself. Such comparison validates the current product, not the microplastic transport model unless an independent particle endpoint is also observed.

### 3.3 Laboratory settling and rheology

DS1 and DS2 are controlled laboratory datasets. They can support parameter extraction, process-model testing and sensitivity scenarios. They are not independent field validation of the coastal transport model. DS1's absolute vertical scale must be resolved before using extracted speeds in physical units. DS2's fluid recipes/layer assignment and density anomaly must be resolved before quantitative transfer.

## 4. Predeclared metrics

Choose metrics only after the endpoint and observation support are established.

### Concentration

For paired observed/predicted concentrations \(O_i,P_i\), report:
- mean absolute error: \(MAE=n^{-1}\sum_i|P_i-O_i|\);
- root mean square error: \(RMSE=\sqrt{n^{-1}\sum_i(P_i-O_i)^2}\);
- mean bias: \(Bias=n^{-1}\sum_i(P_i-O_i)\);
- normalized metrics only where the denominator is meaningful and nonzero.

Report units, sample count, detection limits, treatment of zeros/non-detects and uncertainty intervals. Do not pool incompatible size fractions or sampling methods.

### Spatial distribution

Where observation geometry supports it, compare:
- distance between observed and predicted accumulation centroids;
- overlap or skill scores for predeclared accumulation regions;
- spatially blocked residuals and maps of data support.

Do not compute a spatial skill score from a single regional mean or sparse observations with no defensible spatial interpolation.

### Trajectories

For independently observed trajectories, report time-matched separation distance and, where appropriate, along-track/cross-track errors. State drifter/particle type, drogue depth, sampling interval and temporal interpolation. Do not use concentration observations as a proxy for trajectory truth.

### Settling and surface residence

Use laboratory settling observations to evaluate settling parameterizations only under matched fluid, temperature, salinity, particle and geometry conditions. In field simulations, report modelled loss from the defined surface layer as a model diagnostic, not measured seabed deposition. Define residence time operationally (domain exit, surface-layer loss or other event) and do not conflate these outcomes.

## 5. Calibration/evaluation design

Preferred hierarchy:
1. independent contemporaneous pilot-area dataset, if obtained;
2. otherwise, spatially or temporally held-out observations from a compatible dataset;
3. otherwise, regional/historical comparison with explicit Tier B/C classification and no claim of independent pilot validation.

Do not randomly split individual samples when observations are spatially or temporally clustered. Prefer leave-one-period-out, leave-one-station/sector-out or spatial block holdout, provided sample size permits. Freeze the evaluation split before parameter tuning. If data are too sparse for a defensible split, avoid tuning and report scenario ranges.

## 6. Sensitivity and uncertainty

At minimum, assess sensitivity to:
- HFR temporal gaps, QC policy and interpolation/resampling choices;
- spatial mapping/interpolation and radar coverage mask;
- horizontal diffusivity and stochastic realization;
- initial particle distribution and boundary/source assumptions;
- particle size, density, shape and settling velocity;
- aggregation/biofouling parameters where supported;
- time step, integration scheme and random seed.

Use ensembles or structured parameter sweeps where computationally feasible. Report distributions or intervals, not only a single preferred run. Distinguish observational uncertainty, parameter uncertainty, forcing uncertainty and numerical variability.

## 7. Model-comparison rule: M0 versus M1 versus M2

Run configurations on matched periods, domains, initial conditions and forcing wherever possible.

- M1 adds value only if it improves a predeclared endpoint on independent/held-out observations or, where field validation is unavailable, demonstrates a clearly identified process effect without being described as improved predictive skill.
- M2 is activated only after the M4 evidence gate and evaluated separately from M1 where possible, so the rheological contribution is identifiable.
- Complexity is not rewarded by default. If improvements are smaller than observational/ensemble uncertainty, or are not robust to reasonable parameter changes, report no demonstrated improvement.
- If no independent particle observations exist, the correct conclusion is “comparative process/sensitivity assessment; predictive improvement not independently validated.”

## 8. Minimum M1 data-readiness checklist

- [ ] Pilot polygon and time window selected from actual HFR QC/coverage.
- [ ] HFR forcing and independent validation sources explicitly separated.
- [ ] Candidate particle observations classified by evidence tier.
- [ ] Sampling method, mesh, size range, units and spatial/temporal support recorded.
- [ ] Original Gajšt et al. sample-level data requested or documented as unavailable.
- [ ] DS1 absolute vertical calibration status resolved or speeds restricted to relative comparisons.
- [ ] DS2 fluid recipes/layer assignment and density anomaly reviewed or dataset restricted to qualitative use.
- [ ] Calibration and evaluation data split frozen before tuning.
- [ ] Metrics and uncertainty reporting defined for each endpoint.
- [ ] Any endpoint without independent data labelled unvalidated.

## 9. Reporting language

Use:
- “evaluated against” only when an actual comparison was performed;
- “independently validated” only for a genuinely independent, compatible observation set;
- “regional benchmark” for historical or geographically mismatched observations;
- “sensitivity analysis” for scenario sweeps without observational validation;
- “modelled surface-layer loss” rather than “measured seabed deposition”;
- “laboratory proxy” rather than “natural EPS analogue” unless compositional equivalence is demonstrated.
