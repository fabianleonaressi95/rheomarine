# Morandotti microswimmer models: compatibility assessment for RheoMarine

**Assessment date:** 25 November 2026  
**Decision:** mathematically relevant to an optional active-swimmer research branch; not a governing model for passive microplastic transport and not part of the current HFR/M0 pilot.

## 1. Primary sources checked

1. M. Morandotti, “Self-propelled micro-swimmers in a Brinkman fluid,” *Journal of Biological Dynamics* 6, Suppl. 1 (2012), 88–103. DOI: [10.1080/17513758.2011.611260](https://doi.org/10.1080/17513758.2011.611260). The publisher and PubMed abstracts describe an existence, uniqueness and regularity result for a self-propelled swimmer in a particulate viscous medium governed by Brinkman equations. Shape control leads to six ODEs for position and orientation; the swimmer is force- and torque-free. [PubMed](https://pubmed.ncbi.nlm.nih.gov/22873677/) · [publisher full-text page](https://www.tandfonline.com/doi/full/10.1080/17513758.2011.611260).
2. G. Dal Maso, A. DeSimone, M. Morandotti, “An Existence and Uniqueness Result for the Motion of Self-Propelled Microswimmers,” *SIAM Journal on Mathematical Analysis* 43 (2011), 1345–1368. DOI: [10.1137/10080083X](https://doi.org/10.1137/10080083X). The model assumes very low Reynolds number, Stokes flow, negligible inertia, and no external force or torque. Shape change determines the motion through a six-dimensional position/orientation system. [SISSA record](https://www.math.sissa.it/publication/existence-uniqueness-result-motion-self-propelled-microswimmers/index.html) · [SIAM record](https://epubs.siam.org/doi/10.1137/10080083X).
3. M. Morandotti, *Self-propulsion in viscous fluids through shape deformation*, PhD thesis, SISSA, 2011. The thesis treats Stokes and Brinkman settings, no-slip coupling at the swimmer surface, force/torque-free self-propulsion and shape control. [SISSA repository](https://iris.sissa.it/handle/20.500.11767/4264) · [thesis PDF](https://cvgmt.sns.it/media/doc/paper/1707/PhD_Thesis_Morandotti_2011.pdf).

## 2. What is transferable — and what is not

The transferable mathematical structure is a coupled active-body kinematics:

- state: swimmer position and orientation (six degrees of freedom in 3D);
- control: time-dependent body-shape deformation;
- fluid problem: Stokes or Brinkman system with no-slip coupling;
- closure: zero net external force and torque;
- output: translation and rotation induced by the prescribed shape cycle.

This is not the same model as the current RheoMarine M0 particle tracker. M0 describes passive particles advected by an externally supplied surface current and dispersed by a prescribed horizontal diffusivity. A passive plastic fragment has no internally controlled shape cycle that generates self-propulsion. Morandotti's force/torque-free swimmer equations must therefore not be inserted into M0 or used to infer microplastic transport.

The Brinkman medium in Morandotti is a particulate/porous viscous medium represented by a drag term in the fluid equations. It is not automatically equivalent to seawater containing suspended microplastics, nor to a coastal HFR grid. A Brinkman parameter (permeability or equivalent drag scale) requires a physically justified medium model and independent parameter data.

## 3. Potential RheoMarine application

A separate optional active-particle module could be relevant for motile organisms (for example, selected planktonic or microbial classes) if the project explicitly expands its target from passive plastic debris to biological swimmers. A reduced environmental-coupling model might begin with

\[
\dot{\mathbf X}=\mathbf u_{\rm env}(\mathbf X,t)
+v_s\mathbf p,
\]

where \(\mathbf u_{\rm env}\) is the resolved ambient velocity, \(v_s\) is a measured or literature-supported swimming speed, and \(\mathbf p\) is an orientation vector. An orientation equation would then need a justified biological/physical law (e.g. measured reorientation, taxis, rotational diffusion or a Jeffery-type approximation where its assumptions apply). This reduced equation is a proposed modelling architecture, not a formula derived directly from Morandotti's theorem.

A genuine Morandotti-type hydrodynamic model would additionally require body geometry and its admissible shape family, deformation/control histories, fluid viscosity and (for Brinkman) a justified permeability/drag parameter, no-slip boundary conditions, and the force/torque resistance operators. The present HFR product supplies neither these microscale boundary data nor the three-dimensional ambient flow around each swimmer.

## 4. Data and evidence required before implementation

- Specify the biological target species or organism class; do not use “microswimmer” as an undifferentiated proxy for microplastics.
- Obtain measured swimming-speed distributions, body size/shape, orientation statistics and reorientation times under relevant temperature, salinity and light/food conditions.
- Establish whether the organism is motile at the modelled scale and whether active swimming is material relative to HFR current speed and unresolved turbulence.
- Obtain independent biological observations for evaluation; HFR currents alone cannot validate organism trajectories.
- Use 3D hydrodynamic forcing or explicitly label a 2D surface approximation. HFR surface currents do not resolve vertical shear or the swimmer's local 3D flow.
- If using Brinkman rather than Stokes, identify the particulate/porous medium and independently constrain its permeability/drag coefficient.

## 5. Decision for the current project

| Component | Decision |
|---|---|
| M0 passive microplastic surface transport | Keep as current baseline; no Morandotti self-propulsion term. |
| M1 particle classes, density, shape and settling | Continue independently, using measured/source-traceable parameters. |
| M2 rheological correction | Retain the existing evidence gate; Brinkman is not a shortcut to a marine rheology model. |
| Optional active biological swimmers | Plausible future module only after target organism, data and validation plan are specified. |
| Direct use of six-ODE Morandotti system in HFR M0 | Reject: different physical problem and missing microscale inputs. |

**Conclusion:** Morandotti is relevant as a rigorous mathematical foundation for a possible active-swimmer module, not as a direct model for passive microplastics. The immediate project should complete HFR-to-M0 coupling and the evidence-based M1 particle-property work first. An active biological module should be a separately scoped extension with its own state variables, forcing and validation dataset.
