# RheoMarine-SLO — Feasibility, Risk and Verification Matrix
**Date:** 26 November 2026  
**Use:** application-support annex for the RISTANC proposal. This is a planning and control document, not evidence that external services, partners, datasets or participants have been secured.

## 1. Overall feasibility judgement

**Feasible as an eight-month, applicant-led pilot study with staged scope and explicit fallback options. Not yet evidenced as a fully validated operational forecast system for microplastic concentrations, three-dimensional transport or seabed deposition.**

The project should be submitted only with this bounded claim. M0 is the mandatory core; M1 is conditional on traceable particle-property evidence; M2 is exploratory and proceeds only after the M4 decision gate. HFR surface currents are forcing information, not direct observations of microplastic concentration or vertical circulation.

### Feasibility by component

| Component | Current evidence | Feasibility judgement | What must be verified before/during delivery | Minimum acceptable output |
|---|---|---|---|---|
| M0 surface transport baseline | Existing finite-volume advection-diffusion/Stokes-settling implementation and six deterministic software tests | **Feasible, with validation work remaining** | Analytic translation/rotation tests; mass budget; grid/time-step convergence; coast/open-boundary behaviour; HFR ingestion; independent comparison where observations permit | Reproducible baseline, test report, parameter/provenance record and explicit statement of validation coverage |
| HFR forcing and pilot polygon | Public Izola and Piran HFR products identified; previous QC audit found substantial missing/invalid coverage and long outages | **Conditionally feasible; geography must be data-led** | Re-download exact period; inspect QC, timestamps, GDOP/coverage and spatial overlap; confirm metadata/calibration with data operators where possible | One defensible contiguous pilot area/time window, coverage maps/tables, data manifest and limitations; narrow or change window if needed |
| M1 biological conditioning | Published DS1/DS2 trajectory analyses offer preliminary evidence of material- and stratification-dependent settling differences | **Feasible as sensitivity/parameter scenarios; empirical calibration conditional** | Traceable parameter source, material/species mapping, unit checks, uncertainty ranges and separation of calibration from validation | M1 scenario comparison with provenance and uncertainty; no universal law or causal mechanism claimed |
| B.1 laboratory service | Budget placeholder €3,000; no confirmed quote or provider commitment recorded | **Critical unresolved dependency** | Written quote, method, sample count, deliverables, schedule, VAT/taxes, included consumables, data rights, shipping and cancellation terms | Either a contracted, bounded service within budget/timeline or a documented reduced-scope fallback |
| M2 rheological extension | No validated project-specific rheological parameter set yet documented | **Exploratory only; no-go is an acceptable outcome** | M4 review of relevant independent measurements, repeatability, parameter identifiability and expected model benefit | Written M4 go/no-go. If no-go, omit M2 and report why |
| Independent validation | Validation strategy drafted; actual independent dataset for every metric not secured | **Partly feasible; metric-specific** | Identify data source, licence, temporal/spatial overlap and independence from calibration; predefine metrics | Validation table classifying each result as independently validated, partially checked or unvalidated |
| Dissemination | Defined target of 30 unique people, one briefing and bilingual summary | **Operationally feasible but reach is not guaranteed** | Build a relevant contact list through public professional channels; log invitations, delivery, attendance and feedback; deduplicate | Evidence pack with anonymised reach counts, briefing report, materials and feedback summary |
| Applicant workload and administration | A.3 plan: 220 h × €30/h all-in over eight months | **Arithmetically feasible; fiscal treatment needs confirmation** | Confirm eligible all-in cost treatment for an Italian-resident natural-person applicant with ZRS/tax adviser; maintain timesheet and task log | Approved budget basis and contemporaneous time record; no claim that €30/h is net pay |
| Budget and procurement | Total €12,000 reconciles arithmetically; C.1–C.6 are planning estimates | **Conditionally feasible** | Confirm B.1 quote; validate travel assumptions and C.5 translation/printing costs; remove duplicate lab consumables; confirm procurement/tax rules | Final budget supported by quotes/calculations and no double-counting |

