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

RheoMarine-SLO will address the RISTANC challenge concerning marine pollution, plastics and the protection of marine ecosystems. The project will focus on the Slovenian territorial sea. The initial candidate pilot is the **Izola–Piran coastal sector**, subject to verification of the integrated HFR product, valid-vector coverage, quality flags, temporal continuity and access conditions. The current quantitative evidence is reported in the [HFR quantitative coverage note](HFR_QUANTITATIVE_COVERAGE_2026-11-28.md): both nodes have nominal 20×22 grids (440 cells); seven-day subsets yielded 337 IZOL and 325 PIRA timestamps; selected 4×4 pilot subregions had mean cell-validity fractions of 88.43% and 93.40%, respectively; recent 30-day strict QCflag==1 fractions over the full grid were approximately 51% (IZOL) and 25% (PIRA). These metrics have different denominators and do not establish continuous common coverage or data accuracy. The final pilot polygon will be selected after common-mask and territorial-boundary intersection in WP1. The final contiguous pilot polygon and analysis period will be fixed in M1 using predeclared coverage and continuity criteria and, where possible, complementary observations. Ankaran and Koper remain possible wider-context sectors, not assumed areas of validated or continuous data coverage. The project will not treat nominal station extent or an automatically selected rectangular grid crop as proof of geographic representativeness.

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
| **WP4 — Synthesis, dissemination and reuse (M7–M8)** | Prepare the final technical report and a two-page non-technical summary in English and Slovenian; publish project-generated code, metadata and reproducibility manifest subject to third-party licences; circulate the brief to targeted monitoring/research contacts and the accessible summary through coastal/community channels; hold one open online or hybrid technical briefing (target 15–20 attendees); record invitations, actual attendance, feedback and unique reach. | **D4:** final report; English technical brief and Slovenian-language summary; versioned code, metadata and reproducibility manifest; one briefing; dissemination log with a deduplicated target of 30 unique people. |

The applicant will coordinate the work, conduct the computational analysis and modelling, maintain the reproducibility record and prepare the reports. Laboratory measurements will be procured as a defined external service if a suitable provider and quote are secured. No institution or researcher is represented as a confirmed partner unless a separate written agreement is obtained.

**Feasibility and fallback arrangements.** The pilot sub-area will be narrowed if HFR coverage or data quality is insufficient. If the preferred laboratory cannot provide the required service within the budget and schedule, the project will use only independently documented parameters and available datasets, reduce the experimental scope, and clearly report the limitation; it will not substitute unsupported rheological assumptions for missing measurements. If independent validation data are unavailable for a particular metric, that metric will be labelled as unvalidated and will not be used to claim model improvement.

### Innovation

The innovation of RheoMarine-SLO lies in a falsifiable, staged comparison of three levels of description in a defined Slovenian coastal setting: a conventional hydrodynamic baseline (M0), a biological particle-conditioning model (M1), and a rheological settling correction (M2) that is introduced only when supported by independent experimental evidence.

Rather than assuming that a more complex model is necessarily better, the project uses an explicit decision gate and independent validation to determine whether additional biological or rheological information improves predictive performance. It also separates surface-current observations from vertical particle processes and makes data limitations and uncertainty part of the reported result.

The added value is a reproducible workflow that can show which additional measurements or particle parameters materially affect transport and settling estimates, and which do not. The project does not claim to establish a new physical law, to demonstrate that seawater as a whole is non-Newtonian, or to treat laboratory polymer proxies as interchangeable with naturally occurring extracellular polymeric substances (EPS).

### Impact

The expected impact is improved evidence for interpreting microplastic transport and settling in a selected area of the Slovenian territorial sea. The project will provide a transparent comparison of model assumptions, an assessment of uncertainty, and a documented indication of whether biological aggregation or additional rheological measurements are useful for this specific application.

The project will use a defined dissemination pathway rather than relying on unspecified public exposure. The target is **30 unique people reached by the end of M8**, distributed across three groups. The figures below are planning targets, not confirmed participants, endorsements or institutional commitments.

