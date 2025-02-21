import streamlit as st
from utils.crater_functions import *
from utils.plot_craters import *
from utils.crater_types import crater_types

st.markdown(
    """<h2 style="text-align: center">
            Single Crater Simulation
        </h2>
    """, unsafe_allow_html=True)

# === CRATER CHOICES ===
crater_choice = st.selectbox("Choose a predefined crater type:", list(crater_types.keys()))
params = crater_types[crater_choice]

# === SLIDERS ===
params["g"] = st.slider("🌍 Gravity (m/s²)", 0.1, 20.0, params["g"])
params["rho_planet"] = st.slider("🔗 Planet Density (g/cm³)", 2.0, 5.0, params["rho_planet"])
params["delta_impactor"] = st.slider("☄️ Impactor Density (g/cm³)", 2.0, 8.0, params["delta_impactor"])
params["a"] = st.slider("🌀 Impactor Radius (m)", 5, 10000, params["a"])
params["temp"] = st.slider("🔥 Impactor Temperature (K)", 5, 200, params["temp"])
params["u"] = st.slider("🚀 Impactor Velocity (km/s)", 1, 25, params["u"])
params["angle"] = st.slider("📐 Impact Angle (°)", 0, 45, params["angle"])

t_slider = st.slider("⏳ Normalized Time (Ut/a)", min_value=1, max_value=1000, step=1)

# === COMPUTATION ===
dp, Dp = calculate_crater_param(params["g"], params["a"], params["u"], params["rho_planet"], params["delta_impactor"])
y_d = calculate_degradation(y_ul, params["temp"], params["delta_impactor"])
Ys = calculate_yield_strength(y_d, y_0, convert_mohr(params["angle"]))
crater_type = determine_crater_class(Ys, params["rho_planet"], params["g"], dp)

t_values, R_values, Z_values = solve_crater_growth(params["u"], Dp, dp)
    
t_index = np.searchsorted(t_values, t_slider)
R_current = R_values[t_index]
Z_current = Z_values[t_index]

# === DISPLAY BUTTONS ===
with st.container():
    col1, col2, col3 = st.columns(3, gap="large", vertical_alignment="center")

    with col1:
        simulate_button = st.button("🚀 Simulate")

    with col2:
        animate_button = st.button("☄️ Animate")
        
    with col3:
        generate_button = st.button("🎬 Generate GIF")


# === SIMULATE ONE FRAME ===
if simulate_button:
    simulate(dp, Dp, crater_type, R_current, Z_current, params, t_slider)

# === ANIMATE ===
if animate_button:  
    animate(dp, Dp, crater_type, R_values, Z_values, params, t_values)  

# === DOWNLOAD GIF ANIM ===
if generate_button:
    generate(t_values, R_values, Z_values, params, crater_type)