"""Independent particle-transport engine for RheoMarine.

This package is deliberately independent of HFR ingestion. The caller supplies
model-ready velocity fields and their QC mask through :class:`VelocityField`.
"""
from .m0 import SimulationResult, VelocityField, simulate_m0

__all__ = ["SimulationResult", "VelocityField", "simulate_m0"]
