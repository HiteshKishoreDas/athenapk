import numpy as np

CONST_pc = 3.086e18
CONST_yr = 3.154e7
CONST_amu = 1.66053886e-24
CONST_kB = 1.3806505e-16

unit_length = CONST_pc * 1e3  # 1 kpc
unit_time = CONST_yr * 1e6  # 1 Myr
unit_density = CONST_amu  # 1 mp/cm-3

unit_velocity = unit_length / unit_time

unit_mass = unit_density * unit_length**3

KELVIN = unit_velocity * unit_velocity * CONST_amu / CONST_kB
unit_q = (unit_density * (unit_velocity**3)) / unit_length

Xsol = 1.0
Zsol = 1.0

X = Xsol * 0.7381
Z = Zsol * 0.0134
Y = 1 - X - Z # He_mass_fraction

mu = 1.0 / (2.0 * X + 3.0 * (1.0 - X - Z) / 4.0 + Z / 2.0)
mue = 2.0 / (1.0 + X)
muH = 1.0 / X

mH = 1.0

gamma = 5 / 3

def temperature(rho, prs):
    return (prs / rho) * (KELVIN * mu)

def pressure(rho, T):
    return rho*T / (KELVIN * mu)

def cs_calc(T_hot, mu=0.5):
    kB = 1.38 * 1e-23
    mp = 1.66 * 1e-27

    m_to_cm = 100

    return np.sqrt(gamma * kB / (mu * mp) * T_hot) * m_to_cm / unit_velocity