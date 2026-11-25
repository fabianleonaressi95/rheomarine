1. Title of Dataset: MPs_position
Data were collected in the Laboratory of Hydrodynamic Micromodels, Institute of Geophysics, Polish Academy of Sciences

2. Folder List: 

Folders IW1 and IW2 (where IW1 and IW2 refer to Interrogation Window #1 and Interrogation Window #2) 
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

General description: settling of microplastic particles in two-layered column of liquid with upper and lower layers varying in density and/or rheological properties. Solutions composed of artificial seawater and xanthan gum. 6 types of particles were tested.

4. Data-specific information:
 
Each sub-folder contains:
several .csv files (equal to the number of all runs in the experimental set) called set_NoSet_ParticleType_ind_run_RunParticle.csv, 
where 
NoSet is a number of set
ParticleType is in the following format:
P_ind where P indicates the type of particle (S – sphere, D – disk, R - rod) 
ind - indicates set of particles in terms of dimensions (a, b, c) defined in the related paper and below,
RunParticle indicates the number of run for the particular type of particle. 

Files contain data on the position of particle centroid and angle (orientation) of non-spherical particles 
in time in four columns: x [pix], z [pix], t[s], and angle[degrees]. One pixel corresponds to 31 mum.
where x - the horizontal coordinate, z - the vertical coordinate, t - time instant. 
angle defined as the angle (in degrees) between the x-axis and the major axis of the ellipse that has the 
same second moments as the particle projection assessed using Matlab Image Processing Toolbox® 

dimensions of particles (L –  length, I – breadth, and S – thickness)

Sa: L=I=S = 1.50 ± 0.02 mm
D_a: L = 1.96 ± 0.06 mm; I = 1.96 ± 0.05 mm; S = 0.20 mm
D_b: L = 3.00 ± 0.06 mm; I = 3.00 ± 0.05 mm; S = 20 mm
D_c: L = 3.03 ± 0.03 mm; I = 3.03 ± 0.07 mm; S = 0.30 mm
R_a: L = 2.39 ± 0.14 mm; I = 0.32 ± 0.03 mm; S = 0.32 ± 0.03 mm
R_b: L = 4.05 ± 0.13 mm; I = 0.3 ± 0.03 mm;	S = 0.30 mm




