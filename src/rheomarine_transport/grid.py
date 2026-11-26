"""Conservative finite-volume M0 transport on a uniform Cartesian surface grid.

Boundary and masking semantics
------------------------------
``step_advection_diffusion`` supports three explicit, documented closures:

* ``wet`` — a static (ny, nx) boolean water mask. Cells with ``wet == False``
  are land: they must carry zero concentration, all face fluxes touching them
  are exactly zero (no-flux coastline condition), and source/sink terms are
  not applied there.
* ``active`` — an optional per-step (ny, nx) boolean mask, e.g. the QC-valid
  forcing mask for one observation. A cell that is wet but not active is
  isolated for that step: every face flux touching it is zero, so its
  tracer mass is retained unchanged and resumes advection when the mask
  lifts. This is the conservative "QC hole = temporary barrier" policy; it
  never interpolates or zero-fills missing forcing.
* ``open_edges`` — a subset of {"west", "east", "south", "north"} whose
  outer faces exchange mass by advection only. The open-face flux uses the
  boundary cell's velocity and concentration (zero-gradient, first-order
  upwind in the outward sense); the diffusive flux is zero. With no open
  edges the domain is closed and mass is conserved exactly.

Velocities, diffusivity, source and sink may be non-finite ONLY on cells
that are inactive for the step (``wet & active == False``); on active cells
they must be finite. Non-finite forcing on an active cell raises instead of
being silently replaced.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
FloatArray = NDArray[np.float64]

OPEN_EDGES = ("west", "east", "south", "north")

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
    boundary_loss_mass: float = 0.0

def _field(value, shape, name):
    arr = np.asarray(value, dtype=float)
    if arr.ndim == 0: arr = np.full(shape, float(arr))
    if arr.shape != shape: raise ValueError(f"{name} must be scalar or have shape {shape}")
    if not np.all(np.isfinite(arr)): raise ValueError(f"{name} must be finite")
    return arr

def _field_masked(value, shape, name, active):
    """Like _field, but non-finite values are allowed on inactive cells."""
    arr = np.asarray(value, dtype=float)
    if arr.ndim == 0: arr = np.full(shape, float(arr))
    if arr.shape != shape: raise ValueError(f"{name} must be scalar or have shape {shape}")
    if np.any(~np.isfinite(arr) & active):
        raise ValueError(f"{name} must be finite on active cells")
    return arr

def _bool_mask(value, shape, name):
    arr = np.asarray(value)
    if arr.shape != shape: raise ValueError(f"{name} must have shape {shape}")
    return arr.astype(bool)

def _effective_mask(wet, active, shape):
    if wet is None:
        w = np.ones(shape, dtype=bool)
    else:
        w = _bool_mask(wet, shape, "wet")
    if active is None:
        a = np.ones(shape, dtype=bool)
    else:
        a = _bool_mask(active, shape, "active")
    return w & a

def _check_open_edges(open_edges):
    edges = tuple(open_edges) if open_edges is not None else ()
    bad = set(edges) - set(OPEN_EDGES)
    if bad:
        raise ValueError(f"unknown open_edges {sorted(bad)}; allowed: {list(OPEN_EDGES)}")
    return edges

def stability_timestep(grid, u, v, diffusivity, cfl=0.8, *, active=None):
    """Explicit-step bound for first-order upwind advection and diffusion.

    With ``active`` given, only active cells constrain the bound; inactive
    cells may carry non-finite forcing (they contribute no flux).
    """
    if not 0 < cfl <= 1: raise ValueError("cfl must be in (0, 1]")
    shape=(grid.ny,grid.nx)
    if active is None:
        uu=_field(u,shape,"u"); vv=_field(v,shape,"v")
        kk=_field(diffusivity,shape,"diffusivity")
    else:
        act=_bool_mask(active,shape,"active")
        uu=_field_masked(u,shape,"u",act); vv=_field_masked(v,shape,"v",act)
        kk=_field_masked(diffusivity,shape,"diffusivity",act)
        uu=np.where(act,uu,0.0); vv=np.where(act,vv,0.0); kk=np.where(act,kk,0.0)
    if np.any(kk<0): raise ValueError("diffusivity must be non-negative")
    rate=float(np.max(np.abs(uu))/grid.dx+np.max(np.abs(vv))/grid.dy)
    rate+=float(2*np.max(kk)*(grid.dx**-2+grid.dy**-2))
    return np.inf if rate==0 else cfl/rate

def step_advection_diffusion(concentration,u,v,diffusivity,dt,grid,source=0.0,sink_rate=0.0,*,enforce_stability=True,wet=None,active=None,open_edges=()):
    """Advance one step; see module docstring for mask and boundary semantics.

    Velocities: m/s; dx,dy: m; diffusivity: m2/s; dt: s.
    Source has concentration/s units; sink_rate has 1/s units.
    ``open_edges`` subsets of {"west","east","south","north"} replace the
    zero-normal-flux condition on those sides by zero-gradient advective
    exchange with zero diffusive flux; mass is then not closed and the
    net loss is reported as ``boundary_loss_mass``.
    """
    shape=(grid.ny,grid.nx); c=_field(concentration,shape,"concentration").copy()
    edges=_check_open_edges(open_edges)
    wet_arr = None if wet is None else _bool_mask(wet, shape, "wet")
    eff = _effective_mask(wet_arr, active, shape)
    if wet_arr is not None and np.any(c[~wet_arr] != 0):
        raise ValueError("concentration must be zero on land (wet == False) cells")
    uu=_field_masked(u,shape,"u",eff); vv=_field_masked(v,shape,"v",eff)
    kk=_field_masked(diffusivity,shape,"diffusivity",eff)
    ss=_field_masked(source,shape,"source",eff); lam=_field_masked(sink_rate,shape,"sink_rate",eff)
    if np.any(c<0): raise ValueError("concentration must be non-negative")
    finite_kk = kk[np.isfinite(kk)]; finite_lam = lam[np.isfinite(lam)]
    if np.any(finite_kk<0) or np.any(finite_lam<0): raise ValueError("diffusivity and sink_rate must be non-negative")
    if not np.isfinite(dt) or dt<=0: raise ValueError("dt must be finite and positive")
    if enforce_stability:
        limit=stability_timestep(grid,uu,vv,kk,active=eff)
        if dt>limit*(1+1e-12): raise ValueError(f"dt={dt:g} exceeds explicit stability bound {limit:g}")
    # safe copies: inactive cells contribute exactly zero to every face
    u_s=np.where(eff,uu,0.0); v_s=np.where(eff,vv,0.0)
    k_s=np.where(eff,kk,0.0); s_s=np.where(eff,ss,0.0); l_s=np.where(eff,lam,0.0)

    fx=np.zeros((grid.ny,grid.nx+1)); uf=.5*(u_s[:,:-1]+u_s[:,1:]); kf=.5*(k_s[:,:-1]+k_s[:,1:])
    cup=np.where(uf>=0,c[:,:-1],c[:,1:]); grad=(c[:,1:]-c[:,:-1])/grid.dx
    both_x=eff[:,:-1]&eff[:,1:]
    fx[:,1:-1]=np.where(both_x,uf*cup-kf*grad,0.0)
    if "west" in edges: fx[:,0]=np.where(eff[:,0],u_s[:,0]*c[:,0],0.0)
    if "east" in edges: fx[:,-1]=np.where(eff[:,-1],u_s[:,-1]*c[:,-1],0.0)

    fy=np.zeros((grid.ny+1,grid.nx)); vf=.5*(v_s[:-1,:]+v_s[1:,:]); ky=.5*(k_s[:-1,:]+k_s[1:,:])
    cupy=np.where(vf>=0,c[:-1,:],c[1:,:]); grady=(c[1:,:]-c[:-1,:])/grid.dy
    both_y=eff[:-1,:]&eff[1:,:]
    fy[1:-1,:]=np.where(both_y,vf*cupy-ky*grady,0.0)
    if "south" in edges: fy[0,:]=np.where(eff[0,:],v_s[0,:]*c[0,:],0.0)
    if "north" in edges: fy[-1,:]=np.where(eff[-1,:],v_s[-1,:]*c[-1,:],0.0)

    div=(fx[:,1:]-fx[:,:-1])/grid.dx+(fy[1:,:]-fy[:-1,:])/grid.dy
    advected=c-dt*div
    if np.min(advected)<-1e-12: raise FloatingPointError("negative concentration; reduce dt")
    advected=np.maximum(advected,0)
    after_source=advected+dt*s_s
    if np.min(after_source)<-1e-12: raise ValueError("source would produce negative concentration")
    after_source=np.maximum(after_source,0)
    updated=after_source*np.exp(-l_s*dt)
    area=grid.cell_area
    mb=float(c.sum()*area); sm=float((dt*s_s).sum()*area)
    sk=float((after_source-updated).sum()*area); ma=float(updated.sum()*area)
    # net mass carried out through open faces over this step (positive = loss)
    bl=float(dt*(np.sum(fx[:,-1])*grid.dy-np.sum(fx[:,0])*grid.dy
                     +np.sum(fy[-1,:])*grid.dx-np.sum(fy[0,:])*grid.dx))
    return TransportResult(updated,mb,ma,sm,sk,boundary_loss_mass=bl)
