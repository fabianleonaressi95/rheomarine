# RISTANC Application — Section C draft (English)

**Project:** RheoMarine-SLO  
**Status:** Working draft for applicant review; not a submitted application.  
**Drafting basis:** current RheoMarine dossier, application-form extraction, evaluation review, ethics review and gap/budget audits.  
**Important:** bracketed items are factual dependencies to close before submission. Numerical reach estimates below are planning estimates, not confirmed attendance or institutional commitments.

---

## C. Project idea

### Project title

**RheoMarine-SLO: Testing the role of biological aggregation and effective particle properties in microplastic transport and settling in the Slovenian territorial sea**

### Project duration

**8 months**, starting from the effective date of the RISTANC funding agreement. The work plan below uses relative project months (M1–M8); it does not assume that the project can start on 1 January 2027 before the agreement is signed.

### Project relevance

Microplastic pollution is a recognised pressure on marine ecosystems. Understanding where microplastic particles are transported, how long they remain in the water column, and under which conditions they settle is relevant to monitoring and management in the Slovenian territorial sea. Particle behaviour depends not only on surface circulation, but also on particle size, density, shape, biological conditioning and aggregation. These processes can affect the reliability of predictions based on conventional particle-settling parameters alone.

RheoMarine-SLO will address the RISTANC challenge concerning marine pollution, plastics and the protection of marine ecosystems. The project will focus on the Slovenian territorial sea. The initial candidate pilot is the **Izola–Piran coastal sector**, subject to verification of the integrated HFR product, valid-vector coverage, quality flags, temporal continuity and access conditions. The final contiguous pilot polygon and analysis period will be fixed in M1 using predeclared coverage and continuity criteria and, where possible, complementary observations. Ankaran and Koper remain possible wider-context sectors, not assumed areas of validated or continuous data coverage. The project will not treat nominal station extent or an automatically selected rectangular grid crop as proof of geographic representativeness.

The project will assess whether adding information on biological aggregation and experimentally supported particle properties improves the description of microplastic transport and settling compared with a conventional hydrodynamic baseline. This is locally relevant because better characterised uncertainty and settling assumptions can support the interpretation of monitoring data and the design of future targeted observations in Slovenian coastal waters.

The project will distinguish surface-current information from vertical transport and seabed deposition: HFR observations describe surface currents and do not, by themselves, reconstruct the full three-dimensional water-column circulation or directly measure seabed deposition.

### Objectives

The main objective is to develop and independently assess a reproducible, uncertainty-aware modelling workflow for microplastic transport and settling in a selected area of the Slovenian territorial sea, and to determine whether biological aggregation and, where supported by measurements, rheological corrections provide a measurable improvement over a conventional baseline.

The project will pursue three progressively more demanding model configurations:

- **M0 — hydrodynamic baseline:** surface-current information, an appropriately justified turbulent-diffusion representation and conventional particle-settling parameters.
- **M1 — biological particle conditioning:** representation of aggregation and biofouling through independently sourced or measured changes in effective particle properties.
- **M2 — conditional rheological correction:** a settling correction using rheological parameters only if the laboratory evidence and data quality justify it. M2 will be assessed at a formal decision point in M4 and will not be retained merely to increase model complexity.

Success will be assessed through the following indicators:

1. **Data and pilot-area readiness:** a documented pilot-area and time-window selection, with HFR coverage, quality-control criteria, data provenance and known limitations recorded in D1.
2. **Particle-characterisation evidence:** a documented set of particle/aggregate and settling parameters, with sample provenance, methods, uncertainty and limitations recorded in D2.
3. **Model comparison:** reproducible M0 and M1 runs, and an M2 run only if justified, evaluated using independent observations where available and metrics including RMSE, MAE, spatial displacement/error, settling-related quantities and residence-time estimates as appropriate to the available data.
4. **Evidence-based model selection:** a final comparison stating whether M1 and/or M2 improves performance over M0 on independent evidence. If no statistically and scientifically defensible improvement is demonstrated, the project will report that result and retain the simpler model.

The project will not define success as proving in advance that seawater is generally non-Newtonian or that a rheological correction must improve predictions.

### Implementation plan

The project will be implemented through four work packages over eight months. The schedule is relative to the effective start date under the funding agreement.