## 2. Risk register

Probability and impact are qualitative planning assessments, not statistical estimates. Ratings must be reviewed when new evidence arrives.

| ID | Risk and cause | Probability / impact | Early warning or trigger | Prevention / mitigation | Contingency and deliverable protection | Evidence to retain |
|---|---|---|---|---|---|---|
| R1 | HFR data gaps or poor QC prevent a sufficiently continuous pilot | High / High | Valid vectors do not support the predeclared spatial-temporal coverage criteria; outages overlap the analysis window | Reassess both Izola and Piran products; inspect exact cells, timestamps and QC; predefine selection rules before model fitting | Narrow polygon and/or time window; if necessary use HFR for bounded case studies, not continuous hindcast; deliver D1 with explicit limitations | Raw query/metadata, retrieval date, QC scripts, coverage tables/maps, selection decision |
| R2 | HFR product does not represent the vertical water column or particle concentration | Certain limitation / High if misrepresented | Any proposed claim infers 3D circulation, concentration or seabed deposition from surface HFR alone | State scope in methods, figures and executive summary; distinguish surface transport from vertical settling | Restrict claims to surface-current-informed transport scenarios and separately parameterised settling sensitivity | Model specification, assumptions register, report review checklist |
| R3 | Laboratory supplier unavailable, quote exceeds €3,000, or turnaround misses M4 | Medium–High / High | No written quote/scope by early project procurement checkpoint; method or lead time incompatible with M4 | Request comparable quotes; define minimum viable protocol and exact outputs; clarify taxes, consumables, sample handling and data ownership | Reduce or remove new lab work; use independently published parameters for sensitivity only; do not describe literature values as new measurements | Dated requests, quotes, supplier response, procurement decision, revised scope |
| R4 | DS1/DS2 published data cannot support quantitative parameter transfer | Medium / High | Unit calibration, material mapping, recipe or experimental conditions remain unresolved | Treat results as preliminary evidence; record assumptions; run bounded sensitivity scenarios; seek original methods/data where feasible | Do not calibrate M1/M2 from ambiguous values; retain M0 and report parameter uncertainty | Source bibliography, extraction tables, scripts, unit audit and limitations |
| R5 | M2 rheological correction is not identifiable or supported | High / Medium | Laboratory evidence absent, noisy or not relevant to environmental conditions by M4 | Make M2 conditional; define decision criteria before looking at outcome; compare added complexity against independent evidence | M4 no-go; omit M2; redirect effort to M0/M1 validation and uncertainty | M4 gate memo, evidence table, decision rationale |
| R6 | No independent validation dataset for one or more metrics | Medium–High / High | No independent observations with compatible variables, resolution, licence and overlap | Inventory validation sources in M1; keep calibration and validation records separate; avoid selecting metrics post hoc | Mark affected metrics unvalidated; report software verification separately from physical validation; no claim of predictive improvement | Dataset inventory, licences, split/provenance log, metric availability matrix |
| R7 | Model numerical errors or insufficient convergence | Medium / High | Failed mass budget, unstable runs, grid/time-step sensitivity or boundary artefacts | Extend test suite; analytic benchmarks; mesh/time-step refinement; conservation and stability diagnostics | Reduce model complexity/domain; deliver tested numerical baseline and disclose unresolved tests | CI/test logs, benchmark outputs, convergence plots, run configuration |
| R8 | Budget is insufficient or contains overlapping costs | Medium / High | Lab quote excludes VAT/consumables or requires extra sample preparation; travel/translation estimates differ materially | Obtain written quotes; define B.1 inclusions; keep C.3 at zero unless separately justified; verify travel route and unit prices | Reallocate only within call rules and with transparent justification; reduce scope rather than invent expenditure | Quotes, calculations, budget revision history, invoices/receipts if required |
| R9 | A.3 cost treatment for an Italian-resident individual is misunderstood | Medium / High | ZRS cannot confirm treatment or gross-up assumptions | Obtain written clarification from ZRS and advice from a qualified tax professional before finalising the amount | Revise hours/unit cost or eligibility route before signature; do not represent €30/h as net income | Written clarification, adviser note, final calculation |
| R10 | Planned 30-person dissemination target is not achieved | Medium / Medium | Low response to invitations or briefing registrations | Target relevant professional/community channels; send concise bilingual material; offer accessible online attendance | Report actual unique reach; widen lawful circulation; do not count impressions or duplicate contacts as unique beneficiaries | Redacted distribution log, platform attendance report, feedback summary, deduplication method |
| R11 | Data licences or privacy rules prevent redistribution | Medium / Medium | Dataset terms prohibit republishing; contact list contains unnecessary personal data | Link to source data rather than mirror restricted data; collect minimum contact information; publish aggregate metrics | Release code, metadata and derived data only where permitted; keep personal data private and time-limited | Licence register, data-management note, privacy notice/retention procedure |
| R12 | Eight-month schedule is compressed by procurement, access or review delays | Medium / High | WP2 procurement or WP1 data checks slip beyond planned checkpoints | Start data and provider checks early; maintain parallel work on M0 tests and documentation | Prioritise D1, M0, uncertainty analysis and final reproducible package; omit conditional M2 | Monthly progress log, decision log, revised Gantt/scope |

