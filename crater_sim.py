import numpy as np 
import matplotlib.pyplot as plt
import streamlit as st
import time
from scipy.integrate import solve_ivp


# HYPERPARAMETERS
P = 1e5
T = 190
rho_planet = 2.7 # g/cm3
delta_impactor = 2.7 # g/cm3

# GLOBAL PARAMETERS
rho_u = 2.4 #g/cm3
rho_l = 2.2 #g/cm3
T_melting = 1000 # K
beta = 0.8 # no dim
g = 9.81 # m/s2
y_0 = 2.4e9 # resistance initiale (Pa)
y_ul = 1e3 # resistance upper limit (Pa)


# INPUT PARAMETERS
U = 20000 # m/s
a = 1000 / 100 # m


## V2
# Crater Types
crater_types = {
    "Lunaire": {"g": 1.62, "rho_planet": 3.34, "delta_impactor": 2.7, "a": 500, "temp":200, "u":10, "angle":45},
    "Terrestre": {"g": 9.81, "rho_planet": 2.7, "delta_impactor": 2.6, "a": 250, "temp":190, "u":6, "angle":30},
    "Martien": {"g": 3.72, "rho_planet": 3.93, "delta_impactor": 2.5, "a": 1000, "temp":200, "u":12, "angle":20},
    "Cérès": {"g": 0.28, "rho_planet": 2.16, "delta_impactor": 2.4, "a": 2500, "temp":200, "u":12, "angle":45}
}

# Streamlit UI
st.title("Simulation de Formation de Cratères")

crater_choice = st.selectbox("Choisissez un type de cratère :", list(crater_types.keys()))
params = crater_types[crater_choice]

params["g"] = st.slider("Gravité (m/s²)", 0.1, 20.0, params["g"])
params["rho_planet"] = st.slider("Densité de la planète (g/cm³)", 2.0, 5.0, params["rho_planet"])
params["delta_impactor"] = st.slider("Densité de l'impacteur (g/cm³)", 2.0, 5.0, params["delta_impactor"])
params["a"] = st.slider("Rayon de l'impacteur (m)", 5, 5000, params["a"])
params["temp"] = st.slider("Température de l'impacteur (°K)", 5, 200, params["temp"])
params["u"] = st.slider("Vitesse de l'impacteur (km/s)", 1, 12, params["u"])
params["angle"] = st.slider("Angle d'impact (°)", 0, 45, params["angle"])


def convert_mohr(angle):
    return angle/45


def calculate_degradation(y_ul, T, rho):
    if y_ul >= 0.0 and y_ul <= 2.49e9:
        if (T / (T_melting * (1 - beta))) <= 1 and ((rho - rho_l) / (rho_u - rho_l)) <= 1:
            y_d = y_ul * ((T_melting - T) / (T_melting * (1 - beta) )) * ( (rho - rho_l) / (rho_u - rho_l))
        else: 
            y_d = 0
    else:
        print("y_ul value is out of bounds")
        y_d = 0
        
    print(T / (T_melting * (1 - beta)))
    print((rho - rho_l) / (rho_u - rho_l))
    
    print(f"Degradation in strength: {y_d} dyn/cm2")
    return y_d


def calculate_yield_strength(y_d, y_0, dY_dP):
    Ys = y_d + (y_0 - y_d) * np.exp((dY_dP * P) / (y_0 - y_d))
    return Ys


def calculate_crater_param(g, a, U, rho_planet, delta_impactor):
    dp = 0.96 * a * (rho_planet / delta_impactor)**-0.26 * (g * a / U**2)**-0.22
    Dp = 1.82 * a * (rho_planet / delta_impactor)**-0.26 * (g * a / U**2)**-0.22
    
    return (dp, Dp)

def determine_crater_class(Ys, rho_planet, g, dp):
    if Ys / (rho_planet * g * dp) > 0.15:
        crater_type = "Simple"
    else:
        crater_type = "Complex"
        
    return crater_type


def crater_evolution(t, y, U, R_f, Z_f, alpha, beta):
    R, Z = y
    dR_dt = alpha * U * (1 - R / R_f)
    dZ_dt = beta * U * (1 - Z / Z_f)
    return (dR_dt, dZ_dt)


def solve_crater_growth(U, R_f, Z_f, alpha=0.05, beta=0.1, t_final = 1000):
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, 100)
    y0 = [0, 0]
    sol = solve_ivp(crater_evolution, t_span, y0, t_eval = t_eval, args=(U, R_f, Z_f, alpha, beta))
    return sol.t, sol.y[0], sol.y[1]


t_slider = st.slider("Temps normalisé (Ut/a)", min_value=1, max_value=1000, step=1)

