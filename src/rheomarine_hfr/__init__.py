"""HFR ingestion adapter for the RheoMarine transport engine.

Converts European HFR Node ERDDAP NetCDF subsets into QC-masked
``VelocityField`` objects on a local metric grid. Performs no download;
the caller supplies already-acquired files (see docs/hfr/).
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

__all__ = [
    "EARTH_RADIUS_M",
    "HFRDataset",
    "build_segments",
    "crop_field",
    "equirectangular_grid",
    "hfr_valid_mask",
    "load_erddap_netcdf",
    "to_velocity_fields",
]
