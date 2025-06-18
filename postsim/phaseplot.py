import h5py
import numpy as np
import matplotlib.pyplot as plt
import units as un
from scipy import stats

#### main functions ####
def read_parthenon_data(filename):
    """
    Read density and pressure from a Parthenon .phdf file
    Assumes standard variable ordering: [rho, vx, vy, vz, prs]
    """
    with h5py.File(filename, 'r') as f:
        prim_data = f['prim']
        n_vars = prim_data.shape[-1]
        if n_vars >= 5:
            rho = prim_data[..., 0]
            prs = prim_data[..., 4]
        else:
            print("Warning: fewer than 5 variables, assuming fallback ordering")
            rho = prim_data[..., 0]
            prs = prim_data[..., -1]
        return rho, prs

def fit_polytropic_relation(rho, prs):
    log_rho = np.log10(rho)
    log_prs = np.log10(prs)
    coeffs = np.polyfit(log_rho, log_prs, 1)
    gamma_eff = coeffs[0]
    log_K = coeffs[1]
    r_squared = 1 - np.var(log_prs - (gamma_eff * log_rho + log_K)) / np.var(log_prs)
    K = 10**log_K
    rho_fit = np.logspace(log_rho.min(), log_rho.max(), 100)
    prs_fit = K * rho_fit**gamma_eff
    return gamma_eff, K, rho_fit, prs_fit, r_squared

#######

filename = "/ptmp/mpa/ankitad/athenapk/testrun/parthenon.prim.00025.phdf"
rho, prs = read_parthenon_data(filename)
temp = un.temperature(rho, prs)

rho_physical = rho * un.unit_density
prs_physical = prs * un.unit_q

rho_flat = rho_physical.flatten()
prs_flat = prs_physical.flatten()
temp_flat = temp.flatten()

valid = (rho_flat > 0) & (prs_flat > 0) & (temp_flat > 0) & np.isfinite(rho_flat) & np.isfinite(prs_flat)
rho_clean, prs_clean, temp_clean = rho_flat[valid], prs_flat[valid], temp_flat[valid]

if len(rho_clean) == 0:
    raise RuntimeError("No valid data points to plot.")

gamma_eff, K, rho_fit, prs_fit, r_squared = fit_polytropic_relation(rho_clean, prs_clean)

if gamma_eff < 1.1:
    regime = "Nearly isothermal"
elif gamma_eff > 1.5:
    regime = "Nearly adiabatic"
else:
    regime = "Mixed cooling/heating"

#plotting
plt.figure(figsize=(8, 7))
hb = plt.hexbin(np.log10(rho_clean), np.log10(prs_clean), C=np.log10(temp_clean),
                gridsize=200, reduce_C_function=np.mean, cmap='viridis', alpha=0.8)
plt.plot(np.log10(rho_fit), np.log10(prs_fit), 'r-', linewidth=3, 
         label=f'P ∝ ρ^{gamma_eff:.2f} (R² = {r_squared:.3f})')
plt.colorbar(hb, label=r'$\log_{10}(T\,[K])$')
plt.xlabel(r'$\log_{10}(\rho\,[\mathrm{g/cm^3}])$')
plt.ylabel(r'$\log_{10}(P\,[\mathrm{dyn/cm^2}])$')
plt.title('Pressure–Density Phase Diagram with Temperature Coloring')
plt.legend(loc='upper left', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.text(0.02, 0.98, f'γ_eff = {gamma_eff:.3f}\n{regime}',
         transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.savefig('polytropicfit.png')

log_rho = np.log10(rho_clean)
log_prs = np.log10(prs_clean)
log_prs_fit = np.log10(K) + gamma_eff * log_rho
residuals = log_prs - log_prs_fit

plt.figure(figsize=(8, 5))
plt.scatter(log_rho, residuals, c=np.log10(temp_clean), cmap='viridis', alpha=0.6, s=1)
plt.axhline(y=0, color='r', linestyle='--', alpha=0.8)
plt.colorbar(label=r'$\log_{10}(T\,[K])$')
plt.xlabel(r'$\log_{10}(\rho\,[\mathrm{g/cm^3}])$')
plt.ylabel(r'Residual: $\log_{10}(P) - \log_{10}(P_{\mathrm{fit}})$')
plt.title('Residuals from Polytropic Fit')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('polytropic_residuals.png')

