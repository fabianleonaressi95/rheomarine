"""HFR -> M0 adapter: convert European HFR Node NetCDF subsets into
:class:`rheomarine_transport.VelocityField` objects.

Coordinate convention
---------------------
Source data are geographic (EPSG:4326): latitude/longitude in degrees,
EWCT/NSCT in m s-1 (eastward/northward), time in seconds since
1970-01-01T00:00:00Z (verified against dataset metadata).

The adapter projects lon/lat to a local equirectangular metric grid in
metres, centred on the subset bbox centre:

    x = R * cos(lat0) * (lon - lon0) * pi/180
    y = R * (lat - lat0) * pi/180
    R = 6371000 m (mean Earth radius)

For the ~30 km HFR subsets used here this is accurate to well below the
~1.5 km grid spacing; it is NOT a rigorous equal-area or conformal
projection and must be revisited for larger domains.

QC policy
---------
A cell contributes to ``valid`` only if ALL of the following hold:
  * QCflag is in ``accepted_qc_flags`` (default {1} = "good_data" only;
    flags 2/8 exist in the flag table but are not accepted by default);
  * EWCT and NSCT are not the NetCDF fill value (-32.767) and are finite;
  * |velocity| <= 10 m/s (dataset valid_min/valid_max envelope).

Cells failing QC keep a placeholder velocity of 0.0 in the array (the
``VelocityField`` contract requires finite values) but are masked out by
``valid=False``. ``VelocityField.sample`` raises if an interpolation
stencil touches an invalid cell, so placeholders are never used in
trajectories. Missing data are never replaced by observed zeros.

Temporal gaps
-------------
``build_segments`` splits the time axis wherever the gap between
consecutive *observed* timestamps exceeds ``max_gap_s``. Each returned
``VelocityField`` covers one contiguous observation segment, so the M0
engine can never interpolate a trajectory across an unobserved interval.
Linear interpolation between consecutive observed timestamps within a
segment is the documented approximation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.io import netcdf_file

from rheomarine_transport import VelocityField

EARTH_RADIUS_M = 6_371_000.0
EWCT_FILL = -32.767
NSCT_FILL = -32.767
QCFLAG_FILL = -127
VELOCITY_VALID_MAX_MS = 10.0  # dataset valid_min/valid_max envelope


@dataclass(frozen=True)
class HFRDataset:
    """Raw arrays read from an ERDDAP .nc subset (single depth level)."""

    times_s: NDArray[np.float64]          # (nt,) epoch seconds
    latitude: NDArray[np.float64]         # (ny,) degrees_north, increasing
    longitude: NDArray[np.float64]        # (nx,) degrees_east, increasing
    u: NDArray[np.float64]                # (nt, ny, nx) EWCT, m/s, fill kept
    v: NDArray[np.float64]                # (nt, ny, nx) NSCT, m/s, fill kept
    qcflag: NDArray[np.int16]             # (nt, ny, nx)
    dataset_id: str = ""


def load_erddap_netcdf(path: str) -> HFRDataset:
    """Read an ERDDAP griddap .nc subset with vars time/EWCT/NSCT/QCflag.

    Expects the standard (time, depth=1, latitude, longitude) layout and
    squeezes the singleton depth axis. Requires scipy.io.netcdf_file.
    """
    f = netcdf_file(path, "r", mmap=False)
    try:
        names = set(f.variables)
        required = {"time", "latitude", "longitude", "EWCT", "NSCT", "QCflag"}
        missing = required - names
        if missing:
            raise ValueError(f"{path}: missing variables {sorted(missing)}")
        t = np.asarray(f.variables["time"][:], dtype=np.float64)
        lat = np.asarray(f.variables["latitude"][:], dtype=np.float64)
        lon = np.asarray(f.variables["longitude"][:], dtype=np.float64)
        u = np.asarray(f.variables["EWCT"][:], dtype=np.float64)
        v = np.asarray(f.variables["NSCT"][:], dtype=np.float64)
        q = np.asarray(f.variables["QCflag"][:])
    finally:
        f.close()
    # squeeze singleton depth axis -> (nt, ny, nx)
    u = u.reshape(u.shape[0], -1, u.shape[-1]) if u.ndim == 4 and u.shape[1] == 1 else u
    v = v.reshape(v.shape[0], -1, v.shape[-1]) if v.ndim == 4 and v.shape[1] == 1 else v
    q = q.reshape(q.shape[0], -1, q.shape[-1]) if q.ndim == 4 and q.shape[1] == 1 else q
    if u.shape[1] != lat.size or u.shape[2] != lon.size:
        raise ValueError(f"{path}: grid axes inconsistent with variable shape {u.shape}")
    if not (np.all(np.diff(lat) > 0) and np.all(np.diff(lon) > 0)):
        raise ValueError(f"{path}: latitude/longitude must be strictly increasing")
    order = np.argsort(t, kind="stable")
    t = t[order]
    keep = np.concatenate(([True], np.diff(t) > 0))  # drop duplicate timestamps
    if not np.all(keep):
        u, v, q = u[keep], v[keep], q[keep]
        t = t[keep]
    return HFRDataset(t, lat, lon, u, v, q.astype(np.int16))


def equirectangular_grid(
    longitude: NDArray[np.float64],
    latitude: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Project (lon, lat) degrees to local metric x, y in metres.

    Projection centre is the centre of the supplied coordinate ranges.
    Returns (x, y) 1-D arrays aligned with the inputs.
    """
    lon = np.asarray(longitude, dtype=np.float64)
    lat = np.asarray(latitude, dtype=np.float64)
    lon0 = 0.5 * (lon.min() + lon.max())
    lat0 = 0.5 * (lat.min() + lat.max())
    x = EARTH_RADIUS_M * np.cos(np.deg2rad(lat0)) * np.deg2rad(lon - lon0)
    y = EARTH_RADIUS_M * np.deg2rad(lat - lat0)
    return x, y


