import numpy as np
import units as un

nx_box = [256, 256, 256]  # Number of grid points in each direction
nx_mb = [64, 64, 64]  # Number of grid points in each direction for the mesh block

L_box = 1
rho0 = 1.0  # Reference density
T0 = 1e6 #in K
M = 0.75

k_peak = 2.0

#====================================#
T_floor = T0/100

cs = un.cs_calc(T0, mu=un.mu)  # Sound speed in the medium
v_turb = cs * M

p0 = un.pressure(rho0, T0)  # Reference pressure
p_floor = p0*0.00001

L_drive = L_box/k_peak
t_eddy = L_drive/v_turb

tlim = 8*t_eddy

dt_hst = 0.0001*tlim
dt_hdf = tlim/10
dt_rst = 0.1*tlim

x_max = L_box

corr_time = t_eddy
accel_rms  = 10 * v_turb**2 / (4*L_drive) 

n_cores = np.prod(nx_box)/np.prod(nx_mb) 
enable_cool = 'none'

rescale_time = 6*t_eddy
rescale_Ms = 0.75