| Work package and timing | Main activities | Outputs / verification |
|---|---|---|
| **WP1 — Data, quality control and pilot-area definition (M1–M2)** | Review available HFR surface-current observations and complementary environmental/particle datasets; document access and licensing conditions; assess temporal coverage, quality flags, GDOP and spatial gaps; select the pilot sub-area and analysis window; define the independent-validation strategy and data-management record. | **D1:** pilot-area and data-readiness report, including coverage maps or tables, quality-control rules, provenance, limitations and a documented validation plan. |
| **WP2 — Particle processes and laboratory evidence (M2–M4)** | Finalise a minimum laboratory protocol with a qualified external laboratory; obtain measurements or documented parameters relevant to particle size, effective density, aggregation and settling; consider natural biological material only where permissions, sample availability and handling conditions are confirmed. Xanthan/carrageenan, if used, will be treated only as controlled experimental proxies and not as equivalent to natural marine EPS. | **D2:** laboratory/particle-characterisation report with methods, sample information, raw or processed data as agreed, uncertainty and limitations. |
| **M4 decision gate** | Review the quality and relevance of the laboratory evidence. Decide whether a rheological correction is sufficiently supported to proceed to M2. | A documented go/no-go decision. If evidence is insufficient, M2 is omitted and resources remain focused on M0/M1 validation and interpretation. |
| **WP3 — Modelling and independent comparison (M3–M7)** | Implement and document M0 and M1; implement M2 only after the M4 decision gate; compare model configurations against independent observations or datasets not used for calibration; quantify uncertainty and sensitivity; document where HFR surface information cannot support claims about vertical transport or seabed deposition. | **D3:** reproducible code/workflow and comparative technical report containing model assumptions, validation design, metrics, uncertainty, sensitivity and negative or inconclusive findings. |
| **WP4 — Synthesis, dissemination and reuse (M7–M8)** | Prepare final report, metadata and user-oriented technical brief; publish project-generated outputs where lawful and compatible with third-party licences; organise one concise online or hybrid technical briefing, subject to availability of participants; record feedback and provide access instructions for reusable outputs. | **D4:** final report, technical brief, versioned code and metadata, dissemination record and reuse/licensing note. |

The applicant will coordinate the work, conduct the computational analysis and modelling, maintain the reproducibility record and prepare the reports. Laboratory measurements will be procured as a defined external service if a suitable provider and quote are secured. No institution or researcher is represented as a confirmed partner unless a separate written agreement is obtained.

**Feasibility and fallback arrangements.** The pilot sub-area will be narrowed if HFR coverage or data quality is insufficient. If the preferred laboratory cannot provide the required service within the budget and schedule, the project will use only independently documented parameters and available datasets, reduce the experimental scope, and clearly report the limitation; it will not substitute unsupported rheological assumptions for missing measurements. If independent validation data are unavailable for a particular metric, that metric will be labelled as unvalidated and will not be used to claim model improvement.

### Innovation

The innovation of RheoMarine-SLO lies in a falsifiable, staged comparison of three levels of description in a defined Slovenian coastal setting: a conventional hydrodynamic baseline (M0), a biological particle-conditioning model (M1), and a rheological settling correction (M2) that is introduced only when supported by independent experimental evidence.

Rather than assuming that a more complex model is necessarily better, the project uses an explicit decision gate and independent validation to determine whether additional biological or rheological information improves predictive performance. It also separates surface-current observations from vertical particle processes and makes data limitations and uncertainty part of the reported result.

The added value is a reproducible workflow that can show which additional measurements or particle parameters materially affect transport and settling estimates, and which do not. The project does not claim to establish a new physical law, to demonstrate that seawater as a whole is non-Newtonian, or to treat laboratory polymer proxies as interchangeable with naturally occurring extracellular polymeric substances (EPS).

### Impact

The expected impact is improved evidence for interpreting microplastic transport and settling in a selected area of the Slovenian territorial sea. The project will provide a transparent comparison of model assumptions, an assessment of uncertainty, and a documented indication of whether biological aggregation or additional rheological measurements are useful for this specific application.

The principal target groups and estimated reach are:

| Target group | Need addressed | Expected benefit / output | Planned route to reach them | Estimated reach |
|---|---|---|---|---:|
| Marine and environmental monitoring practitioners, including relevant public bodies | Understand the limits of surface-current products and the sensitivity of transport/settling estimates to particle assumptions | Concise technical brief, pilot-area data/coverage assessment and model-comparison findings | Direct circulation of the brief and invitation to the project briefing; no institutional endorsement is implied | **5–10 people** |
| Researchers, students and technical specialists working on marine pollution, modelling or environmental data | Access to reproducible methods, documented assumptions and evidence on model performance | Versioned analysis workflow, metadata, technical report and open outputs where licences permit | Repository publication and one open technical briefing | **10–20 people** |
| Coastal and environmental stakeholders interested in marine litter and local sea conditions | Obtain an accessible explanation of what the modelling can and cannot establish for the Slovenian coastal area | Short non-technical summary and presentation of findings and limitations | Briefing and circulation through relevant professional/community channels, subject to access | **10–15 people** |

