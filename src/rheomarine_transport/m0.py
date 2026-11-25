"""M0 stochastic Lagrangian surface advection-diffusion model.

Coordinates, time and velocities must use one consistent unit system.
The velocity array has shape (time, y, x, component), with components (u, v).
Invalid/QC-failed cells are never silently interpolated or replaced by zero.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import NDArray

BoundaryMode = Literal["reflect", "absorb"]


@dataclass(frozen=True)
class VelocityField:
    """Rectilinear, time-dependent surface velocity forcing.

    Attributes:
        x, y: strictly increasing 1-D grid coordinates.
        times: strictly increasing forcing times.
        velocity: (nt, ny, nx, 2) array; final axis is (u, v).
        valid: optional boolean QC mask with shape (nt, ny, nx).
    """

    x: NDArray[np.float64]
    y: NDArray[np.float64]
    times: NDArray[np.float64]
    velocity: NDArray[np.float64]
    valid: NDArray[np.bool_] | None = None

    def __post_init__(self) -> None:
        x = np.asarray(self.x, dtype=float)
        y = np.asarray(self.y, dtype=float)
        t = np.asarray(self.times, dtype=float)
        u = np.asarray(self.velocity, dtype=float)
        if x.ndim != 1 or y.ndim != 1 or t.ndim != 1:
            raise ValueError("x, y and times must be one-dimensional")
        if min(x.size, y.size, t.size) < 2:
            raise ValueError("each grid axis and the time axis need at least two points")
        if not (np.all(np.diff(x) > 0) and np.all(np.diff(y) > 0)
                and np.all(np.diff(t) > 0)):
            raise ValueError("x, y and times must be strictly increasing")
        if u.shape != (t.size, y.size, x.size, 2):
            raise ValueError("velocity must have shape (nt, ny, nx, 2)")
        if not np.all(np.isfinite(u)):
            raise ValueError("velocity contains non-finite values; use valid mask and finite data")
        mask = self.valid
        if mask is not None and np.asarray(mask).shape != (t.size, y.size, x.size):
            raise ValueError("valid mask must have shape (nt, ny, nx)")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "times", t)
        object.__setattr__(self, "velocity", u)
        if mask is not None:
            object.__setattr__(self, "valid", np.asarray(mask, dtype=bool))

    def sample(self, positions: NDArray[np.float64], time: float) -> NDArray[np.float64]:
        """Bilinearly interpolate velocity in space and linearly in time.

        Raises ValueError if a particle is outside forcing coverage or any
        interpolation corner fails QC. No extrapolation or gap filling occurs.
        """
        p = np.asarray(positions, dtype=float)
        if p.ndim != 2 or p.shape[1] != 2:
            raise ValueError("positions must have shape (n, 2)")
        if time < self.times[0] or time > self.times[-1]:
            raise ValueError("requested time is outside forcing coverage")
        if np.any(p[:, 0] < self.x[0]) or np.any(p[:, 0] > self.x[-1]) \
                or np.any(p[:, 1] < self.y[0]) or np.any(p[:, 1] > self.y[-1]):
            raise ValueError("particle lies outside forcing coverage")

        it1 = min(int(np.searchsorted(self.times, time, side="right")), len(self.times)-1)
        it0 = max(it1 - 1, 0)
        wt = (time - self.times[it0]) / (self.times[it1] - self.times[it0])
        ix1 = np.clip(np.searchsorted(self.x, p[:, 0], side="right"), 1, len(self.x)-1)
        iy1 = np.clip(np.searchsorted(self.y, p[:, 1], side="right"), 1, len(self.y)-1)
        ix0, iy0 = ix1 - 1, iy1 - 1
        wx = (p[:, 0] - self.x[ix0]) / (self.x[ix1] - self.x[ix0])
        wy = (p[:, 1] - self.y[iy0]) / (self.y[iy1] - self.y[iy0])

        def spatial(field: NDArray[np.float64], it: int) -> NDArray[np.float64]:
            corners = ((iy0, ix0), (iy0, ix1), (iy1, ix0), (iy1, ix1))
            if self.valid is not None and any(
                not np.all(self.valid[it, iy, ix]) for iy, ix in corners
            ):
                raise ValueError("interpolation stencil intersects a QC-invalid HFR cell")
            f00 = field[it, iy0, ix0]
            f10 = field[it, iy0, ix1]
            f01 = field[it, iy1, ix0]
            f11 = field[it, iy1, ix1]
            return ((1-wx)*(1-wy))[:, None]*f00 + (wx*(1-wy))[:, None]*f10 \
                + ((1-wx)*wy)[:, None]*f01 + (wx*wy)[:, None]*f11

        v0 = spatial(self.velocity, it0)
        if it0 == it1:
            return v0
        v1 = spatial(self.velocity, it1)
        return (1-wt)*v0 + wt*v1


@dataclass(frozen=True)
class SimulationResult:
    """Particle positions and auditable number bookkeeping."""

    initial_positions: NDArray[np.float64]
    final_positions: NDArray[np.float64]
    active: NDArray[np.bool_]
    exited: NDArray[np.bool_]
    history: NDArray[np.float64]
    times: NDArray[np.float64]
    initial_count: int
    active_count: int
    exited_count: int
    surface_loss_count: int

    @property
    def number_balance_residual(self) -> int:
        return self.initial_count - self.active_count - self.exited_count - self.surface_loss_count


def _reflect(values: NDArray[np.float64], lower: float, upper: float) -> NDArray[np.float64]:
    width = upper - lower
    z = np.mod(values - lower, 2*width)
    return lower + np.where(z <= width, z, 2*width-z)


def simulate_m0(
    forcing: VelocityField,
    initial_positions: NDArray[np.float64],
    *,
    start_time: float,
    end_time: float,
    dt: float,
    diffusivity: float | NDArray[np.float64] = 0.0,
    boundary: BoundaryMode = "reflect",
    surface_loss_rate: float = 0.0,
    seed: int = 0,
    max_forcing_gap: float | None = None,
) -> SimulationResult:
    """Advance passive particles using Euler-Maruyama.

    diffusivity is a scalar K (isotropic) or a symmetric 2x2 tensor in
    coordinate_units**2 / time_unit. surface_loss_rate is an optional
    first-order hazard (1/time_unit); it removes particles from the modelled
    surface layer, not from the ocean and not as measured seabed deposition.

    max_forcing_gap is the largest permitted interval between adjacent HFR
    timestamps, in the same time unit as forcing.times. By default it is
    1.5 times the median sampling interval. Any integration step whose time
    interval intersects a larger observational gap is rejected. Set an
    explicit value only when justified by the forcing product and study design.
    """
    p0 = np.asarray(initial_positions, dtype=float)
    if p0.ndim != 2 or p0.shape[1] != 2 or not np.all(np.isfinite(p0)):
        raise ValueError("initial_positions must be a finite (n, 2) array")
    if start_time < forcing.times[0] or end_time > forcing.times[-1] or end_time <= start_time:
        raise ValueError("simulation interval must lie within forcing time coverage")
    if dt <= 0 or surface_loss_rate < 0:
        raise ValueError("dt must be positive and surface_loss_rate non-negative")
    median_interval = float(np.median(np.diff(forcing.times)))
    gap_limit = 1.5 * median_interval if max_forcing_gap is None else float(max_forcing_gap)
    if not np.isfinite(gap_limit) or gap_limit <= 0:
        raise ValueError("max_forcing_gap must be finite and positive")
    forcing_gaps = np.diff(forcing.times)
    large_gap_indices = np.flatnonzero(forcing_gaps > gap_limit)
    if boundary not in ("reflect", "absorb"):
        raise ValueError("boundary must be 'reflect' or 'absorb'")
    if np.any(p0[:, 0] < forcing.x[0]) or np.any(p0[:, 0] > forcing.x[-1]) \
            or np.any(p0[:, 1] < forcing.y[0]) or np.any(p0[:, 1] > forcing.y[-1]):
        raise ValueError("initial particles must lie inside the domain")

    k = np.asarray(diffusivity, dtype=float)
    if k.ndim == 0:
        if not np.isfinite(k) or k < 0:
            raise ValueError("scalar diffusivity must be finite and non-negative")
        chol = np.eye(2) * np.sqrt(k)
    elif k.shape == (2, 2):
        if not np.allclose(k, k.T) or np.min(np.linalg.eigvalsh(k)) < -1e-12:
            raise ValueError("diffusivity tensor must be symmetric positive semidefinite")
        eigval, eigvec = np.linalg.eigh(k)
        chol = eigvec @ np.diag(np.sqrt(np.maximum(eigval, 0.0)))
    else:
        raise ValueError("diffusivity must be a scalar or 2x2 tensor")

    rng = np.random.default_rng(seed)
    n = len(p0)
    pos = p0.copy()
    active = np.ones(n, dtype=bool)
    exited = np.zeros(n, dtype=bool)
    lost = np.zeros(n, dtype=bool)
    times = np.arange(start_time, end_time, dt)
    times = np.append(times, end_time) if times.size == 0 or times[-1] < end_time else times
    history = np.full((len(times), n, 2), np.nan)
    history[0] = pos

    for step in range(len(times)-1):
        t = float(times[step])
        t_next = float(times[step+1])
        h = t_next - t
        # Do not integrate across an observational gap, even if both step
        # endpoints happen to lie in otherwise well-sampled intervals.
        if large_gap_indices.size:
            gap_left = forcing.times[large_gap_indices]
            gap_right = forcing.times[large_gap_indices + 1]
            crosses_gap = (gap_left < t_next) & (gap_right > t)
            if np.any(crosses_gap):
                j = int(np.flatnonzero(crosses_gap)[0])
                raise ValueError(
                    "simulation step intersects an HFR forcing gap "
                    f"({gap_left[j]:g} to {gap_right[j]:g}; "
                    f"duration {gap_right[j]-gap_left[j]:g} exceeds "
                    f"max_forcing_gap={gap_limit:g})"
                )
        ids = np.flatnonzero(active)
        if ids.size == 0:
            history[step+1] = pos
            continue
        velocity = forcing.sample(pos[ids], t)
        noise = np.sqrt(2*h) * (rng.standard_normal((ids.size, 2)) @ chol.T)
        candidate = pos[ids] + velocity*h + noise

        outside = ((candidate[:, 0] < forcing.x[0]) | (candidate[:, 0] > forcing.x[-1])
                   | (candidate[:, 1] < forcing.y[0]) | (candidate[:, 1] > forcing.y[-1]))
        if boundary == "absorb":
            exited_ids = ids[outside]
            exited[exited_ids] = True
            active[exited_ids] = False
            keep = ~outside
            pos[ids[keep]] = candidate[keep]
        else:
            candidate[:, 0] = _reflect(candidate[:, 0], forcing.x[0], forcing.x[-1])
            candidate[:, 1] = _reflect(candidate[:, 1], forcing.y[0], forcing.y[-1])
            pos[ids] = candidate

        survivors = np.flatnonzero(active)
        if surface_loss_rate > 0 and survivors.size:
            remove = rng.random(survivors.size) < (1.0 - np.exp(-surface_loss_rate*h))
            lost_ids = survivors[remove]
            lost[lost_ids] = True
            active[lost_ids] = False
        history[step+1] = pos

    return SimulationResult(
        initial_positions=p0.copy(), final_positions=pos.copy(), active=active,
        exited=exited, history=history, times=times, initial_count=n,
        active_count=int(active.sum()), exited_count=int(exited.sum()),
        surface_loss_count=int(lost.sum()),
    )
