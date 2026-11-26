"""HFR ingestion adapter for the RheoMarine transport engine.

Converts European HFR Node ERDDAP NetCDF subsets into QC-masked velocity
fields on a local metric grid. Provides both Lagrangian and Eulerian
handoffs; performs no download, and callers supply acquired files.
"""
from .adapter import (
    EARTH_RADIUS_M,
    HFRDataset,
    build_segments,
    crop_field,
    equirectangular_grid,
    hfr_valid_mask,
    load_erddap_netcdf,
    to_velocity_fields,
)
from .eulerian import EulerianHFRForcing, to_eulerian_forcing
from .trajectory import simulate_qc_aware

__all__ = [
    "EARTH_RADIUS_M",
    "HFRDataset",
    "build_segments",
    "crop_field",
    "equirectangular_grid",
    "hfr_valid_mask",
    "load_erddap_netcdf",
    "simulate_qc_aware",
    "to_velocity_fields",
    "EulerianHFRForcing",
    "to_eulerian_forcing",
]