dp, Dp = calculate_crater_param(params["g"], params["a"], params["u"], params["rho_planet"], params["delta_impactor"])
y_d = calculate_degradation(y_ul, params["temp"], params["delta_impactor"])
Ys = calculate_yield_strength(y_d, y_0, convert_mohr(params["angle"]))
crater_type = determine_crater_class(Ys, params["rho_planet"], params["g"], dp)
    
t_values, R_values, Z_values = solve_crater_growth(params["u"], Dp, dp)
    
    
t_index = np.searchsorted(t_values, t_slider)
R_current = R_values[t_index]
Z_current = Z_values[t_index]

   
if st.button("Simuler"):
    
    st.write("### Résultats Calculés")
    st.write(f"**Profondeur de pénétration** : {dp:.2f} m")
    st.write(f"**Diamètre du cratère transitoire** : {Dp:.2f} m")
    st.write(f"**Type de cratère** : {crater_type}")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    r = np.linspace(-R_current, R_current, 300) / params["a"]
    r_crater = R_current / (2 * params["a"])
    h_lip = 0.1 * (R_current / params["a"])
    w_lip = 0.5 * r_crater 
    z = -(Z_current / params["a"]) * (1 - (r / r_crater)**2)
    lip = h_lip * np.exp(-((r - r_crater)**2) / w_lip**2) + h_lip * np.exp(-((r + r_crater)**2) / w_lip**2)
    z_lip = z + lip
    
    z_lip[r < -r_crater] = 0
    z_lip[r > r_crater] = 0
    
    ax.fill_between(r, np.minimum(z, z_lip), -3, color='tan', alpha=0.6, label="Surface impactée")
    ax.fill_between(r, z_lip, 0.1, color='white')
    ax.plot(r, z_lip, color='darkred', linewidth=2, label=f"Cratère {crater_type}")
    ax.set_xlabel("Rayon normalisé (r/a)")
    ax.set_ylabel("Profondeur normalisée (z/a)")
    ax.set_title(f"Profil du cratère après impact")
    ax.legend()
    ax.set_xlim(-1.5 * r_crater, 1.5 * r_crater)
    ax.set_ylim(-3, 3)
    
    ax.text(0.02, 0.9, f"T = {t_slider:.1f}", transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    
    st.pyplot(fig)
    
         
        
animate = st.button("Animer")
if animate:
    placeholder = st.empty()
    
    st.write("### Résultats Calculés")
    st.write(f"**Profondeur de pénétration** : {dp:.2f} m")
    st.write(f"**Diamètre du cratère transitoire** : {Dp:.2f} m")
    st.write(f"**Type de cratère** : {crater_type}")
    
    for frame in range(len(t_values)):        
        R_anim = R_values[frame]
        Z_anim = Z_values[frame]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        r = np.linspace(-R_anim, R_anim, 300) / params["a"]
        r_crater = R_anim / (2 * params["a"])
        h_lip = 0.1 * (R_anim / params["a"])
        w_lip = 0.5 * r_crater 
        z = -(Z_anim / params["a"]) * (1 - (r / r_crater)**2)
        lip = h_lip * np.exp(-((r - r_crater)**2) / w_lip**2) + h_lip * np.exp(-((r + r_crater)**2) / w_lip**2)
        z_lip = z + lip

        z_lip[r < -r_crater] = 0
        z_lip[r > r_crater] = 0
        
        ax.fill_between(r, np.minimum(z, z_lip), -3, color='tan', alpha=0.6, label="Surface impactée")
        ax.fill_between(r, z_lip, 0.1, color='white')
        ax.plot(r, z_lip, color='darkred', linewidth=2, label=f"Cratère {crater_type}")
        ax.set_xlabel("Rayon normalisé (r/a)")
        ax.set_ylabel("Profondeur normalisée (z/a)")
        ax.set_title(f"Profil du cratère après impact")
        ax.legend()
        ax.set_xlim(-1.5 * r_crater, 1.5 * r_crater)
        ax.set_ylim(-3, 3)
        ax.text(0.02, 0.9, f"T = {t_values[frame]:.1f}", transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        
        placeholder.pyplot(fig)
        plt.close(fig)
        
        time.sleep(0.05)

st.sidebar.header("☄️ More on EasyCraterSim")

show_info = st.sidebar.checkbox("ℹ️ About EasyCraterSim")
show_contact = st.sidebar.checkbox("📬 Contact Info")

if show_contact:
    st.sidebar.write("For any questions or contributions, reach out to:")
    st.sidebar.write("📧 Email: maxime.soares-correia@universite-paris-saclay.fr")
    st.sidebar.write("[🌍 GitHub Repo](https://github.com/MaxSC4/EasyCraterSim)")

if show_info:
    st.sidebar.write("""
        EasyCraterSim is a numerical simulation tool for modeling impact crater formation.
        It is based on the work of O'Keefe & Ahrens (1999) and developed as part of the 
        Mathematical Modeling course at Université Paris-Saclay. More on the GitHub!                     
""")
 


