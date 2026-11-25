# RISTANC — Application Readiness and Evidence Dossier
**Project:** RheoMarine-SLO  
**Date:** 25 November 2026  
**Purpose:** consolidate the evidence needed to turn the existing Section C draft into a submission-ready application.  
**Rule:** distinguish documented facts, planned activities, external dependencies and items not claimed. No institution, dataset, laboratory, sample or stakeholder is represented as committed unless written confirmation exists.

## 1. Four substantive evaluation requirements

### 1.1 Concrete link to the Slovenian territorial sea

**Evidence now available**
- Slovenian HFR nodes at Izola (NIB) and Piran (ARSO) are documented by NIB and the European HFR Node.
- Public ERDDAP datasets exist for both stations, with nominal 30-minute resolution, geospatial metadata and QC fields.
- The data are directly relevant to surface-current forcing for a pilot in Slovenian coastal waters.

**Application wording**
Use the territorial wording in `HFR_SLOVENIAN_TERRITORIAL_SEA_DATA_AUDIT_2026-11-25.md`. The first project month will verify actual spatial overlap, valid-data fractions, temporal coverage and quality flags before fixing the pilot polygon/time window.

**Still open**
- Download and QC analysis of the exact cells/time period.
- Final pilot polygon and analysis window.
- Independent validation dataset for each metric.

Do not state that Ankaran, Koper, Izola and Piran are all fully covered. They are candidate coastal sectors; the final area is data-led.

### 1.2 Feasible implementation without a formal OGS collaboration

The applicant-led plan is feasible as a staged computational project:
- WP1: obtain public HFR data, verify QC/coverage and define the pilot.
- WP2: request a qualified external laboratory service for a bounded measurement protocol; use existing published datasets if no quote/service is secured.
- M4: retain M2 rheological correction only if independent experimental evidence supports it.
- WP3: implement M0/M1; M2 only after the gate; separate calibration and validation.
- WP4: report, archive metadata/code and disseminate a concise technical brief.

**No OGS partnership is claimed.** OGS operates one node in the regional network and contributes to the published HFR system; that fact does not make OGS a RheoMarine partner or guarantee bespoke support. Public Izola/Piran data are the primary access route. Laboratory work is a subcontracted service only if a supplier, scope, price, timeline and procurement route are confirmed.

**Fallbacks**
- HFR incomplete: narrow pilot/time window; do not extrapolate unsupported coverage.
- Laboratory unavailable/too expensive: reduce experimental scope; use independently published parameters; do not claim new rheological measurements.
- No independent validation data: report the affected metrics as unvalidated; do not claim predictive improvement.
- M2 unsupported at M4: omit M2 and complete M0/M1 analysis.

### 1.3 Local impact and user pathway

The project will not promise direct removal of plastic pollution or immediate changes in municipal policy. Its deliverables are decision-support evidence:
1. Pilot-area/data-readiness map and HFR limitations.
2. Technical comparison of conventional and biology-informed settling assumptions.
3. Quantified uncertainty and sensitivity analysis.
4. Evidence-based recommendations on which additional measurements are worth collecting.
5. Reproducible workflow, metadata and concise technical brief.

**Potential user groups (not confirmed partners or committed recipients)**

| Potential user group | Concrete relevance | Project output they could use | Engagement route | Planned reach |
|---|---|---|---|---:|
| Slovenian marine/environmental monitoring bodies, including ARSO and NIB/Marine Biology Station | Interpret surface-current observations and understand limits when inferring particle transport | HFR data/QC note, model-comparison brief, data-gap recommendations | Public institutional contact channels; send final technical brief; invite to an open online briefing | 5–10 people |
| Coastal environmental/public-service stakeholders in the Slovenian coastal area | Understand what the model can/cannot say about microplastic transport and what monitoring is needed | Short non-specialist summary and local pilot map | Publicly available municipal/environmental contact channels; open invitation | 10–15 people |
| Researchers, students and technical specialists in marine science, environmental modelling and particle processes | Reuse methods and assess model assumptions | Versioned code, metadata, methods and technical report | Repository publication, research mailing lists and open briefing | 10–20 people |

**Estimated reach:** 25–45 unique people, with overlap deduplicated. These are planning estimates, not confirmed attendance, endorsements, letters of support or commitments by ARSO, NIB, OGS or municipalities. If the application form asks for target-group reach, retain this caveat and explain the channels.

### 1.4 Applicant competencies — evidence map

The application should evidence the computational and documentation work directly, while openly identifying the marine-operational and laboratory components as external dependencies.

| Project task | Documented evidence available | How to present it | Boundary / caveat |
|---|---|---|---|
| Mathematical/computational modelling | Research repositories and technical records; Python, NumPy, SciPy and QuTiP work | Link selected, relevant examples and describe the applicant's own contribution | Do not equate exploratory models with validated marine prediction |
| Numerical analysis and reproducibility | RheoMarine scripts for DS1/DS2, machine-readable outputs, audit notes and correction history | Show script names, dataset provenance, methods and reproducibility workflow | Preserve known limitations: DS1 z calibration; DS2 set-to-fluid mapping; dataset weighting |
| Particle-settling data analysis | DS1 analysis of 722 terminal trajectories and DS2 stratified analysis of 108 average trajectories | Present as analysis of published experimental datasets, not original experiments conducted by applicant | Do not claim to have performed laboratory measurements |
| Scientific communication | BA/MA qualifications and 13 published articles (as listed in CV) | Attach concise CV and selected publication list | Verify dates/titles and provide documentary links |
| Computational research outputs | Code Ocean capsules: https://codeocean.com/capsule/3674340/tree/v1 and https://codeocean.com/capsule/1970808/tree/v1 | Identify them as computational capsules and state exactly what each explores | Exploratory outputs; not peer-reviewed proof of a general physical law |
| Marine field operations, HFR instrument operation and rheometry | No established direct professional track record documented in the current CV material | State explicitly that these are not claimed as applicant's independent competencies; use public HFR products and a qualified lab supplier if contracted | Do not inflate CV or imply access to instruments/lab |

