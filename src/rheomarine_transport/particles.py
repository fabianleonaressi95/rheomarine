"""Evidence-conscious particle properties for M1."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class ParticleClass:
    """Measured/sourced class properties; settling velocity positive downward."""
    class_id: str
    diameter_m: float
    particle_density_kg_m3: float
    settling_velocity_ms: float | None = None
    shape_factor: float | None = None
    def __post_init__(self):
        if not self.class_id: raise ValueError("class_id cannot be empty")
        if not math.isfinite(self.diameter_m) or self.diameter_m<=0: raise ValueError("diameter must be positive")
        if not math.isfinite(self.particle_density_kg_m3) or self.particle_density_kg_m3<=0: raise ValueError("density must be positive")
        if self.settling_velocity_ms is not None and not math.isfinite(self.settling_velocity_ms): raise ValueError("settling velocity must be finite")
        if self.shape_factor is not None and (not math.isfinite(self.shape_factor) or self.shape_factor<=0): raise ValueError("shape factor must be positive")

def stokes_settling_velocity(diameter_m,particle_density_kg_m3,fluid_density_kg_m3=1025.0,dynamic_viscosity_pa_s=1.05e-3,gravity_ms2=9.80665):
    """Signed spherical Stokes reference (m/s), positive downward.

    Only appropriate for low-Reynolds-number spherical settling. Not a
    universal law for irregular microplastics or aggregates.
    """
    vals=(diameter_m,particle_density_kg_m3,fluid_density_kg_m3,dynamic_viscosity_pa_s,gravity_ms2)
    if not all(math.isfinite(x) for x in vals): raise ValueError("inputs must be finite")
    if diameter_m<=0 or min(particle_density_kg_m3,fluid_density_kg_m3,dynamic_viscosity_pa_s,gravity_ms2)<=0:
        raise ValueError("diameter, densities, viscosity and gravity must be positive")
    return (particle_density_kg_m3-fluid_density_kg_m3)*gravity_ms2*diameter_m**2/(18*dynamic_viscosity_pa_s)
