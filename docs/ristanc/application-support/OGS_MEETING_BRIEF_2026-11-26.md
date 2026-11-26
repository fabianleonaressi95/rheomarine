# RheoMarine-SLO — OGS meeting brief

**Meeting:** 26 November 2026  
**Purpose:** technical discussion and assessment of possible future collaboration.  
**Status:** RISTANC application in preparation; OGS is not a confirmed partner.

## 1. What is being proposed

**RheoMarine-SLO: Testing the role of biological aggregation and effective particle properties in microplastic transport and settling in the Slovenian territorial sea.**

The immediate proposal is a bounded pilot in the Slovenian territorial sea. It will test whether adding biological aggregation and experimentally supported particle properties improves estimates of microplastic transport and settling relative to a conventional baseline.

The proposed initial geographical focus is the Izola–Piran coastal sector, subject to verification of actual HFR coverage, quality flags, independent observations and the final pilot polygon. The project must not imply that the entire coastal strip is uniformly covered.

## 2. RISTANC application

- Call: RISTANC Small Projects Funding Call.
- Applicant: individual applicant resident in an EU Member State.
- Requested contribution: up to EUR 12,000 (current working budget).
- Planned duration: 8 months, counted from the effective date of the funding agreement.
- Submission deadline: 28 November 2026, 23:59 CET.
- Submission route: signed application PDF by email to ristanc-funding@zrs-kp.si.
- Challenge: marine pollution, plastics and protection of marine ecosystems.

RISTANC is the immediate pilot instrument. It is not a grant application by OGS, and OGS is not represented as an applicant, partner or committed provider.

## 3. Work already undertaken

- Analysis of published DS1 settling trajectories (722 runs) and particle-property data.
- Second-pass analysis of DS2 stratified settling data (108 trajectories), with explicit caveats on inferred layer order and fluid assignment.
- Definition of a staged M0/M1/M2 modelling design.
- Preliminary audit of public HFR-NAdr Izola and Piran ERDDAP endpoints and metadata.
- Identification of validation, calibration-traceability, laboratory and sampling dependencies.

These are computational analyses of existing datasets and public metadata, not original marine field campaigns or experiments conducted by the applicant.

### 3.1 Quantitative results already obtained

**DS1 — homogeneous-fluid settling (Mrokowska et al. 2024; 722 trajectories).** Terminal slopes were estimated from the final 40% of each recorded trajectory and compared with artificial-seawater (AS) baselines. The first-pass aggregate reports a decrease from 0.059 to 0.013 in the recorded z-units for AS to XG 1 g/L (about 78%). Because the absolute z calibration is unresolved (pixels versus metres), these are not yet physical settling velocities. The second-pass material-normalised analysis finds at XG 1 g/L: POM retains 24.4% of its AS-baseline speed (R=0.2437), PA 7.15% (R=0.0715), PET 7.23% (R=0.0723), and PS 4.75% (R=0.0475). Thus the robust candidate finding is **material-dependent relative retardation**, not an absolute sea-settling law. Ratios are equal-weight averages over available specifications, not particle-count-weighted population estimates; C_* specifications lack dimension records.

**DS2 — stratified two-layer settling (Mrokowska et al. 2025; 108 ensemble-averaged trajectory records).** After uniform-time resampling, explicit density-profile sorting by z, and separation of the interface-crossing IW1 from the lower-layer IW2 window, the IW1 median below/above speed ratios are: set1_1 0.66, set1_2 0.36, set1_3 0.14; set2_1 0.67, set2_2 0.33, set2_3 0.20; set3_1 1.37, set3_2 2.57, set3_3 5.41. The analysed sets therefore show a strong descriptive contrast between retardation in sets 1–2 and acceleration below the interface in set 3. IW2 median speeds agree with IW1 below-interface medians to within approximately 25% in 8/9 sets, supporting the interpretation of IW2 as a lower-layer reference window. **Critical qualification:** set-to-fluid ordering is inferred from the dataset description and kinematic signature, not verified against the paywalled paper; exact fluid recipes remain unresolved, and set3 bottom density (~1037–1038 kg/m³) is anomalous. These are kinematics of ensemble-averaged centroid tracks, not single-particle instantaneous measurements. No causal law or marine parameter transfer is claimed.

