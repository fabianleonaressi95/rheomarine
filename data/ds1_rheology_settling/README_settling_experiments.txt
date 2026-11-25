1. Title of Dataset: Settling_experiments
Data were collected in Laboratory of Hydrodynamic Micromodels, Institute of Geophysics, Polish Academy of Sciences

2. Folder List: 

Folder Settling_experiments contains 7 sub-folders with data for each experimental set.

AS
AS_XG0.5
AS_XG1
AS_CR0.5
AS_CR1
AS_XGCR0.5
AS_XGCR1
where AS - artificial seawater, XG - xanthan gum, CR - kappa-carrageenan, XGCR - mixture of xanthan gum and kappa-carrageenan
0.5 and 1 are concentrations of polymers in g/L.

3. Additional related data collected that was not included in the current data package: 
Data on dimensions of tesp particles stored in Dimensions_of_particles folder and data on the rheological properties of solutions stored in Rheological_data folder
	
4. Methodological information:

Detailed description of methods used for collection/generation of data: 
Presented in a paper linked to this dataset.

General description: settling of microplastic particles in dispersions of xantahan gum and kappa-carrageenan in artificial seawater was recorded using a camera.
7 types of solutions were used, and 15 different particles were tested.  

5. Data-specific information:
 
Each sub-folder contains:
several .csv files (equal to the number of all runs in the experimental set) called SolutionName_ParticleType_ind_run_RunParticle.csv, 
where 
ParticleType is in the following format:
P_A_ind where P indicates type of particle (S – sphere, D – disk, R - rod, B - blade, I - irregulaer) 
A indicates polymer type (PS, POM, PET, PA), 
ind - indicates set of particles in terms of dimentsions (a, b, c) defined in the related paper and below,
RunParticle indicates the number of run for the particular type of particle. 

Files contain data on the position of particle centroid and angle (orientgation) of non-spherical particles 
in time in four columns: x [pix], z [pix], t[s], angle[degrees]
where x - horizontal cooridnate, z - vertical coordinate, t - time instant. 
angle defined as the angle (in degrees) between the x-axis and the major axis of the ellipse that has the 
same second-moments as the particle projection assessed using Matlab Image Processing Toolbox® 