## 3. Decision gates and measurable controls

The gates below are project-management controls. They do not imply that any external organisation has agreed to provide data, services or participation.

| Gate | Timing | Decision question | Required evidence | Go decision | No-go / fallback |
|---|---|---|---|---|---|
| G0 — mobilisation and procurement | M1 | Can the project access the intended HFR products and procure the minimum viable laboratory service within time and budget? | HFR access/metadata check; provider replies and written quote or documented market check; revised task schedule | Proceed with bounded Izola–Piran candidate pilot and feasible lab protocol | Narrow pilot; remove new lab measurements if unavailable; preserve literature-based sensitivity only |
| G1 — data readiness | End M2 | Is there a contiguous, defensible HFR area and period for the intended surface-transport analysis? | QC-filtered coverage and outage analysis; spatial overlap; timestamp regularity; data provenance | Fix polygon and period using documented criteria | Narrow area/window or switch to case-study analysis; do not imply full-coast coverage |
| G2 — particle evidence | End M4 | Are particle-property and settling inputs traceable and relevant enough for M1, and is there evidence to justify M2? | Source/method, units, uncertainty, sample/material mapping, repeatability and independence assessment | Retain only the model level supported by evidence | M1 limited to sensitivity scenarios; M2 omitted if not supported |
| G3 — numerical and validation readiness | M5–M6 | Are M0/M1 numerically stable and is independent validation available for each claimed metric? | Benchmark and convergence results; mass-budget tests; validation data inventory and metric definitions | Compare only validated/partially validated metrics with explicit labels | Report software verification and sensitivity only where physical validation is unavailable |
| G4 — final evidence and dissemination | M8 | Are deliverables reproducible, limitations disclosed and actual reach evidenced? | Versioned repository/release; data and code manifest; final report; briefing record; deduplicated dissemination log | Publish and report verified outputs | Publish a scoped pilot report and list outstanding evidence; do not inflate impact claims |

## 4. Laboratory procurement specification — minimum request for quotation

The €3,000 B.1 line is a **budget ceiling/planning placeholder**, not a supplier quote or evidence of availability. Before treating WP2 as secured, request a written offer that answers:

1. Provider legal name, laboratory location and relevant competence/accreditation (where applicable).
2. Exact method(s) proposed and the parameter(s) measured: particle size distribution, effective density, aggregation/aggregate size, settling velocity and/or rheological properties. Do not assume one method measures all of these.
3. Sample type, number of samples/replicates, sample volume or mass, preparation and storage requirements.
4. Whether natural seawater/EPS samples can be accepted; any permits, biosafety, chain-of-custody or shipping requirements.
5. Raw data and processed outputs supplied, units, calibration information, uncertainty and quality-control documentation.
6. Turnaround time and milestone dates compatible with the M4 decision gate.
7. Full all-in price, VAT/tax status, shipping, sample preparation, consumables and any additional charges.
8. Data ownership, publication rights and permission to include results in the public report/repository.
9. Quote validity, payment terms and cancellation conditions.

**Procurement rule:** if the offer does not fit the B.1 allocation or schedule, reduce the scope. Do not create a fictitious quote, assume free institutional access or transfer costs into C.3 where they are already included in B.1.

## 5. Verification and evidence pack

Maintain one project evidence folder with a dated index. The minimum evidence pack is:

- **Data:** source URLs/IDs, retrieval date, metadata, licences, query parameters, QC rules, HFR coverage and outage summaries.
- **Numerics:** versioned code, software environment, deterministic test results, analytic benchmarks, convergence checks, mass-budget diagnostics and run configurations.
- **Particle processes:** source papers, extracted data tables, unit checks, parameter mapping, uncertainty ranges and limitations.
- **Laboratory:** requests for quotation, supplier replies, selected quote/contract if any, protocol, sample log, raw/processed results and QC.
- **Validation:** independent dataset inventory, calibration/validation separation, metric definitions, results and explicit unvalidated flags.
- **Management:** monthly hours log, task records, decision-gate minutes, risk updates and budget change log.
- **Dissemination:** final materials, Zenodo DOI/release where used, GitHub release, invitation/delivery log, attendance report, anonymised feedback and deduplicated unique-reach count.

## 6. Suggested application wording

> RheoMarine-SLO is feasible as a staged eight-month pilot because its mandatory core (M0) is an applicant-led computational workflow supported by an existing numerical implementation and deterministic software tests, while public HFR products provide a defined route to surface-current forcing. Feasibility is nevertheless conditional on a data-led selection of the pilot area and time window, as the available HFR records contain quality-control gaps and do not provide three-dimensional circulation or microplastic concentration measurements. Particle-conditioning scenarios (M1) will use only traceable published or newly measured parameters, with uncertainty reported. New laboratory work is subject to a written service quote and a minimum viable protocol within the B.1 budget. The rheological extension (M2) is explicitly conditional on an M4 evidence gate and will be omitted if measurements do not support it. Where independent observations are unavailable, affected metrics will be labelled unvalidated and no predictive improvement will be claimed. These controls protect delivery of a reproducible pilot report, tested baseline, documented uncertainty and evidence-based recommendations even if the more ambitious extensions are not justified.

## 7. Pre-submission closure checklist

- [ ] Obtain and review a written B.1 quote, or explicitly revise WP2 and budget assumptions before submission.
- [ ] Confirm B.1 scope, VAT, sample preparation, consumables, delivery time and data/publication rights.
- [ ] Verify C.1 travel basis and C.5 translation/printing estimates; retain support for unit costs.
- [ ] Confirm A.3 all-in treatment and eligibility for an Italian-resident natural-person applicant with ZRS/tax adviser.
- [ ] Ensure the application calls the HFR data surface-current observations and does not infer 3D transport or seabed deposition from HFR alone.
- [ ] Keep M1 parameter transfer conditional and M2 exploratory.
- [ ] Name no institution, researcher, laboratory or stakeholder as a partner without written agreement.
- [ ] Keep the 30-person figure labelled as a target; actual beneficiaries will be counted and deduplicated at delivery.
- [ ] Preserve the fallback: M0 + uncertainty + reproducible report remain deliverable if laboratory work or M2 cannot proceed.

---
