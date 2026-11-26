# C6 — Applicant competence and evidence annex

**Applicant:** Fabian Leo Naressi  
**Project:** RheoMarine-SLO  
**Purpose:** Evidence supporting evaluation criterion C6 (competences and experience).  
**Status:** Evidence-based draft for applicant verification before submission.

## 1. Competence profile and fit to the assigned role

The applicant is an independent researcher whose documented formal education is in Italian literature and journalism/publishing culture. The applicant is **not** presented as a graduate or professional specialist in oceanography, marine chemistry, environmental engineering, laboratory rheometry or marine field sampling.

The relevant contribution to RheoMarine-SLO is the computational and analytical workstream: processing observational and experimental datasets; implementing and testing numerical methods; comparing model configurations; documenting data provenance, assumptions and uncertainty; and preparing reproducible technical outputs.

The strongest evidence for this role is not a generic skills statement. It is the project-specific computational work already present in the RheoMarine repository: two analyses of published microplastic-settling datasets and a first tested numerical transport baseline.

## 2. Formal education and communication experience

- **MA in Journalism and Publishing Culture**, University of Parma (2021; EQF level 7 as stated in the CV).
- **BA in Italian Literature**, University of Bologna (2018; EQF level 6 as stated in the CV).
- **Classical high-school diploma**, Liceo G. Leopardi–E. Majorana (2014).
- The current CV reports **13 published articles** across the listed editorial outlets. A selected bibliography or publication record should be attached so that the count and bibliographic details can be checked.
- Languages as stated in the CV: Italian (native), German B2, English B1 and French A2.

These qualifications support research communication, literature synthesis, technical writing and dissemination. They are not represented as formal training in marine science or numerical modelling.

## 3. Direct, project-specific computational evidence

| Evidence | Work completed and traceable artefacts | Competence demonstrated | Boundary of the claim |
|---|---|---|---|
| **E1 — DS1 experimental-trajectory analysis** | scripts/analyze_ds1_settling.py; data/ds1_rheology_settling/ds1_analysis_summary.json; analysis/POST_MERGE_AUDIT_2026-11-25.md. The source dataset contains 722 particle-tracking runs. The analysis derives settling metrics and compares material-specific ratios against artificial-seawater baselines. | Python-based data processing; numerical differentiation/regression workflow; grouping and comparison across particle/material classes; interpretation of ratios; audit and correction of quantitative claims. | The underlying experiments were performed by the source authors, not the applicant. Absolute vertical-coordinate calibration is unresolved, so absolute physical settling speeds are not claimed. Ratios are equal-weight summaries over available specifications, not particle-count-weighted population estimates. |
| **E2 — DS2 stratified-settling analysis** | scripts/analyze_ds2_stratified.py; data/ds2_stratified/ds2_interface_summary.json; analysis/POST_MERGE_AUDIT_2026-11-25.md. The analysed dataset contains 108 ensemble-averaged trajectory records. The workflow resamples irregular timestamps, computes smoothed kinematic quantities, applies interface-zone coverage rules and compares above/below-interface behaviour. | Time-series processing; numerical gradients and smoothing; data-quality checks; classification by experimental set and interrogation window; explicit handling of missing/insufficient coverage; critical interpretation of dataset metadata. | These are analyses of ensemble-averaged centroid tracks, not new single-particle experiments. Layer-order assignment and exact fluid recipes remain incompletely verified against the source paper. The results are descriptive and do not establish a universal causal law. |
| **E3 — M0 numerical transport baseline** | tests/test_transport.py; src/rheomarine_transport/ as identified in the repository README; docs/model/TRANSPORT_ENGINE_INTERFACE.md. The repository documents six deterministic tests covering zero-flow invariance, closed-domain mass conservation, diffusion mass conservation, source/sink bookkeeping, a stability guard and Stokes-settling sign/particle-class validation. | Numerical implementation; conservation and stability checks; software testing; separation of a controlled numerical baseline from later physical validation. | This is software verification on a controlled closed rectangular domain. Coastline masks, open boundaries, spherical metrics, HFR forcing integration and independent coastal forecast validation are not yet demonstrated. It must not be described as a validated operational ocean model. |
| **E4 — HFR data-readiness and provenance analysis** | docs/validation/INDEPENDENT_HFR_EVIDENCE_AUDIT_2026-11-25.md; docs/ristanc/application-support/HFR_LIVE_ENDPOINT_AND_CALIBRATION_CHECK_2026-11-25.md; docs/ristanc/application-support/HFR_SLOVENIAN_TERRITORIAL_SEA_DATA_AUDIT_2026-11-25.md. The work records endpoint checks, QC-flag coverage, temporal gaps, metadata and calibration questions for Izola and Piran. | Retrieval and inspection of real observational data products; metadata and provenance review; QC/coverage summarisation; identification of limits before model use. | This is a desk-based data audit, not operation or calibration of HFR instruments, not an ADCP validation campaign and not proof of full three-dimensional circulation. |
| **E5 — Research software and documentation practice** | Public repositories https://github.com/fabianleonaressi95/rheomarine and https://github.com/fabianleonaressi95/theorem; Code Ocean capsules https://codeocean.com/capsule/3674340/tree/v1 and https://codeocean.com/capsule/1970808/tree/v1. | Version-controlled research organisation; computational notebooks/scripts; structured reporting of methods, assumptions and numerical outputs. | The Code Ocean projects are exploratory computational outputs. The broader mathematical repository is supporting evidence of research practice, not evidence of oceanographic expertise or peer-reviewed validation of a marine model. |

