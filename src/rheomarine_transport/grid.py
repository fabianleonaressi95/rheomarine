"""Conservative finite-volume M0 transport on a uniform Cartesian surface grid."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
FloatArray = NDArray[np.float64]

@dataclass(frozen=True)
class Grid2D:
    """Uniform grid; nx and ny are cell counts."""
    nx: int
    ny: int
    dx: float
    dy: float
    def __post_init__(self):
        if self.nx < 2 or self.ny < 2: raise ValueError("nx and ny must be >= 2")
        if not np.isfinite(self.dx) or not np.isfinite(self.dy) or self.dx <= 0 or self.dy <= 0:
            raise ValueError("dx and dy must be finite and positive")
    @property
    def cell_area(self): return self.dx * self.dy

@dataclass(frozen=True)
class TransportResult:
    concentration: FloatArray
    mass_before: float
    mass_after: float
    source_mass: float
    sink_mass: float

def _field(value, shape, name):
    arr = np.asarray(value, dtype=float)
    if arr.ndim == 0: arr = np.full(shape, float(arr))
    if arr.shape != shape: raise ValueError(f"{name} must be scalar or have shape {shape}")
    if not np.all(np.isfinite(arr)): raise ValueError(f"{name} must be finite")
    return arr

def stability_timestep(grid, u, v, diffusivity, cfl=0.8):
    """Explicit-step bound for first-order upwind advection and diffusion."""
    if not 0 < cfl <= 1: raise ValueError("cfl must be in (0, 1]")
    shape=(grid.ny,grid.nx); uu=_field(u,shape,"u"); vv=_field(v,shape,"v")
    kk=_field(diffusivity,shape,"diffusivity")
    if np.any(kk<0): raise ValueError("diffusivity must be non-negative")
    rate=float(np.max(np.abs(uu))/grid.dx+np.max(np.abs(vv))/grid.dy)
    rate+=float(2*np.max(kk)*(grid.dx**-2+grid.dy**-2))
    return np.inf if rate==0 else cfl/rate

def step_advection_diffusion(concentration,u,v,diffusivity,dt,grid,source=0.0,sink_rate=0.0,*,enforce_stability=True):
    """Advance one step; zero-normal-flux boundaries on all four sides.

    Velocities: m/s; dx,dy: m; diffusivity: m2/s; dt: s.
    Source has concentration/s units; sink_rate has 1/s units.
    """
    shape=(grid.ny,grid.nx); c=_field(concentration,shape,"concentration").copy()
    uu=_field(u,shape,"u"); vv=_field(v,shape,"v"); kk=_field(diffusivity,shape,"diffusivity")
    ss=_field(source,shape,"source"); lam=_field(sink_rate,shape,"sink_rate")
    if np.any(c<0): raise ValueError("concentration must be non-negative")
    if np.any(kk<0) or np.any(lam<0): raise ValueError("diffusivity and sink_rate must be non-negative")
    if not np.isfinite(dt) or dt<=0: raise ValueError("dt must be finite and positive")
    if enforce_stability:
        limit=stability_timestep(grid,uu,vv,kk)
        if dt>limit*(1+1e-12): raise ValueError(f"dt={dt:g} exceeds explicit stability bound {limit:g}")
    fx=np.zeros((grid.ny,grid.nx+1)); uf=.5*(uu[:,:-1]+uu[:,1:]); kf=.5*(kk[:,:-1]+kk[:,1:])
    cup=np.where(uf>=0,c[:,:-1],c[:,1:]); grad=(c[:,1:]-c[:,:-1])/grid.dx
    fx[:,1:-1]=uf*cup-kf*grad
    fy=np.zeros((grid.ny+1,grid.nx)); vf=.5*(vv[:-1,:]+vv[1:,:]); ky=.5*(kk[:-1,:]+kk[1:,:])
    cupy=np.where(vf>=0,c[:-1,:],c[1:,:]); grady=(c[1:,:]-c[:-1,:])/grid.dy
    fy[1:-1,:]=vf*cupy-ky*grady
    div=(fx[:,1:]-fx[:,:-1])/grid.dx+(fy[1:,:]-fy[:-1,:])/grid.dy
    advected=c-dt*div
    if np.min(advected)<-1e-12: raise FloatingPointError("negative concentration; reduce dt")
    advected=np.maximum(advected,0)
    after_source=advected+dt*ss
    if np.min(after_source)<-1e-12: raise ValueError("source would produce negative concentration")
    after_source=np.maximum(after_source,0)
    updated=after_source*np.exp(-lam*dt)
    area=grid.cell_area
    mb=float(c.sum()*area); sm=float((dt*ss).sum()*area)
    sk=float((after_source-updated).sum()*area); ma=float(updated.sum()*area)
    return TransportResult(updated,mb,ma,sm,sk)
