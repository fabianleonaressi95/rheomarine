# rheomarine

Mathematical and computational modelling of microplastic transport,
biological aggregation and rheological effects in the North Adriatic
Sea — experimental data + analysis.

## Data sources (Mendeley Data, CC BY 4.0, IG PAS)

| Dir | Dataset | Content |
|-----|---------|---------|
| `data/ds1_rheology_settling/` | Mrokowska et al. 2024 — settling of MPs in mucus-rich water column | 722 PTV trajectories (`*_run_*.csv`: x,z,t,angle), 7 solutions (AS, XG, CR, XG+CR @ 0.5/1 g/L) × 15 particle types (S/D/R/B/C/I × PS/POM/PET/PA6); particle dimension CSVs; rheology files |
| `data/ds2_stratified/` | Mrokowska et al. 2025 — MPs sinking through rheologically stratified seawater | `MPs_sinking_dynamics` (9 experiments, two-layer AS↔XG), `Density_and_refractive_index_profiles`, `Rheological_data` (flow/amplitude/gelling), transition-interface positions in README |

## Analysis so far

`scripts/extract_settling_velocities.py` — terminal settling velocity `w_s`
(linear fit on last 40% of each trajectory) for all 722 runs:

- `data/ds1_rheology_settling/settling_velocities.csv` — one row per run
- `data/ds1_rheology_settling/settling_summary.json` — mean/std per
  solution × particle type × material × size

Headline: XG reduces `w_s` strongly and concentration-dependently
(AS 0.059 → XG1 0.013, −78%); carrageenan much weaker (−16% at 1 g/L);
XG+CR intermediate. Units of z are as-recorded (README claims pixels;
absolute calibration not in dataset — open item).

## Second-pass analyses

`scripts/analyze_ds1_settling.py` — joins velocities with measured
particle dimensions (14 dim files + S_PS from README; `C_*` specs have
no dimension data in the dataset) and computes the retardation factor
`R = w_fluid / w_AS` per solution × particle spec, aggregated by
solution/material/shape, plus orientation statistics (circular spread
of the projection angle, correlation with smoothed sinking speed) for
non-spherical particles:

- `data/ds1_rheology_settling/ds1_particle_dimensions.csv`
- `data/ds1_rheology_settling/ds1_retardation.csv`
- `data/ds1_rheology_settling/ds1_analysis_summary.json`

Findings: retardation is strongly **material-dependent** — at XG 1 g/L,
POM retains about 24% of its AS-baseline settling speed (R ≈ 0.24),
whereas PS/PET/PA retain roughly 5–7% (R ≈ 0.05–0.07). POM is therefore
less retarded than the other reported materials, but it is still slower
than its own AS baseline. At XG 0.5 g/L the ordering persists (POM
R≈0.60 vs PS R≈0.24). CR alone is weaker and shows the same broad
material ordering. These are equal-weight averages over available
particle specifications, not particle-count-weighted estimates.

`scripts/analyze_ds2_stratified.py` (v2) — resamples each ensemble-averaged
centroid track onto a uniform time grid (source timestamps are jittered),
splits IW1 tracks at the visible interface bounds into above / interface /
below zones, and reports IW2 as a lower-layer reference window. Density
profiles are explicitly sorted by z before computing layer densities:

- `data/ds2_stratified/ds2_interface_transit.csv` (108 trajectories,
  zone-coverage flags)
- `data/ds2_stratified/ds2_set_iw_particle_summary.csv` (set × IW ×
  particle-type medians)
- `data/ds2_stratified/ds2_interface_summary.json`
- `analysis/DS2_V2_NOTES.md` — interpretation decisions and caveats

Findings (IW1, `R = w_below/w_above`): sets 1–2 (inferred AS-over-XG)
show strong retardation growing with Δρ — set1_3 R≈0.14, set2_3
R≈0.20 — while set3 (inferred inverted XG-over-AS) shows acceleration
below the interface (R up to ≈5.4 in set3_3). IW2 speeds match the IW1
below-interface values within ~±25% for 8/9 sets, confirming IW2 samples
only the lower layer. Rods (R) are more affected than spheres (S) in
both regimes. Layer-order assignment is inferred from the Mendeley
dataset description (6× AS-over-XG, 3× XG-over-AS) plus the set3
velocity signature — **not** verified against the paywalled paper;
exact fluid recipes remain an open item, as does the anomalous set3
bottom density (~1038 kg/m³).

## Scientific model and validation protocol

The modelling design is maintained separately from the application narrative:

- [Central research question and falsifiable hypotheses](docs/science/RESEARCH_QUESTION_AND_HYPOTHESES.md)
- [M0/M1/M2 mathematical and computational specification](docs/model/M0_M1_M2_MODEL_SPECIFICATION.md)
- [Independent validation, metrics and uncertainty protocol](docs/validation/INDEPENDENT_VALIDATION_PROTOCOL.md)

These documents define the scientific workstream independently of the ongoing HFR ingestion implementation. The HFR module should provide documented model-ready surface-current fields, QC/coverage masks and provenance; it should not implement or assume the particle-physics modules. The specifications explicitly distinguish surface transport from vertical circulation and seabed deposition, and laboratory proxies from natural marine EPS.

## Transport engine implementation

The repository currently contains two distinct M0 transport implementations; do not conflate their evidence:

- [M0/M1 transport engine and HFR interface contract](docs/model/TRANSPORT_ENGINE_INTERFACE.md)
- **Eulerian finite-volume solver:** `src/rheomarine_transport/grid.py` (`Grid2D`, `step_advection_diffusion`), a conservative advection–diffusion baseline on a uniform Cartesian grid. It currently has no HFR temporal-forcing/QC-mask adapter.
- **Lagrangian particle solver:** `src/rheomarine_transport/m0.py` (`VelocityField`, `simulate_m0`), with the HFR NetCDF adapter in `src/rheomarine_hfr/`. This path applies the documented strict QC mask, metric coordinate conversion and temporal segmentation. Its HFR pilots are particle-path sensitivity experiments, not Eulerian concentration forecasts.
- `tests/test_transport.py`, `tests/test_m0.py`, `tests/test_hfr_adapter.py` and `tests/test_hfr_trajectory.py` cover separate components; see the linked implementation and pilot reports for their actual scope.

Run with `PYTHONPATH=src python -m unittest discover -s tests -v`. Neither implementation is an independently validated coastal forecast model. The finite-volume solver still needs an explicit, fail-closed HFR/QC forcing contract, coastline/wet-cell masks, open-boundary treatment and appropriate grid metrics before a coastal concentration pilot.

## Literature review and scientific basis

The project's working scientific review is maintained directly in Markdown; it is the readable, citable synthesis and the first point of reference for project decisions. It is not necessary to start from a compiled PDF dossier.

- **[Priority literature review — RheoMarine-SLO](docs/literature/PRIORITY_LITERATURE_REVIEW_2026-11-25.md)** — critical synthesis of the technical readings, including the detailed review of Marchetto et al. (2022) and the primary Slovenian field study by Gajšt et al. (2016): HFR validation and Gulf circulation; HFR-NAdr station history; HFR-driven microplastic tracking; particle-tracking good practice; rheological settling and stratification; dataset methods; Northern Adriatic field observations; limitations and implications for WP1–WP4.
- The review includes an access audit that distinguishes full-text readings from publisher-visible article sections, abstracts, institutional records and dataset metadata. It also identifies further North Adriatic hydrodynamic papers for subsequent reading.
- Source papers and datasets are retained under `papers/` and linked from the relevant entries in the Markdown review. The PDF dossier is supplementary archival material, not the project's documentation entry point.

## RISTANC call documents

Primary sources (valid version 2):
- [Guidelines for Applicants](docs/references/ristanc/01callguidelinesforapplicantsristancv5.pdf)
- [Application Form (DOCX)](docs/references/ristanc/02applicationformristancv5.docx)
- [Evaluation Criteria](docs/references/ristanc/03evaluationcriteriaristancv5.pdf)
- [Ethical Aspects](docs/references/ristanc/04ethical-aspectsristancv5.pdf)
- [Current Q&A (5 November 2026)](https://www.ristanc.eu/storage/doc/202611/qa-ristancen-gbv3.pdf)
- [Archived earlier Q&A (20 October 2026)](docs/references/ristanc/archive/qa-ristanc-202610-20.pdf)

Reviews and working documents:
- [Call requirements audit](docs/references/ristanc/RISTANC_DOCUMENTS_AUDIT_2026-11-25.md)
- [Evaluation criteria review](docs/references/ristanc/RISTANC_EVALUATION_REVIEW_2026-11-25.md)
- [Ethical and open-science review](docs/references/ristanc/RISTANC_ETHICS_REVIEW_2026-11-25.md)
- [Application form — full text extraction](docs/references/ristanc/02_APPLICATION_FORM_FULL_TEXT.md)
- [Application form — field map](docs/references/ristanc/02_APPLICATION_FORM_FIELD_MAP.md)
- [Application form — cross-check](docs/references/ristanc/RISTANC_APPLICATION_FORM_CROSSCHECK_2026-11-25.md)
- [Section C draft — RheoMarine-SLO (English)](docs/ristanc/application-support/SECTION_C_DRAFT_RHEOMARINE_SLO_EN.md)
- [Tax and funding-agreement review](legal/RISTANC_TAX_AND_FUNDING_AGREEMENT_REVIEW_2026-11-25.md)
- Application preparation files: `docs/ristanc/application-support/`

## RISTANC readiness and territorial evidence

- [Application readiness and evidence dossier](docs/ristanc/application-support/APPLICATION_READINESS_EVIDENCE_DOSSIER_2026-11-25.md)
- [Slovenian territorial-sea HFR data audit](docs/ristanc/application-support/HFR_SLOVENIAN_TERRITORIAL_SEA_DATA_AUDIT_2026-11-25.md)
- [HFR live endpoint and calibration-metadata check](docs/ristanc/application-support/HFR_LIVE_ENDPOINT_AND_CALIBRATION_CHECK_2026-11-25.md)
- Reproducible short-window benchmark: `python scripts/audit_hfr_endpoints.py --days 1 7 --timeout 120`
- [Applicant competence evidence annex (draft)](docs/ristanc/application-support/APPLICANT_COMPETENCE_EVIDENCE_ANNEX_DRAFT.md)
- [Laboratory provider shortlist and tailored quotation requests](docs/ristanc/application-support/LABORATORY_PROVIDER_SHORTLIST_AND_REQUESTS.md)
- [OGS meeting brief — 26 November 2026](docs/ristanc/application-support/OGS_MEETING_BRIEF_2026-11-26.md)
- [Funding pathways beyond RISTANC](docs/ristanc/application-support/FUNDING_PATHWAYS_BEYOND_RISTANC_2026-11-25.md)