## 4. Match between demonstrated competence and RheoMarine-SLO tasks

The applicant's personal responsibilities are restricted to tasks that can be performed and evidenced through computational work:

1. **Data intake and quality control:** retrieve public HFR products; preserve source metadata and retrieval records; apply documented QC/coverage rules; define the pilot window and polygon only after data-readiness checks.
2. **Experimental-data analysis:** process published particle-settling datasets; derive and compare quantities while retaining calibration, sampling and source-metadata limitations.
3. **Numerical modelling:** maintain and extend the controlled M0 transport baseline; implement M1 only using defensible particle-property inputs; keep code, configuration and numerical tests versioned.
4. **Model assessment:** conduct sensitivity and uncertainty analysis; compare matched model configurations; distinguish software verification, numerical robustness and independent physical validation.
5. **Research delivery:** prepare reproducible outputs, metadata, technical reports and dissemination materials.

The existing M0 code is a preliminary numerical core, not a completed coastal forecasting system. Full integration with the selected HFR fields, realistic coastal boundaries and independent observations remains project work.

## 5. Specialist competence gaps and mitigation

The project does not conceal the applicant's lack of a formal marine-science or laboratory-rheometry qualification. It manages this limitation through a deliberately staged design:

- HFR observations will be used as surface-current data products, subject to provider documentation and QC. The applicant will not claim to operate or independently calibrate the radar network.
- Laboratory characterisation will be procured from a qualified external provider if a suitable scope, price and schedule are confirmed. The applicant will analyse and document the supplied data but will not claim to perform rheometer measurements.
- Oceanographic interpretation and independent validation will be sought through technical consultation or collaboration only where the relevant researcher or institution explicitly agrees in writing.
- NIB's reported data holdings and analytical capacity, and the interest expressed by individual contacts, are not treated as a formal partnership, guaranteed data access or a contribution already secured. OGS, NIB, ARSO and FVO are not listed as project partners without written confirmation.
- M2 remains conditional on the M4 evidence gate. If suitable measurements or specialist input are unavailable, the project will retain M0/M1 and report the limitation rather than manufacture rheological parameters.

This allocation makes the project feasible within the applicant's demonstrated computational competence while placing specialist experimental tasks with appropriately qualified providers.

## 6. Evidence index

Primary project evidence:

- RheoMarine repository: https://github.com/fabianleonaressi95/rheomarine
- DS1 analysis: scripts/analyze_ds1_settling.py
- DS2 analysis: scripts/analyze_ds2_stratified.py
- Quantitative interpretation audit: analysis/POST_MERGE_AUDIT_2026-11-25.md
- M0 test suite: tests/test_transport.py
- Model specification: docs/model/M0_M1_M2_MODEL_SPECIFICATION.md
- Transport interface: docs/model/TRANSPORT_ENGINE_INTERFACE.md
- HFR evidence audit: docs/validation/INDEPENDENT_HFR_EVIDENCE_AUDIT_2026-11-25.md
- Broader computational research: https://github.com/fabianleonaressi95/theorem
- Code Ocean capsules: https://codeocean.com/capsule/3674340/tree/v1 and https://codeocean.com/capsule/1970808/tree/v1

## 7. Applicant verification and submission checklist

Before submission:

1. Attach a current, signed and dated CV together with the proposed [research and computational project addendum](APPLICANT_CV_RESEARCH_ADDENDUM_DRAFT.md). The current CV does not yet list the Python/scientific-computing skills or the RheoMarine DS1, DS2, M0 and HFR work; verify each description and contribution before attaching it.
2. Add a selected list of the 13 articles reported in the CV, with titles, outlets, dates and URLs. Do not rely on an unreferenced count.
3. Verify the applicant's authorship/contribution to every repository, script and Code Ocean capsule cited above.
4. If available, attach verifiable certificates or training records for Python, numerical methods, data analysis or scientific computing. Do not imply that such certificates exist if they do not.
5. Keep the education titles and dates exactly as shown on the official degree records and CV.
6. Keep the distinction between completed computational analyses and future oceanographic/laboratory work visible in the application.

**Assessment boundary:** this annex supports competence in computational analysis, numerical implementation, data handling, reproducibility and scientific communication. It does not establish a formal marine-science qualification, professional oceanographic field experience or laboratory-rheometry expertise.
