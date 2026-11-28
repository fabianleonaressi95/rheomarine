# HFR quantitative coverage and data-readiness evidence — 28 November 2026

**Project:** RheoMarine-SLO  
**Purpose:** supply quantitative, auditable HFR evidence for RISTANC Section C and the C6 competence annex.  
**Evidence status:** measured data-access/QC statistics and reproducible pilot processing; not a full coastal coverage validation.

## 1. Data products and nominal grid

| Node | Operator | Dataset | Verified archive span in audit | Nominal grid |
|---|---|---|---|---:|
| Izola (IZOL) | NIB | EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3 | 2022-11-24 to 2026-11-25 (verified local QC archive) | 20 × 22 = 440 cells |
| Piran (PIRA) | ARSO | EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3 | 2021-01-01 onward in catalogue; seven-day pilot retrieved 18–25 Nov 2026 | 20 × 22 = 440 cells |

Both products expose eastward/northward surface-current components and QC flags. Nominal sampling is 30 minutes, but the time axes are irregular. HFR represents the upper approximately 0.3–2.5 m and is not a full-depth circulation product.

## 2. Quantified QC and coverage indicators

| Indicator | IZOL | PIRA | Interpretation |
|---|---:|---:|---|
| Seven-day pilot timestamps (18–25 Nov 2026) | 337 | 325 | Observed timestamps; not assumed regular or gap-free |
| Mean valid-cell fraction in selected 4×4 computational subregion | 88.43% | 93.40% | Mean of per-cell validity in the selected subregion; not whole-grid coverage |
| Strict QC acceptance (QCflag == 1) over recent 30-day full-grid denominator | ~51% | ~25% | Full nominal grid × timestamps, including empty cells; not accuracy estimates |
| Historical gaps >1 hour | 69 in verified IZOL archive | ~2,008 in catalogue audit | Different archive spans; gap count is not a direct quality score |
| Maximum observed outage in audit | ~65 days | ~51 days | Demonstrates need for explicit temporal-gap handling |

The 4×4 subregions used in the pilot were computationally selected for a reproducible sensitivity experiment. Their coordinate ranges are:

- IZOL: 45.55385–45.59435°N, 13.52950–13.58744°E.
- PIRA: 45.55385–45.59435°N, 13.56812–13.62606°E.

These are separate selected windows. Their bounding boxes overlap in longitude only over approximately 13.56812–13.58744°E; this is **not** proof that a contiguous, valid, simultaneous common-vector footprint exists across the Slovenian coastal strip. A cell-by-cell common-mask intersection and geographic clipping against the official Slovenian territorial-sea boundary remain required before fixing the final pilot polygon.

## 3. Reproduced computational pilot — scope and limits

The seven-day input files were checksum-verified and the Lagrangian K=0 pilot was reproduced bit-identically from the committed inputs. The pilot used 64 initial particles per segment, accepted only QCflag == 1, and used a maximum temporal gap threshold of 10,800 s. The longest analysed segment was 70.5 h. In the block-4 reflecting-boundary sensitivity run, the longest-segment active-only median displacement was 3.34 km for IZOL and 2.56 km for PIRA.

These are conditional surface-advection sensitivity outputs in artificially bounded computational windows. The reflecting perimeter is not a physical coastline. The pilot does not establish predictive skill, concentration, retention, vertical transport, settling or seabed deposition. An absorbing-boundary sensitivity run caused all particles in the longest segment to exit the 4×4 crop, demonstrating that results are boundary-sensitive. The project will therefore not describe the pilot as a validated coastal forecast.

## 4. RISTANC-ready quantitative wording

> The project has identified two public HFR surface-current products directly relevant to the Slovenian coastal pilot: Izola (NIB) and Piran (ARSO), each distributed on a nominal 20×22 grid (440 cells) at nominal 30-minute resolution. A seven-day subset retrieved for 18–25 November 2026 contained 337 IZOL and 325 PIRA timestamps, confirming usable recent data streams but also irregular sampling. In a reproducible pilot extraction, the selected 4×4 computational subregions showed mean cell-validity fractions of 88.43% (IZOL) and 93.40% (PIRA). Over the more extensive recent 30-day full-grid audit, strict QCflag == 1 acceptance was approximately 51% for IZOL and 25% for PIRA, with empty cells included in the denominator. The project will therefore prioritise IZOL for the initial forcing window and use PIRA as a complementary source subject to stricter QC screening. These figures are data-readiness indicators, not accuracy estimates or proof of continuous coverage across the entire Slovenian coast. The final pilot polygon will be selected only after a common valid-cell/time mask is intersected with the official territorial boundary. HFR will constrain surface transport only; vertical transport and seabed deposition will require independent evidence or explicitly labelled model assumptions.

## 5. WP1 quantitative acceptance criteria

1. Generate a time × latitude × longitude validity mask for both datasets using documented provider QC semantics; missing/fill values are never converted to zero current.
2. Report, for each candidate polygon and month: timestamp availability, per-cell valid fraction, strict QC acceptance, maximum temporal gap and simultaneous IZOL/PIRA overlap.
3. Clip candidate cells to the official Slovenian territorial-sea boundary; report cell counts and area fractions only after this geometric intersection is executed.
4. Select the smallest contiguous area meeting a predeclared coverage threshold; if no area meets it, narrow the scope or use one node and state the limitation.
5. Keep calibration and independent validation windows separate; identify independent observations for each claimed validation metric.

## 6. Source artefacts

- docs/hfr/README.md
- docs/hfr/M0_PILOT_REPRODUCTION_2026-11-26.md
- docs/hfr/INDEPENDENT_M0_PILOT_AUDIT_2026-11-25.md
- results/hfr_pilot_audit/pilot_report.json
- results/hfr_pilot_audit/IZOL_v3_7d_summary.json
- results/hfr_pilot_audit/PIRA_v3_7d_summary.json
- docs/ristanc/application-support/HFR_SLOVENIAN_TERRITORIAL_SEA_DATA_AUDIT_2026-11-25.md

**Conclusion:** the application can now report measured QC and pilot-subregion availability quantitatively, while remaining explicit that full territorial polygon coverage and independent physical validation are still WP1/WP3 tasks.