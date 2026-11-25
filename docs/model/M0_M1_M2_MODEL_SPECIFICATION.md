# RheoMarine-SLO — M0/M1/M2 model specification

**Status:** scientific and computational specification; implementation must be reconciled with the HFR integration and the available datasets before being treated as executable.
**Project horizon:** 8 months. **Decision gate:** M4 for M2.
**Scope:** surface transport and evidence-constrained particle settling in a selected Slovenian coastal pilot area.

## 1. Purpose and modelling question

The model comparison asks whether particle-specific properties and biological conditioning add predictive skill beyond a conventional surface-transport baseline forced by observed high-frequency radar (HFR) currents.

The comparison is staged:
- **M0:** surface advection–diffusion baseline with conventional, explicitly documented particle loss/settling assumptions.
- **M1:** particle classes and evidence-supported changes in effective properties, including biofouling/aggregation only where parameterized from defensible evidence.
- **M2:** optional rheological correction, activated only after the M4 evidence gate.

The model must be capable of returning a negative result: additional complexity is not retained unless it improves predeclared metrics on independent or held-out observations without unacceptable loss of robustness.

## 2. Domain, state variables and forcing

Let the horizontal pilot domain be \(\Omega\subset\mathbb R^2\), with time interval \([t_0,t_1]\). The primary prognostic variable is surface-layer particle concentration (or particle number per unit horizontal area) for class \(k\), denoted \(C_k(x,y,t)\).

HFR provides an observed estimate of the near-surface horizontal velocity field \(\mathbf u_{HFR}(x,y,t)\). It is a surface-current forcing, not a measurement of the full three-dimensional velocity field. Any gap filling, interpolation, filtering, temporal resampling or spatial mapping applied to HFR must be explicitly recorded with method, parameters, source timestamps and QC provenance.

Additional forcing may include wind and river/shoreline source scenarios only where suitable observations or defensible boundary data exist. Such terms must be labelled as measured, externally sourced, prescribed scenario, or unknown. Do not silently infer a river plume, beach source or vertical circulation from HFR alone.

The initial and boundary conditions must be recorded for every run. The pilot polygon and time window are selected only after HFR coverage/QC and the availability of compatible observations are assessed.

## 3. M0 — surface advection–diffusion baseline

For each particle class, a suitable depth-integrated surface-layer baseline is

\[
\frac{\partial C_k}{\partial t}
+\nabla_h\!\cdot(\mathbf u_{HFR} C_k)
=\nabla_h\!\cdot(\mathbf K_h\nabla_h C_k)
+S_k-L_k.
\]

Here:
- \(\mathbf K_h\) is a documented horizontal dispersion tensor (or a scalar \(K_h\) only if isotropy is an explicit simplifying assumption);
- \(S_k\) represents specified particle inputs, if any;
- \(L_k\) represents loss from the modelled surface layer, including a conventional settling/loss parameterization only where its meaning and units are explicit.

A simple first-order surface-layer loss may be written \(L_k=\lambda_k C_k\), where \(\lambda_k\) has units of inverse time. If a well-mixed surface layer of specified thickness \(h_s\) is assumed and a downward settling velocity \(w_{s,k}\) is justified, one possible closure is \(\lambda_k=w_{s,k}/h_s\). This is a model closure, not a direct HFR measurement; its validity depends on the layer definition and vertical-mixing assumptions. Do not use it to claim a resolved three-dimensional vertical flux or seabed deposition.

For a Lagrangian implementation, particles satisfy the horizontal stochastic transport equation

\[
d\mathbf X_i=\mathbf u_{HFR}(\mathbf X_i,t)dt
+\sqrt{2\mathbf K_h}\,d\mathbf W_i,
\]

with a documented boundary rule and particle removal/loss rule. The stochastic term must be implemented consistently with the chosen diffusion tensor and numerical scheme. The Eulerian and Lagrangian formulations are alternative representations; they must not be combined as if they were independent physical effects.

**M0 minimum outputs:** trajectories or concentration fields; particle count/mass bookkeeping; domain exit and surface-layer loss counts; coverage mask; run metadata; uncertainty/sensitivity results.

## 4. M1 — particle-specific effective properties and aggregation

M1 resolves a set of particle classes \(k\) defined by the available evidence. A class may include polymer/material, size interval, shape class and a documented effective density. Do not invent missing dimensions or treat polymer identity as a complete description of particle behaviour.

For each class, record at minimum:
- material/polymer label and source;
- size metric and units (length, equivalent diameter, or measured dimensions);
- shape/aspect-ratio descriptor where available;
- pristine polymer density and source;
- effective density or biofouling/aggregate state, with source and uncertainty;
- settling-velocity estimate, measurement conditions and calibration status.

Aggregation and biofouling are distinct state changes. If data support a transition model, represent class/state transitions with rates \(q_{k\to j}\) and document their units and evidence. Otherwise, run bounded scenarios rather than fitting unsupported rates. An aggregate must not be represented merely by changing density if its size, porosity or shape also changes and those properties are known to matter.

A generic multi-class equation is

\[
\frac{\partial C_k}{\partial t}
+\nabla_h\!\cdot(\mathbf u_{HFR} C_k)
=\nabla_h\!\cdot(\mathbf K_{h,k}\nabla_h C_k)
+S_k-L_k
+\sum_{j\ne k}q_{j\to k}C_j
-\sum_{j\ne k}q_{k\to j}C_k.
\]