**HFR data-readiness audit — Izola and Piran (25 November 2026).** Public ERDDAP endpoint checks and cell-level QC summaries were executed. Over the latest 30-day window, QCflag==1 accounts for approximately 51% of the 440 nominal grid cells per timestamp at IZOLA and 25% at PIRAN. IZOLA acceptance is approximately 53% over 90 days; its 12-month flag-1 fraction falls to approximately 23%. PIRAN has roughly 2,000 gaps longer than one hour and a maximum outage around 51 days; IZOLA's maximum documented outage is around 65 days. Both feeds advertised same-day observations at the audit snapshot, with 1–30-day subset requests returning in roughly 1–37 seconds. Nominal resolution is 30 minutes but timestamps are irregular. These figures support IZOLA as the initial candidate and PIRAN as complementary data subject to stricter QC; they do not establish continuous coverage or validation of particle transport. The exposed calibration metadata dates (IZOLA 2023-01-01; PIRAN 2015-01-10) require operator confirmation, not a claim of instrument inaccuracy.

**Numerical transport core — software verification only.** A separate conservative finite-volume surface advection–diffusion baseline exists with six deterministic tests: zero-flow invariance, closed-domain mass conservation, diffusion mass conservation, source/sink budget, stability guard, and Stokes settling sign/particle-class validation. This is a controlled closed-rectangle implementation. It has not yet passed analytic translation/rotation benchmarks, grid/time-step convergence, realistic coastline/open-boundary tests, or independent observational validation. Do not present it as a validated coastal forecast.


## 4. Proposed scientific design

- **M0:** hydrodynamic baseline using suitable surface-current information, justified diffusion assumptions and conventional settling parameters.
- **M1:** biological conditioning/aggregation represented through measured or independently sourced changes in effective particle properties.
- **M2:** conditional rheological correction, retained only if relevant laboratory evidence supports it and it improves independent comparison.

HFR provides surface-current information; it does not directly measure full 3D circulation, vertical particle transport or seabed deposition. M2 is a hypothesis to test, not a predetermined result. Xanthan/carrageenan, if used, are controlled experimental proxies and are not interchangeable with natural marine EPS.

## 5. Questions for OGS

### Pilot area and oceanographic data
1. Is Izola–Piran a defensible pilot area given current HFR footprints and available complementary observations?
2. Which HFR variables, quality flags, temporal windows and spatial cells should be retained or excluded?
3. Are independent current observations (e.g. ADCP/current-meter records) accessible for a defined period?
4. What calibration/validation metadata or uncertainty documentation should be requested from the operators?

### Particle processes and laboratory work
5. Which measurements are essential to characterise particle size, effective density, aggregation and settling?
6. Is natural EPS/biological material necessary for this pilot, or can the first phase use existing published data and a limited controlled protocol?
7. Which laboratory or service provider could quote a bounded protocol, with methods, sample count, outputs, turnaround and total cost?

### Partnership and future funding
8. Could OGS envisage a future role in a larger collaborative proposal, subject to internal assessment?
9. Which FVG maritime-technology, Italy–Slovenia cross-border or European instruments are most relevant to a follow-on project?
10. Which regional companies or other research groups could provide the consortium structure required by a future call?

## 6. What we are asking for — and what we are not

We are asking for technical guidance, pointers to datasets and facilities, and an assessment of whether a future collaboration is scientifically and institutionally realistic.

We are **not** asking OGS to endorse unvalidated results, guarantee access to restricted data, provide unpaid laboratory work, sign a commitment on the spot or become a RISTANC partner retroactively.

## 7. Desired meeting outcomes

1. Preliminary view on the pilot area and HFR suitability.
2. Shortlist of independent validation datasets or named data custodians.
3. Minimum viable laboratory measurement protocol.
4. Realistic indication of laboratory/service costs and lead times.
5. Named technical contact or agreed follow-up route, if appropriate.
6. One or two plausible funding routes for a larger second phase.

## 8. Follow-up record

Complete after the meeting:

| Topic | Advice / decision | Responsible contact | Next action | Due date |
|---|---|---|---|---|
| Pilot polygon and HFR coverage |  |  |  |  |
| Independent validation data |  |  |  |  |
| Laboratory scope and quote |  |  |  |  |
| Natural samples / permits |  |  |  |  |
| Potential OGS role |  |  |  |  |
| Regional / cross-border funding |  |  |  |  |

## 9. Repository references

- [Section C project narrative](SECTION_C_DRAFT_RHEOMARINE_SLO_EN.md)
- [Application readiness and evidence dossier](APPLICATION_READINESS_EVIDENCE_DOSSIER_2026-11-25.md)
- [Slovenian territorial-sea HFR data audit](HFR_SLOVENIAN_TERRITORIAL_SEA_DATA_AUDIT_2026-11-25.md)
- [HFR live endpoint and calibration-metadata check](HFR_LIVE_ENDPOINT_AND_CALIBRATION_CHECK_2026-11-25.md)
- [Laboratory provider shortlist and quotation requests](LABORATORY_PROVIDER_SHORTLIST_AND_REQUESTS.md)
- [Funding pathways beyond RISTANC](FUNDING_PATHWAYS_BEYOND_RISTANC_2026-11-25.md)
