"""Independent particle-transport engine for RheoMarine.

This package is deliberately independent of HFR ingestion. The caller supplies
model-ready velocity fields and their QC mask through :class:`VelocityField`.
"""
from .m0 import SimulationResult, VelocityField, simulate_m0

__all__ = ["SimulationResult", "VelocityField", "simulate_m0"]
"""Independent surface transport engine for RheoMarine-SLO."""
from .grid import Grid2D, TransportResult, stability_timestep, step_advection_diffusion
from .particles import ParticleClass, stokes_settling_velocity
__all__ = ["Grid2D","TransportResult","stability_timestep","step_advection_diffusion","ParticleClass","stokes_settling_velocity"]
