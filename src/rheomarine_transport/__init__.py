"""RheoMarine surface-transport engines and particle-property primitives.

The package exposes both the conservative Eulerian finite-volume solver and
the Lagrangian particle tracker. They are alternative numerical formulations;
they must not be combined as independent physical effects in one run.
"""
from .m0 import SimulationResult, VelocityField, simulate_m0
from .grid import Grid2D, TransportResult, stability_timestep, step_advection_diffusion
from .particles import ParticleClass, stokes_settling_velocity

__all__ = [
    "SimulationResult",
    "VelocityField",
    "simulate_m0",
    "Grid2D",
    "TransportResult",
    "stability_timestep",
    "step_advection_diffusion",
    "ParticleClass",
    "stokes_settling_velocity",
]
