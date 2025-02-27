import streamlit as st
import matplotlib.pyplot as plt
from utils.crater_functions import estimate_impactor, calculate_crater_param
from utils.ui.utils_ui import *

st.set_page_config(
    page_title="EasyCraterSim - About", 
    page_icon="☄️",
    menu_items={
        'About': "# EasyCraterSim\nEasyCraterSim is a numerical simulation tool for modeling impact crater formation. It is based on the work of O'Keefe & Ahrens (1999) and developed as part of the Mathematical Modeling course at Université Paris-Saclay. More on the GitHub!\nby M. Soares Correia"
    }
    )

show_title()
show_sidebar()

st.subheader("ℹ️ About EasyCraterSim")
st.write("A scientific tool for impact crater simulation and analysis.")

# INTRODUCTION 
st.header("📖 Introduction & Objectives")
st.write("""
EasyCraterSim is a scientific simulation tool designed to model the formation of impact craters on different planetary surfaces.
It allows users to estimate crater characteristics based on an impactor’s properties and to perform inverse simulations to determine the possible impactor for a given crater.

The project was developed as part of the **Mathematical Modeling course** under the supervision of **E. Léger and H. Massol**, at **Université Paris-Saclay**.
It is based on established **impact cratering physics** and empirical scaling laws from geological studies.
""")

st.image("images/38571_MRO-HIRISE-Mars-Small-Blue-Ice-Crater-PIA18115.jpg", caption="Small Blue Ice Crater, Mars, MRO HIRISE NASA", use_container_width=True)


# METHODO
st.header("🧪 Methodology")
st.write("""
The simulation relies on **empirical scaling laws** and **hydrodynamic models** to estimate the final crater morphology.
It takes into account:
- Gravity and surface density of the planetary body.
- Velocity, density, and size of the impactor.
- Energy dissipation and excavation mechanics.

The approach follows classical impact cratering studies, including those by **O’Keefe & Ahrens (1999)** and **Holsapple (1993)**.
""")

st.image("images/method.png", caption="Figure from O'Keefe & Ahrens (1999)", use_container_width=True)


# HOW
st.header("🖥️ How EasyCraterSim Works")
st.write("""
The simulation consists of two main modes:
1. **Single Crater Simulation**: The user inputs the impactor properties, and the program calculates the resulting crater.
2. **Reverse Simulation**: The user inputs a known crater properties, and the program estimates the properties of the impactor.

The model includes:
- **Energy of impact** estimation.
- **Transient and final crater dimensions** calculation.
- **Comparison with real impact craters** to estimate similarity.
""")

st.image("images/meteor_crater.gif", caption="Meteor Crater (USA) animation generated by EasyCraterSim", use_container_width=True)


# DATA AND REF
st.header("📂 Data & References")
st.markdown("""
- **O’Keefe, J.D. & Ahrens, T.J.** (1999). Complex craters: Relationship of stratigraphy and rings to impact conditions. *Journal of Geophysical Research: Planets*.
- **Holsapple, K.A.** (1993). The scaling of impact processes in planetary sciences. *Annual Review of Earth and Planetary Sciences*.
- **Melosh, H.J.** (1989). Impact Cratering: A Geologic Process. *Oxford University Press*.
""")

st.divider()

# CONTACT
st.write("### 📬 Contact")
st.write("""
If you have any questions or want to contribute, feel free to contact us:
📧 **Email**: maxime.soares-correia@universite-paris-saclay.fr  
🌍 [**GitHub Repository**](https://github.com/MaxSC4/EasyCraterSim)
""")