**Suggested CV annex structure (2–3 pages)**
1. Profile and relevant education.
2. Technical skills: Python, numerical/scientific computing, data processing, reproducibility, version control.
3. Three selected evidence items: RheoMarine DS1/DS2 scripts; one relevant Code Ocean capsule; selected theorem/research repository record.
4. Scientific communication and publications.
5. Explicit role in RheoMarine-SLO and limits of experience.

### 1.5 Sustainability and reuse

- Maintain a versioned public repository for project code, documentation and metadata, subject to data-provider terms.
- Publish derived products only where the original dataset licence permits; cite the European HFR Node, NIB, ARSO and other data providers.
- Keep third-party raw data under their original licences and link to source rather than republishing restricted files.
- Include a reproducibility manifest: dataset ID, retrieval date, query, QC filters, software versions, processing scripts and output hashes.
- Do not promise institutional maintenance after the grant unless an institution agrees in writing.

## 2. Administrative application data — local completion checklist

Personal identifiers and banking details must be entered only in the official application form, not committed to this public repository.

- [ ] Complete the natural-person applicant section using the applicant's legal name and current registered residence.
- [ ] Where relevant and accepted by the form, state the capacity in which the applicant acts (trustee) without representing the trust as a separate legal person unless the programme confirms that classification.
- [ ] Leave legal-entity fields blank if the application is formally submitted by a natural person.
- [ ] Complete the contact-person section only if the contact person differs from the applicant.
- [ ] Attach only identity/residence evidence required or accepted by ZRS; do not assume an apostille authenticates the truth of every private declaration.
- [ ] Complete conflict-of-interest, ethics, double-funding, accuracy and privacy declarations truthfully.
- [ ] Confirm whether the 2022 residence certificate plus the Article 41(2) DPR 445/2000 statement is accepted by ZRS; Italian domestic validity rules do not automatically bind a Slovenian recipient.
- [ ] Complete the applicant's CV and selected evidence annex.
- [ ] Enter bank details only in the protected official form and verify account-holder and cross-border payment requirements directly with ZRS.
- [ ] Confirm signature format, language, file format, email destination and receipt procedure.

## 3. Budget completion

Current budget retained unchanged pending quote and itemisation:

| Form line | Current amount | Completion needed |
|---|---:|---|
| A.3 — applicant work | €6,600 | Specify hours/months, unit cost and gross cost basis as required by the current FAQ |
| B.1 — external laboratory service | €3,000 | Obtain real quote; define methods, samples, outputs, schedule and VAT treatment |
| C — direct purchases | €600 | Allocate only to actual eligible subcategories C.1–C.6; avoid double-counting lab consumables |
| E — indirect costs | €1,800 | 25% × (A+C) = €1,800; verify exact form calculation |
| **Total** | **€12,000** | Within the stated call range, subject to final eligibility checks |

Do not invent the laboratory quote, quantities, unit prices or purchases. If a cost cannot be supported, revise the allocation transparently before submission.

## 4. Submission readiness status

| Item | Status | Next action |
|---|---|---|
| Section C narrative | **Drafted** | Final form-length and consistency check |
| Slovenian territorial data pathway | **Documented** | Download/QC actual HFR subset and define pilot |
| No-OGS implementation fallback | **Documented** | Keep OGS out of partner list absent written agreement |
| Local impact pathway | **Drafted; estimates only** | Finalise dissemination channels and plausible reach |
| Applicant competence evidence | **Partly documented** | Assemble concise CV and links to artefacts |
| Laboratory quote | **Open dependency** | Obtain supplier quote or reduce scope |
| C €600 itemisation | **Open** | Populate from actual planned costs only |
| A.3 hours/unit cost | **Open** | Decide defensible time allocation |
| Administrative declarations | **Open** | Complete official form and verify ZRS requirements |
| Final form visual inspection | **Open** | Check checkboxes, signatures, income table and attachments |

## 5. Immediate sequence

1. Download the Izola and Piran HFR subsets and create a coverage/QC summary.
2. Assemble the two-to-three-page CV evidence annex.
3. Obtain or rule out the laboratory quote; do not leave B.1 described as a confirmed service.
4. Itemise C and specify A.3.
5. Populate the official application form and visually inspect every page.
6. Run a final factual, budget, ethics and administrative audit before submission.

## 6. Sources

- NIB HF radar overview: https://www.nib.si/mbp/en/oceanographic-data-and-measurements/other-oceanographic-data/hf-radar-2
- Izola ERDDAP dataset: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.html
- Piran ERDDAP dataset: https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3.html
- ARPA FVG HFR-NAdr network: https://monitor.meteo.fvg.it/radar_marino.php?ln=-en
- OGS Gulf of Trieste Marine Observatory: https://www.ogs.it/en/gulf-trieste-marine-observatory
- RISTANC current call documents and reviews: see `docs/references/ristanc/`.
