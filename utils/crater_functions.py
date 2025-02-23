import numpy as np 
import matplotlib.pyplot as plt
import tempfile
from scipy.integrate import solve_ivp
from PIL import Image


# === PHYSICAL PARAMETERS ===
P = 1e5
T = 190
rho_u = 2.4 #g/cm3
rho_l = 2.2 #g/cm3
T_melting = 1000 # K
beta = 0.8 # no dim
y_0 = 2.4e9 # initial strength (Pa)
y_ul = 1e3 # upper limit strength (Pa)


# === UTILS ===
def convert_mohr(angle):
    """Convert impact angle for Mohr-Coulomb model."""
    return angle/45


def calculate_degradation(y_ul, T, rho):
    """Calculate the strength degradation."""
    if y_ul >= 0.0 and y_ul <= 2.49e9:
        if (T / (T_melting * (1 - beta))) <= 1 and ((rho - rho_l) / (rho_u - rho_l)) <= 1:
            y_d = y_ul * ((T_melting - T) / (T_melting * (1 - beta) )) * ( (rho - rho_l) / (rho_u - rho_l))
        else: 
            y_d = 0
    else:
        print("y_ul value is out of bounds")
        y_d = 0
    return y_d


def calculate_yield_strength(y_d, y_0, dY_dP):
    """Calculate the yield strength of the material."""
    Ys = y_d + (y_0 - y_d) * np.exp((dY_dP * P) / (y_0 - y_d))
    return Ys


def calculate_crater_param(g, a, U, rho_planet, delta_impactor):
    """Compute transient crater depth and diameter."""
    dp = 0.96 * a * (rho_planet / delta_impactor)**-0.26 * (g * a / U**2)**-0.22
    Dp = 1.82 * a * (rho_planet / delta_impactor)**-0.26 * (g * a / U**2)**-0.22
    
    return (dp, Dp)

def determine_crater_class(Ys, rho_planet, g, dp):
    """Determine crater class"""
    if Ys / (rho_planet * g * dp) > 0.15:
        crater_type = "Simple"
    else:
        crater_type = "Complex" # WORK IN PROGRESS
        
    return crater_type


def crater_evolution(t, y, U, R_f, Z_f, alpha, beta):
    """ODE system to model crater growth over time."""
    R, Z = y
    dR_dt = alpha * U * (1 - R / R_f)
    dZ_dt = beta * U * (1 - Z / Z_f)
    return (dR_dt, dZ_dt)


def solve_crater_growth(U, R_f, Z_f, alpha=0.05, beta=0.1, t_final = 1000):
    """Solve the ODE system for crater evolution."""
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, 100)
    y0 = [0, 0]
    sol = solve_ivp(crater_evolution, t_span, y0, t_eval = t_eval, args=(U, R_f, Z_f, alpha, beta))
    return sol.t, sol.y[0], sol.y[1]

def generate_crater_gif(t_values, R_values, Z_values, a, crater_type):
    """Generate an animated GIF of crater evolution"""  
    frames = []      
    fig, ax = plt.subplots(figsize=(8, 5))

    for frame in range(len(R_values)):
        R_anim = R_values[frame]
        Z_anim = Z_values[frame]
  
        r = np.linspace(-R_anim, R_anim, 300) / a
        r_crater = R_anim / (2 * a)
        h_lip = 0.1 * (R_anim / a)
        w_lip = 0.5 * r_crater 
        z = -(Z_anim / a) * (1 - (r / r_crater)**2)
        lip = h_lip * np.exp(-((r - r_crater)**2) / w_lip**2) + h_lip * np.exp(-((r + r_crater)**2) / w_lip**2)
        z_lip = z + lip

        z_lip[r < -r_crater] = 0
        z_lip[r > r_crater] = 0

        ax.clear()

        ax.fill_between(r, np.minimum(z, z_lip), -3, color='tan', alpha=0.6, label="Impacted Surface")
        ax.fill_between(r, z_lip, 0.1, color='white')
        ax.plot(r, z_lip, color='darkred', linewidth=2, label=f"{crater_type} Crater")
        ax.set_xlabel("Normalized radius (r/a)")
        ax.set_ylabel("Normalized depth (z/a)")
        ax.set_title(f"Crater Evolution")
        ax.legend()
        ax.set_xlim(-1.5 * r_crater, 1.5 * r_crater)
        ax.set_ylim(-3, 3)
        ax.text(0.02, 0.9, f"Ut/a = {t_values[frame]:.1f}", transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

        fig.canvas.draw()
        image = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(Image.fromarray(image))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
    temp_path = temp_file.name
    frames[0].save(temp_path, save_all=True, append_images=frames[1:], duration=50, loop=0)
    
    return temp_path

def estimate_impactor(Dp_final, g, rho_planet, delta_impactor_guess=2.7, velocity_guess=20):
    """Estimate impactor parameters based on crater params"""
    a = (Dp_final / (1.82 * (rho_planet / delta_impactor_guess) ** -0.26 * (g * Dp_final / velocity_guess ** 2) ** -0.22))

    return a