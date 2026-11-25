1. Title of Dataset: MPs_velocity
Data were collected in the Laboratory of Hydrodynamic Micromodels, Institute of Geophysics, Polish Academy of Sciences

2. Folder List: 

Folders settling_runs_IW1, settling_runs_IW2 (where IW1 and IW2 refer to Interrogation Window #1 and Interrogation Window #2) 
contain 9 sub-folders with data for each experimental set.

set1_1
set1_2
set1_3
set2_1
set2_2
set2_3
set3_1
set3_1
set3_3
	
3. Methodological information:

Detailed description of methods used for collection/generation of data: 
Presented in a paper linked to this dataset.

General description: settling of microplastic particles in a two-layered column of liquid with upper and lower layers varying in density and/or rheological properties. 
Solutions composed of artificial seawater and xanthan gum. 6 types of particles were tested.

4. Data-specific information:
 
Each sub-folder contains:
several .csv files (equal to the number of all runs in the experimental set) called set_NoSet_ParticleType_ind_run_RunParticle.csv, 
where 
NoSet is a number of set
ParticleType is in the following format:
P_ind where P indicates the type of particle (S – sphere, D – disk, R - rod) 
ind - indicates a set of particles in terms of dimensions (a, b, c) defined in the related paper and below,
RunParticle indicates the number of runs for the particular type of particle. 

Files contain processed data - instantaneous settling velocity of a particle. The rational function has been fitted to the temporal evolution of particle position data and next the first derivative has been evalusted to calculate instantaneous sinking velocity.
Each file contains three columns: u [m/s], z [m], t[s].
where u - sinking velocity, z - vertical coordinate, t - time instant.







