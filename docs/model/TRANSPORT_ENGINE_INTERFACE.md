# RheoMarine transport engine: implementation and HFR interface

Status: M0 numerical core implemented. HFR ingestion now exposes both a QC-aware Lagrangian handoff and a cell-centred Eulerian handoff. This is a computational baseline, not a calibrated or validated coastal forecast model.

## Module layout
- `src/rheomarine_transport/grid.py`: conservative finite-volume surface advection–diffusion step on a uniform Cartesian grid.
- `src/rheomarine_transport/m0.py`: Lagrangian surface advection–diffusion engine.
- `src/rheomarine_hfr/adapter.py`: ERDDAP NetCDF loading, QC, metric coordinates and temporal segmentation.
- `src/rheomarine_hfr/eulerian.py`: conversion of HFR node velocities to finite-volume cell-centred forcing.
- `tests/test_hfr_eulerian.py`: HFR-to-Eulerian conversion and end-to-end numerical handoff tests.

## HFR → Eulerian handoff

The public API is:

```python
from rheomarine_hfr import load_erddap_netcdf, to_velocity_fields, to_eulerian_forcing

dataset = load_erddap_netcdf("IZOL_subset.nc")
segments = to_velocity_fields(dataset, max_gap_s=7200.0)
forcing = to_eulerian_forcing(segments[0])

result = forcing.step(
    concentration, start_time_s=forcing.times[0],
    dt_s=1800.0, diffusivity=K_h,
)
concentration = result.concentration
```

The conversion has explicit semantics:

1. Input HFR coordinates are the local equirectangular metric node axes produced by the existing adapter. Both axes must be uniformly spaced; nonuniform axes are rejected rather than approximated by a single `dx,dy`.
2. Each finite-volume cell is the quadrilateral between four adjacent HFR nodes. Cell-centred eastward and northward velocities are the arithmetic means of the four corner-node values. On this local equirectangular grid, east/north remain aligned with x/y.
3. A cell is valid only if all four corner nodes pass the HFR QC mask. At an exact observation time only that observation's mask is required; at an intermediate time both bracketing masks must be valid.
4. Time sampling is restricted to the supplied contiguous `VelocityField` segment. There is no extrapolation and no crossing of a temporal gap.
5. Invalid cell velocities become NaN at sampling time. The existing finite-volume solver rejects non-finite fields, so QC holes cannot silently become zero current. The current solver has no wet-cell/observation-mask flux treatment: before stepping, the caller must select a rectangular subdomain that is fully QC-supported for the required time interval. No automatic hole filling is performed.

`EulerianHFRForcing.step` samples the velocity at the temporal midpoint of the requested step and delegates to `step_advection_diffusion`. The requested interval must lie entirely inside the segment. The solver's explicit stability check remains active by default.

## Solver inputs and units
| Input | Shape / units | Meaning |
|---|---|---|
| `u`, `v` | (ny,nx), m s-1 | eastward/northward surface velocity at cell centres |
| `concentration` | (ny,nx) | surface-layer concentration |
| `diffusivity` | scalar or (ny,nx), m2 s-1 | horizontal diffusivity |
| `dt` | seconds | time step |
| `Grid2D` | nx, ny, dx, dy | projected metric finite-volume grid |

## Numerical method and boundaries
- First-order upwind advective face fluxes; centred diffusive face fluxes.
- Finite-volume flux divergence; all outer boundaries currently have zero normal flux.
- Explicit advection/diffusion stability bound via `stability_timestep`.
- Materially negative post-transport states raise an error rather than being silently clipped.
- Optional source (concentration s-1) and first-order sink (s-1); sink is integrated exponentially.
- Budget: mass_after = mass_before + source_mass - sink_mass, up to floating-point roundoff.

The rectangular closed-domain boundary is a controlled numerical baseline only. Coastline/wet-cell masks, open-boundary exchange, wet/dry cells, spherical metrics, nonuniform grids, and finite-volume fluxes around HFR missing-data masks are not implemented. The Eulerian adapter therefore fails loudly on incomplete QC support rather than claiming to solve masked coastal flow.

## M1 particle properties
`ParticleClass` stores diameter, density, and optional signed settling velocity. `stokes_settling_velocity` is a spherical low-Reynolds-number reference estimate (positive downward, negative upward). It must not be applied blindly to irregular particles, aggregates, or regimes outside Stokes assumptions. Missing empirical properties remain missing.

This initial M1 layer does not implement aggregation kinetics, biofouling transitions, or a vertical water-column model. A surface-layer loss closure requires a declared layer thickness and justified vertical-mixing assumptions; it is not a measurement of seabed deposition.

## Tests
Run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

The Eulerian adapter tests cover node-to-cell conversion, uniform metric spacing, time interpolation, exact-time QC handling, rejection of temporal extrapolation, loud failure on QC holes, and an end-to-end HFR-to-solver zero-flow benchmark. Passing these tests verifies software integration on synthetic data; it does not validate the physical model against independent observations.

## Before coastal pilot use
1. Add a conservative wet-cell/QC-mask flux formulation or define and document a fully supported rectangular subdomain.
2. Implement coastline and open-boundary conditions before interpreting coastal transport.
3. Validate grid metrics and the equirectangular approximation for the selected domain.
4. Archive original vector NetCDFs, queries and hashes for IZOL/PIRA pilot reproducibility.
5. Compare against independent drifter/ADCP observations on held-out periods before claiming predictive skill.
