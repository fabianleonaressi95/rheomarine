# RheoMarine transport engine: implementation and HFR interface

Status: initial M0 numerical core implemented; M1 particle-property primitives included. This is a computational baseline, not a calibrated or validated coastal forecast model.

## Module layout
- `src/rheomarine_transport/grid.py`: conservative finite-volume surface advection–diffusion step on a uniform Cartesian grid.
- `src/rheomarine_transport/particles.py`: particle-class metadata and signed spherical Stokes reference velocity.
- `tests/test_transport.py`: deterministic numerical/unit tests.

## Stable handoff from HFR ingestion
The transport engine does not read ERDDAP, NetCDF, QC flags, or HFR archives. The caller supplies at each model step:
| Input | Shape / units | Meaning |
|---|---|---|
| `u` | (ny,nx), m s-1 | eastward surface velocity at cell centres |
| `v` | (ny,nx), m s-1 | northward surface velocity at cell centres |
| `concentration` | (ny,nx) | surface-layer concentration |
| `diffusivity` | scalar or (ny,nx), m2 s-1 | horizontal diffusivity |
| `dt` | seconds | time step |
| `Grid2D` | nx, ny, dx, dy | projected metric grid |

Example:
```python
from rheomarine_transport import Grid2D, step_advection_diffusion
grid = Grid2D(nx=u.shape[1], ny=u.shape[0], dx=1000.0, dy=1000.0)
result = step_advection_diffusion(C, u, v, K_h, dt_seconds, grid)
C = result.concentration
```

The HFR adapter must perform QC-aware interpolation, rotate east/north components into the projected grid basis where necessary, and provide a consistent mask/domain policy. No HFR-specific assumptions are embedded in this package.

## Numerical method and boundaries
- First-order upwind advective face fluxes; centred diffusive face fluxes.
- Finite-volume flux divergence; all outer boundaries currently have zero normal flux.
- Explicit advection/diffusion stability bound via `stability_timestep`.
- Materially negative post-transport states raise an error rather than being silently clipped.
- Optional source (concentration s-1) and first-order sink (s-1); sink is integrated exponentially.
- Budget: mass_after = mass_before + source_mass - sink_mass, up to floating-point roundoff.

The rectangular closed-domain boundary is a controlled numerical baseline only. Coastline/wet-cell masks, open-boundary exchange, wet/dry cells, spherical metrics, nonuniform grids, and HFR missing-data masks are not yet implemented.

## M1 particle properties
`ParticleClass` stores diameter, density, and optional signed settling velocity. `stokes_settling_velocity` is a spherical low-Reynolds-number reference estimate (positive downward, negative upward). It must not be applied blindly to irregular particles, aggregates, or regimes outside Stokes assumptions. Missing empirical properties remain missing.

This initial M1 layer does not implement aggregation kinetics, biofouling transitions, or a vertical water-column model. A surface-layer loss closure requires a declared layer thickness and justified vertical-mixing assumptions; it is not a measurement of seabed deposition.

## Run tests
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Before pilot use
1. Use a projected metric grid; longitude/latitude degrees are not valid dx,dy.
2. Implement coastline/wet-cell masks and open-boundary conditions before a real coastal pilot.
3. Add variable-grid metrics and robust handling of irregular HFR sampling.
4. Verify the stability bound against actual field magnitudes and select dt accordingly.
5. Compare benchmark cases with an established solver before claiming model validation.
6. Do not interpret closed-box mass balance as validation against observations.