| Target group | Need addressed | Output / benefit | Concrete dissemination route and KPI | Planned reach |
|---|---|---|---|---:|
| Slovenian marine/environmental monitoring practitioners and relevant public-sector technical staff | Understand the limits of surface-current products and the sensitivity of transport/settling estimates to particle assumptions | Technical brief, pilot-area HFR coverage/QC note and model-comparison findings | Directly send the final brief to a targeted list of relevant public monitoring contacts; invite recipients to the final briefing; record the number of unique recipients and responses. No agency endorsement is implied. | **8 people** |
| Researchers, postgraduate students and technical specialists in marine pollution, environmental modelling and particle processes | Access reproducible methods, documented assumptions and evidence on model performance | Versioned workflow, metadata, technical report and reuse instructions | Public repository release; targeted circulation to relevant research groups and professional contacts; invitation to the final briefing. Record repository release and direct recipients; do not promise a number of downloads. | **12 people** |
| Coastal communities, environmental organisations and other interested coastal stakeholders | Understand what the modelling can and cannot establish about microplastic transport in the Slovenian coastal area | Two-page non-technical summary in English and Slovenian, plus a short presentation of findings and limitations | Circulate the summary through relevant public/community channels and invite local stakeholders to the open briefing. Attendance and distribution will be recorded where feasible. | **10 people** |

The **30-person target is a deduplicated planning target** across the three groups; a person reached through more than one channel will be counted once. The project will aim for **15–20 attendees** at one open online or hybrid technical briefing in M8, included within—not added on top of—the 30-person target. The invitation will be circulated to a targeted list of approximately 40–50 relevant contacts, subject to the availability of public contact channels. Actual invitations, attendance and dissemination outputs will be recorded in D4. The project does not assume that NIB, ARSO, OGS, municipalities or any named organisation has agreed to participate.

**Dissemination schedule and deliverables**
- **M6–M7:** prepare a concise technical report and a two-page non-technical summary; prepare the English version and a Slovenian-language version/proofread summary.
- **M7:** publish the project-generated code, metadata, reproducibility manifest and report in the project repository, subject to third-party data licences.
- **M7–M8:** circulate the technical brief to relevant monitoring and research contacts and the accessible summary through appropriate coastal/community channels.
- **M8:** hold one open online or hybrid technical briefing (target 15–20 attendees); present the pilot-area/data limitations, M0/M1 comparison, any justified M2 result, uncertainty and practical implications; collect questions and concise feedback.
- **M8:** complete a dissemination log recording the materials released, channels used, invitations sent, attendance (where consented), approximate unique reach and feedback received.

The impact is therefore an improved evidence base, transparent uncertainty and a reusable analytical workflow—not a claim that an eight-month modelling study directly reduces marine litter or changes environmental status.

### Sustainability

The main results will remain usable through a versioned repository containing the project-generated code, documented workflows, metadata, model assumptions, validation procedures and final technical report. Where legally and technically possible, project-generated data and publications will be made openly accessible. Third-party HFR, literature and experimental datasets will be shared or referenced only in accordance with their original licences, access conditions and attribution requirements; where redistribution is not permitted, the project will provide metadata and instructions for obtaining access from the data owner.

The technical brief will be written for reuse by researchers and relevant monitoring practitioners. The workflow will document its software environment, input requirements and limitations so that it can be rerun or adapted to other coastal datasets. The applicant will preserve the project repository and outputs after the grant period, but the application will not promise permanent maintenance by an external institution or organisation that has not agreed to undertake it.

### Competencies and experience

