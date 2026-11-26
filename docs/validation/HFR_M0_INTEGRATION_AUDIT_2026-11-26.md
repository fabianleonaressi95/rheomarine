# HFR–M0 integration audit and evidence status

**Audit date:** 26 November 2026  
**Repository basis:** `main` after the merge of PR #18 and the HFR/M0 implementation commits  
**Scope:** reconcile the existing HFR ingestion, Lagrangian and Eulerian transport interfaces, pilot evidence, tests, and remaining physical-validation gates. No HFR ingestion files or endpoint-audit outputs are rewritten by this audit.

## 1. Verified implementation on main

### HFR ingestion and Lagrangian M0

The existing package `src/rheomarine_hfr/` is the single HFR handoff; do not create a duplicate ingestion pipeline.

- `adapter.py` reads ERDDAP NetCDF subsets with the expected `time`, `latitude`, `longitude`, `EWCT`, `NSCT`, and `QCflag` variables.
- The adapter converts geographic coordinates to a local equirectangular metric grid, retains east/north velocity components in m/s, applies the strict default `QCflag == 1` policy plus finite/fill/velocity-envelope checks, and segments time so no field spans a large observation gap or an all-invalid timestamp.
- The Lagrangian output is a QC-masked `rheomarine_transport.VelocityField`, consumed by `simulate_m0`. Invalid placeholders remain masked and must not be interpreted as measured zero currents.
- `trajectory.py` adds endpoint and exact pathwise QC checks. A step crossing an invalid cell is rejected; QC rejection and artificial crop-boundary exit are recorded separately.
- The NetCDF loader's timestamp-ordering regression is covered: the same stable permutation is applied to time, EWCT, NSCT and QCflag.

### Eulerian finite-volume M0

The HFR-to-Eulerian adapter is already implemented on `main`; it is not an outstanding design-only task.

- `src/rheomarine_hfr/eulerian.py` defines `EulerianHFRForcing` and `to_eulerian_forcing`.
- It converts the node-based `VelocityField` to cell-centred forcing by averaging the four corner-node velocities. A cell is valid only when all four corner nodes are valid.
- It requires at least three nodes per axis and uniform metric spacing, and rejects nonuniform grids instead of silently approximating them.
- Exact observation times use that observation's QC mask; intermediate times require both bracketing observations to be valid. Sampling outside the segment is rejected.
- QC-invalid cell values become NaN at sampling time. The finite-volume solver rejects non-finite forcing; no zero-fill, gap bridging, or coastline inference is performed.
- `EulerianHFRForcing.step` samples at the time midpoint and calls the existing conservative finite-volume solver.

**Update 26 Nov 2026 (later same day):** the wet-cell/QC-mask/open-boundary solver options are implemented in PR #20 (`feat/eulerian-coastal-boundaries`), pending merge; the raw seven-day inputs were recovered, checksum-verified, published as release assets and reproduced bit-identically — see PR #21 and `docs/hfr/M0_PILOT_REPRODUCTION_2026-11-26.md`. Independent physical validation remains **BLOCKED** (gate §5.3–5.5 unchanged).