def hfr_valid_mask(
    qcflag: NDArray[np.int16],
    u: NDArray[np.float64],
    v: NDArray[np.float64],
    *,
    accepted_qc_flags: Sequence[int] = (1,),
) -> NDArray[np.bool_]:
    """Boolean mask of QC-usable cells; True = usable observation."""
    q = np.asarray(qcflag)
    uu = np.asarray(u, dtype=np.float64)
    vv = np.asarray(v, dtype=np.float64)
    qc_ok = np.isin(q, list(accepted_qc_flags))
    finite = (np.isfinite(uu) & np.isfinite(vv)
              & (uu != EWCT_FILL) & (vv != NSCT_FILL)
              & (np.abs(uu) <= VELOCITY_VALID_MAX_MS)
              & (np.abs(vv) <= VELOCITY_VALID_MAX_MS))
    return qc_ok & finite


def build_segments(
    times_s: NDArray[np.float64],
    max_gap_s: float,
    observed: NDArray[np.bool_] | None = None,
) -> list[slice]:
    """Split the time axis at gaps larger than ``max_gap_s`` seconds.

    Returns a list of ``slice`` objects, each covering one contiguous
    block of observed timestamps. Consecutive observations closer than
    ``max_gap_s`` stay in the same segment (linear interpolation in time
    is then the documented approximation).

    ``observed`` (optional, shape (nt,)) marks timestamps that carry at
    least one QC-valid cell. An unobserved timestamp acts as a barrier:
    no segment may interpolate across it, so segments break on both
    sides of every ``observed == False`` index.
    """
    t = np.asarray(times_s, dtype=np.float64)
    if t.ndim != 1 or t.size < 2:
        raise ValueError("times_s must be a 1-D array with >= 2 points")
    if not np.all(np.diff(t) > 0):
        raise ValueError("times_s must be strictly increasing")
    if not np.isfinite(max_gap_s) or max_gap_s <= 0:
        raise ValueError("max_gap_s must be finite and positive")
    if observed is None:
        observed = np.ones(t.size, dtype=bool)
    else:
        observed = np.asarray(observed, dtype=bool)
        if observed.shape != t.shape:
            raise ValueError("observed must have shape (nt,)")
    # a segment may contain only observed times that are consecutive in
    # the original index and separated by <= max_gap_s
    bad = (~observed)
    cuts = set(np.flatnonzero(np.diff(t) > max_gap_s) + 1)
    for i in np.flatnonzero(bad):
        cuts.add(i)      # nothing may end/start inside the bad index
        cuts.add(i + 1)  # break after it as well
    bounds = np.array(sorted(cuts | {0, t.size}))
    segs = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        idx = np.arange(a, b)
        good_idx = idx[observed[idx]]
        # keep only runs of consecutive observed indices
        if good_idx.size == 0:
            continue
        run_start = good_idx[0]
        prev = good_idx[0]
        for k in good_idx[1:]:
            if k != prev + 1:
                if prev - run_start + 1 >= 2:
                    segs.append(slice(int(run_start), int(prev + 1)))
                run_start = k
            prev = k
        if prev - run_start + 1 >= 2:
            segs.append(slice(int(run_start), int(prev + 1)))
    return segs


def to_velocity_fields(
    dataset: HFRDataset,
    *,
    max_gap_s: float,
    accepted_qc_flags: Sequence[int] = (1,),
) -> list[VelocityField]:
    """Convert an :class:`HFRDataset` into QC-masked ``VelocityField``s.

    One ``VelocityField`` per contiguous time segment (see
    :func:`build_segments`). Velocity components keep their m s-1 units;
    positions are local equirectangular metres; times stay in epoch
    seconds. Invalid cells carry a 0.0 placeholder masked by ``valid``.
    """
    x, y = equirectangular_grid(dataset.longitude, dataset.latitude)
    mask = hfr_valid_mask(dataset.qcflag, dataset.u, dataset.v,
                          accepted_qc_flags=accepted_qc_flags)
    u = np.where(mask, dataset.u, 0.0)
    v = np.where(mask, dataset.v, 0.0)
    observed = mask.any(axis=(1, 2))
    fields = []
    for seg in build_segments(dataset.times_s, max_gap_s,
                              observed=observed):
        fields.append(VelocityField(
            x=x, y=y,
            times=dataset.times_s[seg],
            velocity=np.stack([u[seg], v[seg]], axis=-1),
            valid=mask[seg],
        ))
    return fields


def crop_field(
    field: VelocityField,
    iy: slice,
    ix: slice,
) -> VelocityField:
    """Return a sub-domain ``VelocityField`` (cell-index slices on y, x).

    Used to restrict a pilot to a high-coverage sub-region. Grid
    coordinates are re-projected so that x/y remain consistent with the
    equirectangular convention (x depends on lon only, y on lat only).
    """
    xs = field.x[ix]
    ys = field.y[iy]
    return VelocityField(
        x=xs, y=ys, times=field.times,
        velocity=field.velocity[:, iy, ix, :],
        valid=None if field.valid is None else field.valid[:, iy, ix],
    )
