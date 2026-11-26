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

**Important remaining numerical/domain limitation:** the finite-volume solver currently uses a uniform Cartesian metric grid and zero-normal-flux outer boundaries. It does not implement wet-cell/coastline masks, open-boundary exchange, wet/dry treatment, spherical/nonuniform metrics, or fluxes around internal QC holes. Consequently, a complete Eulerian step requires a rectangular subdomain that is QC-valid for the sampled interval; otherwise it fails closed. This is a safe software handoff, not yet a coastal-domain solver.

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

## 3. IZOL and PIRA pilot evidence already in the repository

The pilot work is documented in:

- `docs/hfr/M0_HFR_PILOT_2026-11-25.md`
- `docs/hfr/INDEPENDENT_M0_PILOT_AUDIT_2026-11-25.md`
- `docs/validation/HFR_PILOT_SCIENTIFIC_VALIDATION_GATE_2026-11-25.md`

The reports describe separate IZOL and PIRA seven-day HFR subsets, QC-aware Lagrangian K=0 runs, and regenerated audit variants (block-4 reflect, block-8 reflect, block-4 absorb). They record source-file hashes, segment windows, release counts, QC-stopped/exited counts, and displacement summaries. The raw `data/hfr/raw/*_7d.nc` NetCDF inputs are git-ignored; they are not embedded in this repository snapshot. The separate QCflag archive under `data/hfr/` is not a substitute for the EWCT/NSCT forcing subsets.

The reported runs are numerical surface-advection sensitivity experiments. In particular, reflect/absorb differences demonstrate strong sensitivity to the artificial crop boundary. They must not be described as coastal retention estimates, Eulerian concentration forecasts, vertical transport, or seabed deposition.

## 4. Morandotti compatibility decision

`docs/model/MORANDOTTI_MICROSWIMMER_COMPATIBILITY.md` records the literature assessment.

The Stokes/Brinkman microswimmer results concern active, shape-changing biological swimmers with position/orientation dynamics and self-propulsion constraints. They are not equations for passive microplastic transport. Decision: keep them outside M0; consider only a separate active-biological-particle module if organism-specific kinematics, a scale-consistent fluid model, parameters, and independent observations become available.

## 5. Remaining gates — not silently marked complete

1. **Reproducible raw-data rerun:** restore the exact IZOL/PIRA seven-day NetCDF inputs (or retrieve fresh, versioned subsets), verify checksums and endpoint metadata, then rerun the documented pilots. The git-ignored inputs are not present in the repository snapshot inspected for this audit.
2. **Eulerian coastal-domain readiness:** implement and test wet-cell/coastline masks, open-boundary exchange, and a defensible policy for internal QC holes; validate grid metrics for the selected pilot domain. Until then, restrict Eulerian steps to fully QC-supported rectangular subdomains and closed-box interpretation.
3. **Independent hydrodynamic validation:** compare HFR currents against contemporaneous independent ADCP, buoy, or drifter observations where compatible data can be obtained.
4. **Independent particle-transport validation:** obtain observations that measure the same endpoint as the model (particle trajectories or concentrations) with compatible size cutoffs, depth, time, and spatial support. HFR forcing alone is not validation of particle transport.
5. **Predictive skill:** predeclare held-out evaluation periods/locations and metrics before tuning. If suitable independent particle observations are unavailable, report only process/sensitivity analysis and mark predictive validation as not established.

## 6. Status summary

| Work item | Status | Evidence / boundary |
|---|---|---|
| Existing HFR ingestion preserved | Implemented | `src/rheomarine_hfr/adapter.py` |
| HFR → Lagrangian M0 | Implemented and software-tested | `VelocityField`, `simulate_qc_aware`, tests and pilot reports |
| HFR → Eulerian finite-volume M0 | Implemented and software-tested | `eulerian.py`, `test_hfr_eulerian.py`; restricted to uniform, fully QC-valid rectangular domains |
| IZOL/PIRA Lagrangian sensitivity pilots | Previously executed and documented | 7-day pilot report and independent audit; raw input files git-ignored |
| Morandotti compatibility assessment | Completed as literature/scope note | `docs/model/MORANDOTTI_MICROSWIMMER_COMPATIBILITY.md` |
| Independent physical validation | Not established | Requires independent compatible observations |
| Coastal predictive validation | Not established | Requires domain boundaries, held-out observations and predeclared metrics |

