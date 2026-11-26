# Morandotti microswimmer models: compatibility assessment for RheoMarine

**Status:** literature assessment completed; no microswimmer equations are integrated into M0.
**Decision:** outside the present passive-microplastic M0 scope; retain as a possible, separately validated active-biological-particle module.

## Primary sources checked

1. M. Morandotti, “Self-propelled micro-swimmers in a Brinkman fluid,” *Journal of Biological Dynamics* 6, Suppl. 1 (2012), 88–103. DOI: [10.1080/17513758.2011.611260](https://doi.org/10.1080/17513758.2011.611260). The article proves existence, uniqueness and regularity for a self-propelled microswimmer in a particulate viscous medium represented by a Brinkman fluid. The swimmer's shape change is the control; the force/torque-free self-propulsion constraint leads to six ODEs for position and orientation.
2. G. Dal Maso, A. DeSimone, M. Morandotti, “An Existence and Uniqueness Result for the Motion of Self-Propelled Microswimmers,” *SIAM Journal on Mathematical Analysis* 43(3) (2011), 1345–1368. DOI: [10.1137/10080083X](https://doi.org/10.1137/10080083X). This is the Stokes-fluid predecessor: low-Reynolds-number flow, negligible inertia, no external force or torque, and shape-change-driven motion.
3. M. Morandotti, PhD thesis (2011), “Self-propulsion in viscous fluids through shape deformation,” [SISSA repository record](https://hdl.handle.net/20.500.11767/4264).

The publisher and SISSA records describe a mathematical theory of *active, shape-changing swimmers*. They do not describe passive plastic-particle drift, marine litter transport, aggregation kinetics, or a coastal circulation model.

## Compatibility with the present model hierarchy

| Feature | RheoMarine passive M0 | Morandotti microswimmer theory |
|---|---|---|
| Body | Passive tracer / microplastic particle | Deformable self-propelled swimmer |
| Kinematics | Ambient velocity plus optional Brownian diffusion | Position and orientation driven by shape deformation |
| Governing fluid model | Prescribed surface-current field from HFR | Stokes or Brinkman boundary-value problem |
| Force balance | Not solved at particle scale | Zero net viscous force and torque |
| State | Horizontal position (in current implementation) | Spatial position and orientation; six ODEs in 3D |
| Required inputs | HFR u/v, QC, grid/time support, diffusivity | Geometry, admissible shape controls, fluid parameters, resistance/mobility maps and initial pose |

**No direct substitution is justified.** A Brinkman fluid models a viscous medium with a distributed porous/particulate drag term. Its appearance in Morandotti's theorem does not establish that the North Adriatic water column is a Brinkman medium, nor does it provide a calibrated permeability or drag parameter for the Gulf of Trieste. HFR measures near-surface Eulerian currents at kilometre-scale grid spacing; it does not resolve microscale swimmer hydrodynamics, shape cycles, orientation, or local rheology.

## Possible future module — active biological swimmers

A separate module could be considered only for a clearly identified biological population (for example, a motile microorganism), not for passive microplastics. At a reduced kinematic level one might write

\[
\dot X(t)=u_{\mathrm{HFR}}(X(t),t)+V_{\mathrm{swim}}(t),
\]

with an orientation state and a constitutive/control law for \(V_{\mathrm{swim}}\). This is **not** Morandotti's full model: it is only an environmental-advection-plus-prescribed-swimming approximation. A faithful Morandotti-type coupling would additionally require the swimmer's geometry and shape-actuation law, force/torque-free hydrodynamic resistance problem, and a justified Stokes/Brinkman fluid description.

Minimum data and modelling requirements before a pilot:
- organism identity, life stage, body geometry and size distribution;
- measured swimming-speed distribution, orientation statistics and persistence/tumbling or reorientation law;
- temperature, salinity and relevant local fluid properties;
- if Brinkman is invoked, independent evidence and calibration for its effective drag/permeability parameter;
- vertical habitat/depth distribution and a hydrodynamic field at compatible depth and temporal resolution;
- independent trajectory observations for validation.

Without these data, the active module is not identifiable and should not be parameterised from the HFR current record alone.

## Relevance to microplastics and aggregation

Microplastic particles are not self-propelled swimmers. Biofouling, attachment to organisms, flocculation, and aggregation may alter effective density, size, drag, and settling, but those processes are not equivalent to internally actuated locomotion. They belong in a separately evidenced passive-particle M1/aggregation model, with measured rates and particle properties. Morandotti's swimmer equations must not be used as a proxy for these processes.

## Decision

- **M0:** retain passive surface transport; no Morandotti terms.
- **M1:** pursue particle properties, aggregation/biofouling and vertical settling only with compatible experimental data; Morandotti is not the governing model.
- **Future optional module:** active biological swimmers only, after the above data and a scale-consistent hydrodynamic coupling are available.
- **Current status:** literature compatibility assessed; no implementation, parameter fitting, or validation claimed.
