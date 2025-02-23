import streamlit as st
import pandas as pd
from utils.ui.utils_ui import *
from utils.reverse_utils import *

st.set_page_config(
    page_title="EasyCraterSim - Reverse", 
    page_icon="☄️",
    menu_items={
        'About': "# EasyCraterSim\nEasyCraterSim is a numerical simulation tool for modeling impact crater formation. It is based on the work of O'Keefe & Ahrens (1999) and developed as part of the Mathematical Modeling course at Université Paris-Saclay. More on the GitHub!\nby M. Soares Correia"
    }
    )

show_sidebar()
show_title()

st.markdown(
    """<h2 style="text-align: center"> 
            Reverse Simulation 
        </h2>
    """, unsafe_allow_html=True)

if "scenarios" not in st.session_state:
    st.session_state.scenarios = []
if "sorted" not in st.session_state:
    st.session_state.sorted = False
if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = True
if "random_params" not in st.session_state:
    st.session_state.random_params = {}
if "Dp_final" not in st.session_state:
    st.session_state.Dp_final = 10 * 1000 
if "depth_final" not in st.session_state:
    st.session_state.depth_final = 5000 
if "rho_surface" not in st.session_state:
    st.session_state.rho_surface = 2.7 
if "rho_planet" not in st.session_state:
    st.session_state.rho_planet = 2.7 

col1, col2, col3 = st.columns(3, gap="large", vertical_alignment="center")

with col1:
    sort_by_match = st.button("⬆️ Sort by Best Similarity")
    switch_manual = st.button("🤏 Switch to Manual Mode")

with col3:
    random_scenario = st.button("🎲 Generate Random Scenario")
    reset_simulation = st.button("🔄 Reset Simulation")

st.divider()

if reset_simulation:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if switch_manual:
    st.session_state.manual_mode = True

if random_scenario:
    st.session_state.Dp_final, st.session_state.depth_final, st.session_state.rho_planet, st.session_state.rho_surface, scenarios = generate_random_scenario()
    st.session_state.scenarios = scenarios
    st.session_state.manual_mode = False
    st.session_state.sorted = False

if st.session_state.manual_mode:
    st.session_state.Dp_final = st.slider("🌍 Final Crater Diameter (km)", 1, 200, 10) * 1000 
    st.session_state.depth_final = st.slider("📉 Final Crater Depth (m)", 50, 50000, 5000)
    rho_planet = st.slider("🔗 Planet Density (g/cm³)", 2.0, 5.0, 2.7)
    rho_surface = st.slider("🔗 Surface Layer Density (g/cm³)", 1.5, 3.5, 2.4)

    if not st.session_state.scenarios:
        st.session_state.scenarios = generate_impact_scenarios(st.session_state.Dp_final, st.session_state.depth_final, rho_surface, rho_planet)

scenarios = st.session_state.scenarios
Dp_final = st.session_state.Dp_final
depth_final = st.session_state.depth_final
rho_planet = st.session_state.rho_planet
rho_surface = st.session_state.rho_surface

if len(scenarios) == 0:
    st.warning("⚠️ No valid impactor found that matches the given crater dimensions.")
else:
    valid_scenarios = []

    table_data = []
    for a, U, density, energy in scenarios: 
        similarities = similarity_score(Dp_final, depth_final, a, energy)

        filtered_similarities = {name: score for name, score in similarities.items() if score > 10}
        
        if filtered_similarities:
            similarity_str = ", ".join([f"{name} {score:.1f}%" for name, score in similarities.items() if score > 10])
            table_data.append([f"{a:.2f} m", f"{U:.1f} km/s", f"{density:.2f} g/cm³", f"{energy:.2e} J", similarity_str])

            valid_scenarios.append((a, U, density, energy))



    df_results = pd.DataFrame(table_data, columns=["Impactor Radius", "Velocity", "Density", "Impact Energy", "Similarities"])

    if sort_by_match:
        df_results = df_results.sort_values(by="Similarities", ascending=False)
        st.session_state.sorted = True

    st.markdown("""
    <style>
        table {
            width: 100%;
        }
        th {
            text-align: center !important;
        }
        td {
            text-align: center !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.manual_mode == False:
        st.write("### 🎲 Randomly Generated Parameters")
        st.write(f"**Diameter (km)** : {Dp_final/1000:.2f} km")
        st.write(f"**Depth (m)** : {depth_final:.2f} m")
        st.write(f"**Planet density (g/cm³)** : {rho_planet/1000:.2f} g/cm³")
        st.write(f"**Surface density (g/cm³)** : {rho_surface/1000:.2f} g/cm³")

    st.write(f"### 🔍 {len(valid_scenarios)} Possible Impact Scenarios")

    st.table(df_results)