"""QC-preserving adapter from HFR node fields to the Eulerian finite-volume grid.

HFR values live at rectilinear grid nodes; the finite-volume solver expects
velocities at cell centres. Each cell-centred component is the arithmetic
mean of its four corner nodes, and a cell is valid only when all four
corners are valid. Invalid cells are represented by NaN at sampling time:
the existing solver rejects non-finite forcing rather than treating missing
observations as zero current.

The adapter deliberately does not fill holes, extrapolate in time, bridge
segments, or infer coastlines/open boundaries.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from rheomarine_transport import Grid2D, TransportResult, VelocityField, step_advection_diffusion

FloatArray = NDArray[np.float64]
BoolArray = NDArray[np.bool_]


@dataclass(frozen=True)
class EulerianHFRForcing:
    """Cell-centred HFR forcing on one contiguous observation segment.

    u and v have shape (nt, ny, nx), in m/s. valid has the same shape.
    x_edges and y_edges are the source HFR node coordinates (metres);
    their adjacent pairs define the finite-volume cells.
    """

    grid: Grid2D
    x_edges: FloatArray
    y_edges: FloatArray
    times: FloatArray
    u: FloatArray
    v: FloatArray
    valid: BoolArray

    def __post_init__(self) -> None:
        x = np.asarray(self.x_edges, dtype=float)
        y = np.asarray(self.y_edges, dtype=float)
        t = np.asarray(self.times, dtype=float)
        u = np.asarray(self.u, dtype=float)
        v = np.asarray(self.v, dtype=float)
        valid = np.asarray(self.valid, dtype=bool)
        shape = (t.size, self.grid.ny, self.grid.nx)
        if x.shape != (self.grid.nx + 1,) or y.shape != (self.grid.ny + 1,):
            raise ValueError("edge coordinates must have nx+1 and ny+1 entries")
        if t.ndim != 1 or t.size < 2 or not np.all(np.diff(t) > 0):
            raise ValueError("times must be strictly increasing with at least two samples")
        if u.shape != shape or v.shape != shape or valid.shape != shape:
            raise ValueError(f"u, v and valid must have shape {shape}")
        if not (np.all(np.isfinite(x)) and np.all(np.isfinite(y))
                and np.all(np.isfinite(t))):
            raise ValueError("coordinates and times must be finite")
        if not (np.all(np.isfinite(u)) and np.all(np.isfinite(v))):
            raise ValueError("stored velocity arrays must be finite; use valid mask")
        object.__setattr__(self, "x_edges", x)
        object.__setattr__(self, "y_edges", y)
        object.__setattr__(self, "times", t)
        object.__setattr__(self, "u", u)
        object.__setattr__(self, "v", v)
        object.__setattr__(self, "valid", valid)

    @property
    def cell_center_x(self) -> FloatArray:
        """x coordinates of finite-volume cell centres (metres)."""
        return 0.5 * (self.x_edges[:-1] + self.x_edges[1:])

    @property
    def cell_center_y(self) -> FloatArray:
        """y coordinates of finite-volume cell centres (metres)."""
        return 0.5 * (self.y_edges[:-1] + self.y_edges[1:])

    def sample(self, time_s: float) -> tuple[FloatArray, FloatArray, BoolArray]:
        """Return (u, v, valid) at a time inside this segment.

        Exact observation times use only that observation's QC mask.
        Intermediate times require both bracketing observations to be valid.
        No extrapolation is permitted. Invalid output cells are NaN so the
        finite-volume solver fails loudly if they are passed to it.
        """
        time = float(time_s)
        if not np.isfinite(time) or time < self.times[0] or time > self.times[-1]:
            raise ValueError("requested time is outside this HFR segment")
        exact = int(np.searchsorted(self.times, time, side="left"))
        if exact < self.times.size and self.times[exact] == time:
            mask = self.valid[exact].copy()
            uu = self.u[exact].copy()
            vv = self.v[exact].copy()
        else:
            i1 = int(np.searchsorted(self.times, time, side="right"))
            i0 = i1 - 1
            weight = (time - self.times[i0]) / (self.times[i1] - self.times[i0])
            mask = self.valid[i0] & self.valid[i1]
            uu = (1.0 - weight) * self.u[i0] + weight * self.u[i1]
            vv = (1.0 - weight) * self.v[i0] + weight * self.v[i1]
        uu[~mask] = np.nan
        vv[~mask] = np.nan
        return uu, vv, mask

    def step(
        self,
        concentration: FloatArray,
        *,
        start_time_s: float,
        dt_s: float,
        diffusivity: float | FloatArray,
        source: float | FloatArray = 0.0,
        sink_rate: float | FloatArray = 0.0,
        enforce_stability: bool = True,
        wet: BoolArray | None = None,
        open_edges: tuple[str, ...] = (),
        qc_holes: str = "fail",
    ) -> TransportResult:
        """Advance one Eulerian step using forcing sampled at its midpoint.

        The whole step must lie within this segment. ``qc_holes`` selects
        the policy for cells whose sampled forcing is QC-invalid:

        * ``"fail"`` (default): the NaN forcing reaches the solver, which
          rejects it — the historical fail-closed behaviour.
        * ``"barrier"``: QC-invalid cells become zero-flux barriers for
          this step (conservative ``active`` mask). Tracer mass inside a
          hole is retained unchanged and resumes when QC support returns;
          no interpolation or zero-fill is performed.

        ``wet`` is an optional static land mask and ``open_edges`` an
        optional subset of {"west","east","south","north"}; see
        ``step_advection_diffusion`` for their exact semantics. With the
        defaults the step still requires every cell in the stepped domain
        to be QC-supported at the midpoint.
        """
        if qc_holes not in ("fail", "barrier"):
            raise ValueError("qc_holes must be 'fail' or 'barrier'")
        start = float(start_time_s)
        dt = float(dt_s)
        end = start + dt
        if not np.isfinite(start) or not np.isfinite(dt) or dt <= 0:
            raise ValueError("start_time_s must be finite and dt_s finite and positive")
        if start < self.times[0] or end > self.times[-1]:
            raise ValueError("Eulerian step must lie entirely within one HFR segment")
        uu, vv, mask = self.sample(start + 0.5 * dt)
        active = mask if qc_holes == "barrier" else None
        return step_advection_diffusion(
            concentration, uu, vv, diffusivity, dt, self.grid,
            source=source, sink_rate=sink_rate,
            enforce_stability=enforce_stability,
            wet=wet, active=active, open_edges=open_edges,
        )


def _uniform_spacing(axis: FloatArray, name: str) -> float:
    delta = np.diff(np.asarray(axis, dtype=float))
    if delta.size < 2 or not np.all(delta > 0):
        raise ValueError(f"{name} needs at least three strictly increasing nodes")
    spacing = float(np.mean(delta))
    if not np.allclose(delta, spacing, rtol=1e-6, atol=1e-6):
        raise ValueError(f"{name} must be uniformly spaced for Grid2D")
    return spacing


def to_eulerian_forcing(field: VelocityField) -> EulerianHFRForcing:
    """Convert one HFR VelocityField segment to cell-centred Eulerian forcing.

    The source x/y axes must be uniform metric coordinates. The finite-volume
    grid has one cell between each pair of HFR nodes. East/north components
    remain aligned with the local equirectangular x/y basis. A cell is marked
    valid only if all four surrounding HFR nodes are valid at that time.
    """
    x = np.asarray(field.x, dtype=float)
    y = np.asarray(field.y, dtype=float)
    t = np.asarray(field.times, dtype=float)
    velocity = np.asarray(field.velocity, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size < 3 or y.size < 3:
        raise ValueError("Eulerian conversion requires at least 3 HFR nodes per axis")
    if velocity.shape != (t.size, y.size, x.size, 2):
        raise ValueError("VelocityField velocity must have shape (nt, ny_nodes, nx_nodes, 2)")
    if not (np.all(np.isfinite(x)) and np.all(np.isfinite(y))
            and np.all(np.diff(x) > 0) and np.all(np.diff(y) > 0)):
        raise ValueError("HFR metric coordinates must be finite and strictly increasing")
    dx = _uniform_spacing(x, "x")
    dy = _uniform_spacing(y, "y")
    if field.valid is None:
        node_valid = np.ones((t.size, y.size, x.size), dtype=bool)
    else:
        node_valid = np.asarray(field.valid, dtype=bool)
        if node_valid.shape != (t.size, y.size, x.size):
            raise ValueError("VelocityField valid mask has inconsistent shape")

    u = 0.25 * (
        velocity[:, :-1, :-1, 0] + velocity[:, :-1, 1:, 0]
        + velocity[:, 1:, :-1, 0] + velocity[:, 1:, 1:, 0]
    )
    v = 0.25 * (
        velocity[:, :-1, :-1, 1] + velocity[:, :-1, 1:, 1]
        + velocity[:, 1:, :-1, 1] + velocity[:, 1:, 1:, 1]
    )
    valid = (
        node_valid[:, :-1, :-1] & node_valid[:, :-1, 1:]
        & node_valid[:, 1:, :-1] & node_valid[:, 1:, 1:]
    )
    grid = Grid2D(nx=x.size - 1, ny=y.size - 1, dx=dx, dy=dy)
    return EulerianHFRForcing(
        grid=grid, x_edges=x.copy(), y_edges=y.copy(), times=t.copy(),
        u=u, v=v, valid=valid,
    )