The estimated total is **25–45 people**, allowing for possible overlap between groups; the project will record actual attendance and avoid double-counting where feasible. These are planning estimates, not confirmed participants, partner commitments or guaranteed institutional uptake.

The project will not claim that an eight-month modelling study directly reduces marine litter or changes environmental status. Its near-term contribution is improved evidence, clearer uncertainty and a reusable analytical basis that monitoring practitioners and researchers may use when planning future observations or interpreting data.

### Sustainability

The main results will remain usable through a versioned repository containing the project-generated code, documented workflows, metadata, model assumptions, validation procedures and final technical report. Where legally and technically possible, project-generated data and publications will be made openly accessible. Third-party HFR, literature and experimental datasets will be shared or referenced only in accordance with their original licences, access conditions and attribution requirements; where redistribution is not permitted, the project will provide metadata and instructions for obtaining access from the data owner.

The technical brief will be written for reuse by researchers and relevant monitoring practitioners. The workflow will document its software environment, input requirements and limitations so that it can be rerun or adapted to other coastal datasets. The applicant will preserve the project repository and outputs after the grant period, but the application will not promise permanent maintenance by an external institution or organisation that has not agreed to undertake it.

### Competencies and experience

The applicant brings experience in computational and mathematical modelling, numerical analysis, Python-based scientific workflows and reproducible research. Relevant work includes the development and analysis of numerical models, matrix-based methods, simulation workflows and documented computational research outputs. The applicant has experience using Python and scientific libraries including NumPy, SciPy and QuTiP, and maintains research repositories in which results, code and levels of evidential support are documented.

This experience is directly relevant to the computational components of RheoMarine-SLO: data processing, numerical implementation, model comparison, sensitivity analysis, reproducibility and preparation of technical documentation. The applicant also has experience in scientific writing and dissemination.

The applicant does not claim an established professional track record in operational oceanography, marine field sampling or laboratory rheometry. These specialised tasks will therefore be limited to a clearly specified external laboratory service and/or technical advice only where availability, scope and cost are confirmed in writing. The project will not list OGS or any individual researcher as a partner without their explicit agreement. Any confirmed provider or partner, their precise role and their contribution will be described accurately in the final application.

---

## Applicant review — items to close before copying into the official form

These are drafting controls and must **not** be pasted as claims into the application unless verified.

1. **Pilot area:** confirm which of Ankaran, Koper, Izola and Piran actually falls within the selected data footprint and whether the final pilot should be narrower. Confirm the HFR stations/cells, period, quality flags, data-access conditions and any complementary ADCP or sampling data.
2. **Laboratory:** obtain the quote and confirm the provider, protocol, sample types/counts, instruments, deliverables, turnaround time, VAT and whether consumables are included in B.1.
3. **Natural samples and permits:** decide whether natural seawater/EPS/biological samples are actually needed. Do not promise collection before permissions and availability are confirmed.
4. **Independent validation:** identify the independent dataset for each metric and ensure it is not also used for calibration. If no independent observations exist for a metric, do not present the metric as validated.
5. **Target-group reach:** retain 25–45 only if a real dissemination route can be delivered. Revise the figures if the planned briefing or circulation channels change. Do not imply that any authority, university, institute or stakeholder has agreed to attend.
6. **Applicant evidence:** map the CV and specific repository/code outputs to the competencies paragraph; attach a concise CV under “OTHER” only if permitted/appropriate.
7. **Language and character limits:** confirm whether the form must be submitted in English and whether the submission platform or call administrator imposes limits not shown in the DOCX.
8. **Ethics and AI:** align the final wording with the actual use of AI, any stakeholder contact, personal-data collection, laboratory waste arrangements and the RISTANC consent form.
9. **Budget consistency:** this Section C draft does not change the budget. Before submission, align WP2 and the laboratory scope with B.1 EUR 3,000, allocate C EUR 600 only to actual eligible purchases, and state A.3 quantity and unit cost in accordance with the current FAQ.
10. **Start date:** use the effective date of the signed funding agreement, not a pre-agreement fixed start date.
