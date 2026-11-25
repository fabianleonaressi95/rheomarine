# Independent observation comparison protocol

**Purpose:** define *before any data arrive* how external observations
will be compared with RheoMarine-SLO outputs, so that no comparison can
be retrofitted into a validation claim. Follows
`INDEPENDENT_VALIDATION_PROTOCOL.md` (tiers A–D) and the observational
contract in `OBSERVATIONAL_DATA_SCHEMA.md`.

**Golden rule:** a comparison is *independent validation* only when the
observation is contemporaneous, spatially/temporally compatible, and
traceable to a source that did not force or tune the model. Everything
else is labelled regional benchmark, plausibility check or sensitivity
analysis — per protocol §9 wording rules.

---

## A. Eulerian current comparison (HFR/ADCP/buoy vs model or vs HFR)

### A.1 Collocation

- **Spatial:** pair model/HFR grid cells with observations inside a
  declared search radius (default ≤ half the HFR cell diagonal, ~5 km,
  adjustable per instrument footprint). Report the collocation radius
  and the number of unpaired observations.
- **Temporal:** pair within a declared window (default ±30 min for
  HFR's ~30-min cadence; ±1 h acceptable if documented). Never
  interpolate observations to model times silently — interpolation, if
  used, is a reported processing step.
- **Depth:** compare only where depth compatibility is demonstrated.
  HFR effective depth ~1–2 m; ADCP bins below the surface mixed layer
  measure different water. Report the depth offset explicitly; a
  profile-vs-surface comparison is a *shear diagnostic*, not a
  same-observable validation.

### A.2 Metrics (predeclared)

For paired vectors (u_obs,v_obs) vs (u_mod,v_mod):

- vector RMSE: `sqrt(mean((u_m-u_o)^2 + (v_m-v_o)^2))`
- component bias and RMSE for u and v separately
- speed bias: `mean(|V_m| - |V_o|)` and speed RMSE
- directional error: circular statistics on direction differences,
  reported as median and 90th percentile (not mean of angles)
- complex correlation / magnitude-squared coherence where time series
  length permits
- coverage: fraction of model cells/times with ≥1 collocated
  observation — **report before interpreting any metric**

### A.3 QC and uncertainty

- Apply source QC flags as documented; rejected values are excluded
  with counts reported, never converted.
- Observation uncertainty (if stated) propagates into metric
  interpretation: skill smaller than combined uncertainty is reported
  as *not distinguishable*, not as success or failure.
- HFR-vs-ADCP comparison validates the **current product**; it does not
  validate particle transport unless an independent particle endpoint
  is also observed (protocol §3.2).

## B. Lagrangian drifter comparison

### B.1 Matching

- Match drifter release position to the model domain at deployment time;
  if outside, the trajectory is excluded with reason logged.
- Drifter type is mandatory metadata: **CODE** (drogued, current-following)
  vs **Stokes** (wind/wave-sensitive). They are never pooled; each is
  compared separately and the type is stated in every figure/table.

### B.2 Metrics

- **Separation distance** d(t) between observed and simulated positions
  at matched times (linear interpolation of the *model* trajectory to
  observation times is allowed and reported; observations are not
  interpolated).
- **Endpoint error** at last common time.
- **Along-track / cross-track** decomposition relative to the observed
  path.
- **Skill score** only if a meaningful baseline exists (e.g. persistence
  or free-drift); otherwise report raw errors.
- **Temporal coverage:** fraction of the drifter track inside the model
  domain and inside forcing coverage; tracks leaving the domain are
  censored, not extrapolated.

### B.3 Interpretation limits

- A drifter is a finite-size Lagrangian instrument with wind/wave
  slip — it is not a microplastic particle. Agreement validates the
  *surface transport pathway*, nothing about particle properties.
- ~48 h campaigns give event-scale validation only; no climatological
  claim.

## C. Environmental forcing (wind, waves, sea level)

- Wind/wave/sea-level data are **forcing context**, not current
  validation. They may explain *why* currents behaved as observed
  (e.g. Bora vs Sirocco regimes documented by NEREIDES) but agreement
  between modelled and observed wind is not evidence about currents.
- Use: stratify comparisons by forcing regime; interpret drifter
  CODE-vs-Stokes divergence via wind/wave records.

## D. Minimum requirements for an "independent validation" label

All of the following must hold; otherwise downgrade the label:

1. Observation source independent of the model and of the HFR forcing
   processing chain (or independence explicitly argued, e.g. different
   instrument principle).
2. Temporal overlap with the simulated window, documented.
3. Spatial overlap with the model domain, documented (collocation map).
4. Compatible observable: same quantity, comparable depth/support,
   stated units.
5. Traceable provenance: source dataset ID, retrieval date, licence,
   QC convention — per `OBSERVATIONAL_DATA_SCHEMA.md`.
6. Metrics computed with the predeclared definitions above; coverage
   reported.
7. Calibration/tuning separation preserved (protocol §5): evaluation
   data were not used to fit parameters.

If any item fails → the result is a *comparison*, *benchmark* or
*sensitivity analysis*, labelled accordingly.

## E. Safeguards (restated as binding rules)

- A regional historical benchmark (e.g. Gajšt et al. 2016 means) is
  **not** contemporaneous validation.
- A drifter trajectory is **not** interchangeable with an Eulerian
  current measurement.
- Surface currents do **not** validate vertical transport, settling or
  seabed deposition.
- The K=0 pilot does **not** validate diffusion or settling.
- Missing observations **cannot** be reconstructed from aggregate
  statistics (means, climatologies) — absence stays absence.
- **No validation claim is allowed without traceable independent
  observations**, per `INDEPENDENT_VALIDATION_PROTOCOL.md` §1 and §9.