The applicant is an independent researcher with formal qualifications in Italian literature (BA, University of Bologna, 2018) and journalism and publishing culture (MA, University of Parma, 2021). These qualifications support research communication, literature synthesis and technical dissemination; they are not presented as degrees in oceanography, engineering or marine chemistry. The applicant has a public SSRN working-paper record with DOI 10.2139/ssrn.7015478. The applicant legally changed their name in 2021; the 2019 *ParmAteneo* byline “Fabiano Naressi” is the applicant's former legal name and refers to the same person now applying as Fabian Leo Naressi. The historical byline is retained exactly as published, and documentary evidence of the legal name change can be provided if required. The applicant's journalism experience includes a collaboration with *La Voce di Parma* (February–September 2019), supported by the CV and contemporaneous email correspondence, and a published *ParmAteneo* article, “Senza peli sulla lingua: intervista a Massimo Fini” (19 September 2019; byline “Fabiano Naressi” (the applicant's former legal name before the 2021 legal name change); historical URL https://www.parmateneo.it/?p=52962). These are journalism/public-communication records, not peer-reviewed scientific publications. A Comune di Parma supply document lists *La Voce di Parma* among weekly periodicals supplied to the municipal library system in October 2019–September 2021; preservation of the specific 2019 issues remains unverified. A separate manuscript submitted to *Economia&Lavoro* in July 2026 is not counted as published because acceptance has not been verified. The applicant also completed a 124-hour professional course, “Digital Office Assistant with Google Workspace and Gemini AI” (METHOD JOB B.V.; Forma.Temp; 4–25 March 2026), supporting digital productivity and AI-assisted collaborative work.

The applicant's relevant competence for this project is computational and analytical. It is evidenced by work already documented in the RheoMarine repository (https://github.com/fabianleonaressi95/rheomarine): (i) a Python analysis of 722 particle-tracking runs from a published microplastic-settling dataset, including material-specific comparisons and a post-analysis interpretation audit; (ii) a second workflow analysing 108 ensemble-averaged records from published stratified-settling experiments, with time resampling, interface-zone analysis and explicit coverage checks; and (iii) a first finite-volume surface-transport baseline accompanied by six deterministic software tests covering invariance, mass conservation, source/sink bookkeeping, stability and settling-sign checks. The repository also contains a documented HFR data-readiness audit for the Izola and Piran feeds, including QC coverage, temporal gaps and metadata limitations.

These outputs demonstrate practical experience in scientific Python workflows, numerical data processing, model implementation, software verification, data provenance and critical reporting of uncertainty. Their evidential limits are retained: the underlying DS1/DS2 experiments were performed by the source authors; DS1 absolute vertical calibration remains unresolved; DS2 uses ensemble-averaged tracks and has unresolved source-paper mapping; the M0 test suite verifies a controlled numerical implementation and does not constitute physical validation of a coastal forecast. The HFR work is a desk-based data audit, not radar operation or independent oceanographic validation. Further details and direct artefact paths are supplied in the [C6 applicant competence and evidence annex](APPLICANT_COMPETENCE_EVIDENCE_ANNEX_DRAFT.md).

The applicant will personally lead data processing and QC, computational implementation of M0 and evidence-supported M1, sensitivity and uncertainty analysis, reproducibility records, and technical reporting. M2 will be implemented only if the M4 evidence gate is passed. The applicant does not claim an established professional track record in operational oceanography, marine field sampling or laboratory rheometry. The project has received written offer M49249 from Measurlabs for five seawater µFTIR samples (four environmental samples plus one field blank): EUR 2,047 before customer-country VAT, with an indicative total of EUR 2,497.34 using 22% Italian VAT. The supplier confirms Gulf of Trieste seawater suitability, sample preparation/reporting, polymer identification, particle counts and size, a 4–5 week turnaround and acceptance of an individual applicant. The offer is a supplier quotation, not a confirmed scientific partner or completed analysis. Specialist oceanographic advice or independent validation will be described as a collaboration only after explicit written agreement. No institution or researcher is represented as a confirmed partner without such agreement.
---

## Applicant review — items to close before copying into the official form

These are drafting controls and must **not** be pasted as claims into the application unless verified.

1. **Pilot area:** confirm which of Ankaran, Koper, Izola and Piran actually falls within the selected data footprint and whether the final pilot should be narrower. Confirm the HFR stations/cells, period, quality flags, data-access conditions and any complementary ADCP or sampling data.
2. **Laboratory:** obtain the quote and confirm the provider, protocol, sample types/counts, instruments, deliverables, turnaround time, VAT and whether consumables are included in B.1.
3. **Natural samples and permits:** decide whether natural seawater/EPS/biological samples are actually needed. Do not promise collection before permissions and availability are confirmed.
4. **Independent validation:** identify the independent dataset for each metric and ensure it is not also used for calibration. If no independent observations exist for a metric, do not present the metric as validated.
5. **Target-group reach:** the revised planning target is 30 unique people (8 monitoring/public-sector practitioners, 12 researchers/students/specialists, 10 coastal/community stakeholders), with 15–20 attendees targeted for one final briefing. These are targets, not confirmed participants; record actual reach and deduplicate overlaps.
6. **Applicant evidence:** map the CV and specific repository/code outputs to the competencies paragraph; attach a concise CV under “OTHER” only if permitted/appropriate.
7. **Language and character limits:** confirm whether the form must be submitted in English and whether the submission platform or call administrator imposes limits not shown in the DOCX.
8. **Ethics and AI:** align the final wording with the actual use of AI, any stakeholder contact, personal-data collection, laboratory waste arrangements and the RISTANC consent form.
9. **Budget consistency:** use the [A.3/C budget and dissemination plan](RISTANC_A3_C_BUDGET_AND_DISSEMINATION_PLAN_2026-11-26.md) for the proposed 220 hours × EUR 30 all-in and the itemised EUR 600 C allocation. Confirm the fiscal treatment and ensure travel, venue, translation and printing assumptions match the actual delivery plan. Keep B.1 at EUR 3,000 only if a suitable laboratory scope and quote are secured; avoid double-counting any consumables included in B.1.
10. **Start date:** use the effective date of the signed funding agreement, not a pre-agreement fixed start date.