**Important remaining numerical/domain limitation (pre-PR#20 state):** the finite-volume solver uses a uniform Cartesian metric grid. PR #20 adds `wet` land masks, per-step `active` QC-barrier masks and `open_edges` zero-gradient exchange; it does **not** add spherical/nonuniform metrics, wet/dry fronts, or an authoritative coastline product. A coastline `wet` mask must still be supplied from an external source, and open boundaries remain a documented first-order closure, not a validated open-ocean condition.

## 2. Software verification

The GitHub Actions run associated with PR #18 executed:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

- Python: 3.11.18
- Result: 45 tests run, all passed
- Exit code: 0
- Run: https://github.com/fabianleonaressi95/rheomarine/actions/runs/45854557740

The suite includes the synthetic NetCDF timestamp-alignment regression, Lagrangian QC/path tests, and `tests/test_hfr_eulerian.py` for node-to-cell conversion, uniform metric spacing, time interpolation, exact-time QC handling, no temporal extrapolation, fail-closed QC holes, and an end-to-end zero-flow handoff with mass conservation.

This is software verification on synthetic and unit-test inputs. It does not establish HFR measurement accuracy, physical validity, or predictive skill.

**Update:** the local suite now runs **64 tests** (45 baseline + 19 boundary/mask tests from PR #20), all passing on Python 3.10.12 / numpy 2.2.6 / scipy 1.15.3; CI results for PRs #20–#21 are reported on those PRs.

## 3. IZOL and PIRA pilot evidence already in the repository

The pilot work is documented in:

- `docs/hfr/M0_HFR_PILOT_2026-11-25.md`
- `docs/hfr/INDEPENDENT_M0_PILOT_AUDIT_2026-11-25.md`
- `docs/validation/HFR_PILOT_SCIENTIFIC_VALIDATION_GATE_2026-11-25.md`

The reports describe separate IZOL and PIRA seven-day HFR subsets, QC-aware Lagrangian K=0 runs, and regenerated audit variants (block-4 reflect, block-8 reflect, block-4 absorb). They record source-file hashes, segment windows, release counts, QC-stopped/exited counts, and displacement summaries. The raw `data/hfr/raw/*_7d.nc` NetCDF inputs are git-ignored in the repository but were recovered locally, checksum-verified and published as release assets — see §5.1 and `docs/hfr/M0_PILOT_REPRODUCTION_2026-11-26.md`. The separate QCflag archive under `data/hfr/` is not a substitute for the EWCT/NSCT forcing subsets.

The reported runs are numerical surface-advection sensitivity experiments. In particular, reflect/absorb differences demonstrate strong sensitivity to the artificial crop boundary. They must not be described as coastal retention estimates, Eulerian concentration forecasts, vertical transport, or seabed deposition.

## 4. Morandotti compatibility decision

`docs/model/MORANDOTTI_MICROSWIMMER_COMPATIBILITY.md` records the literature assessment.

The Stokes/Brinkman microswimmer results concern active, shape-changing biological swimmers with position/orientation dynamics and self-propulsion constraints. They are not equations for passive microplastic transport. Decision: keep them outside M0; consider only a separate active-biological-particle module if organism-specific kinematics, a scale-consistent fluid model, parameters, and independent observations become available.

## 5. Remaining gates — not silently marked complete

1. **Reproducible raw-data rerun:** ~~restore the exact IZOL/PIRA seven-day NetCDF inputs~~ — **DONE 26 Nov 2026**: inputs recovered at `data/hfr/raw/`, SHA-256 verified against the values embedded in the committed reports, published as release `hfr-m0-pilot-inputs-2026-11-25`, and the pilot rerun reproduces `results/hfr_pilot_audit/` **bit-identically** (`docs/hfr/M0_PILOT_REPRODUCTION_2026-11-26.md`, PR #21). Evidence label: **PILOT-REPRODUCED** (Lagrangian K=0 sensitivity experiment).
2. **Eulerian coastal-domain readiness:** ~~implement and test wet-cell/coastline masks, open-boundary exchange, and a defensible policy for internal QC holes~~ — **IMPLEMENTED + SOFTWARE-VERIFIED in PR #20** (`wet`/`active`/`open_edges`, `qc_holes="fail"|"barrier"`, 19 new tests, suite 64/64 locally). Still required before a coastal pilot: an authoritative coastline mask, a declared boundary design, and grid-metric validation for the chosen domain. Spherical/nonuniform metrics and wet/dry fronts remain unimplemented.
3. **Independent hydrodynamic validation:** compare HFR currents against contemporaneous independent ADCP, buoy, or drifter observations where compatible data can be obtained. **Status: BLOCKED — DATA-BLOCKED** (no compatible observations in hand; requests pending per validation-gate §8).
4. **Independent particle-transport validation:** obtain observations that measure the same endpoint as the model (particle trajectories or concentrations) with compatible size cutoffs, depth, time, and spatial support. **Status: BLOCKED — DATA-BLOCKED** (Gajšt et al. 2016 sample-level data not public; request pending).
5. **Predictive skill:** predeclare held-out evaluation periods/locations and metrics before tuning. **Status: BLOCKED** — cannot be assessed until gates 3–4 produce data; do not mark satisfied from software tests.

## 6. Status summary

| Work item | Status | Evidence / boundary |
|---|---|---|
| Existing HFR ingestion preserved | IMPLEMENTED | `src/rheomarine_hfr/adapter.py` |
| HFR → Lagrangian M0 | IMPLEMENTED, SOFTWARE-VERIFIED | `VelocityField`, `simulate_qc_aware`, tests and pilot reports |
| HFR → Eulerian finite-volume M0 | IMPLEMENTED, SOFTWARE-VERIFIED | `eulerian.py`, `test_hfr_eulerian.py`; rectangular fully-QC domains by default, `qc_holes="barrier"` opt-in (PR #20) |
| Eulerian coastal boundaries (wet mask, QC barrier, open edges) | IMPLEMENTED, SOFTWARE-VERIFIED (PR #20 pending merge) | `grid.py` `wet`/`active`/`open_edges`, `tests/test_eulerian_boundaries.py`; coastline mask still caller-supplied |
| IZOL/PIRA Lagrangian sensitivity pilots | PILOT-REPRODUCED | 7-day reports + bit-identical rerun, `docs/hfr/M0_PILOT_REPRODUCTION_2026-11-26.md`, release `hfr-m0-pilot-inputs-2026-11-25` |
| Morandotti compatibility assessment | Completed as literature/scope note | `docs/model/MORANDOTTI_MICROSWIMMER_COMPATIBILITY.md` |
| Independent hydrodynamic validation | DATA-BLOCKED | Requires independent compatible current observations |
| Independent particle-transport validation | DATA-BLOCKED | Requires trajectory/concentration observations |
| Coastal predictive validation | OPEN / BLOCKED | Requires domain boundaries, held-out observations and predeclared metrics |