This equation is a bookkeeping framework; it does not assert that all transition rates are known or that aggregation is first-order. Use only terms supported by data, and retain an M0-equivalent run with the same forcing and numerical setup for comparison.

Settling velocities may be measured or estimated using a physically appropriate drag regime. Stokes' law is admissible only after checking its assumptions (small particle Reynolds number, appropriate geometry and fluid rheology, negligible interactions and suitable boundary conditions). Non-spherical particles require a shape-aware treatment or empirical measurements. For polymer mixtures, weathered particles and aggregates, pristine bulk polymer density alone is insufficient.

### Existing experimental datasets: permitted use and caveats

- **DS1 (Mrokowska et al. 2024 dataset):** 722 particle-tracking trajectories across controlled aqueous solutions and particle types. The existing analysis estimates terminal speeds from the final 40% of trajectories. The vertical coordinate's absolute calibration is unresolved (dataset documentation indicates pixels); therefore do not present the derived values as absolute physical settling velocities until calibration is verified. Relative retardation ratios can be explored with this limitation explicitly attached. Dataset solution labels (including xanthan gum and κ-carrageenan) describe laboratory proxies, not natural marine EPS.
- **DS2 (Mrokowska et al. 2025 dataset):** stratified two-layer experiments. Current layer-order assignment is inferred from dataset description and velocity signatures; exact fluid recipes and an anomalous density profile remain open. Use as qualitative/mechanistic or sensitivity evidence only until these uncertainties are resolved. Do not transfer layer-specific numerical parameters directly to the sea.
- Dataset-derived parameters must retain experiment IDs, source files, extraction method, units, calibration status and uncertainty.

## 5. M2 — conditional rheological correction

M2 is not a default model. It is activated only if the project obtains rheological measurements or sufficiently documented published data for a medium and concentration range relevant to the proposed particle experiments.

Before implementing M2, document:
1. measured constitutive response and temperature/salinity/composition;
2. rheometer geometry, protocol, shear-rate range and uncertainty;
3. whether the medium is Newtonian, shear-thinning, viscoelastic or exhibits a yield stress over the relevant range;
4. the constitutive relation selected and its fitted parameter covariance;
5. evidence that the constitutive model is applicable to the particle scale and settling regime.

Do not select a Carreau, power-law, Herschel–Bulkley or viscoelastic model by assumption. Select only after inspecting measured flow curves and, where relevant, oscillatory measurements. Do not equate xanthan gum or κ-carrageenan solutions with natural EPS.

**M4 go/no-go:** retain M2 only if (a) relevant measurements or validated parameters exist, (b) the constitutive fit is identifiable over the relevant range, (c) the correction can be implemented with traceable units, and (d) the expected comparison is feasible within the project. Otherwise document why M2 is not activated.

## 6. Numerical and data-integrity requirements

Every simulation must record:
- code version/commit and configuration file;
- HFR source dataset, station(s), retrieval time, source URL/query and source-file checksum where available;
- QC policy and coverage statistics;
- time zone, timestamp convention, temporal resampling and treatment of missing values;
- coordinate reference system, grid and interpolation method;
- velocity units and conversion;
- particle class definitions, parameter source, units and uncertainty;
- domain polygon, boundary conditions, initial conditions and simulation period;
- numerical integrator, time step, diffusion implementation, random seed(s);
- particle number or concentration normalization and mass/number balance;
- output files and software environment.

Never silently convert units, fill missing HFR values, extrapolate outside radar coverage or treat a QC failure as a zero current. Keep raw, QC-filtered and model-ready data distinct. Preserve provenance from each model-ready field back to the source observation.

## 7. Model comparison and decision rule

M0, M1 and (if activated) M2 must be run over matched periods, domains, initial conditions and forcing wherever possible. Any unavoidable differences must be reported.

Additional complexity is considered useful only if it:
- improves a predeclared metric on independent or held-out observations;
- does not rely on tuning against the evaluation set;
- is robust to reasonable parameter perturbations;
- does not produce physically implausible mass/number balances or unsupported extrapolations.

If no compatible independent observations exist, report a process/sensitivity comparison, not validated predictive skill. In that case, model improvement remains unconfirmed.

## 8. Explicit non-claims

This specification does not claim:
- that HFR measures vertical circulation or seabed deposition;
- that surface concentration alone determines total water-column or sediment burden;
- that all marine water is non-Newtonian;
- that laboratory polymer solutions reproduce natural EPS;
- that the DS1/DS2 datasets provide direct field calibration;
- that historical Slovenian microplastic observations are present-day pilot-site truth;
- that M1 or M2 must outperform M0.

## 9. Implementation handoff

The HFR integration should expose a documented, stable interface supplying model-ready surface velocity fields plus QC/coverage masks and provenance metadata. This document deliberately does not prescribe Devin's file names or overwrite his implementation.

The transport implementation should consume that interface, keep physical parameters in a separate versioned configuration, and include unit tests for advection, diffusion, boundaries, settling/loss bookkeeping, class transitions and reproducibility. Any code-level deviation from this specification should be recorded here or in a linked implementation note.
