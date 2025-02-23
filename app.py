import streamlit as st
from utils.crater_functions import *
from utils.plot_craters import *
from utils.crater_types import crater_types
from utils.ui.utils_ui import *

# === STREAMLIT UI ===
st.set_page_config(
    page_title="EasyCraterSim", 
    page_icon="☄️",
    menu_items={
        'About': "# EasyCraterSim\nEasyCraterSim is a numerical simulation tool for modeling impact crater formation. It is based on the work of O'Keefe & Ahrens (1999) and developed as part of the Mathematical Modeling course at Université Paris-Saclay. More on the GitHub!\nby M. Soares Correia"
    }
    )

style = "<style>.row-widget.stButton {text-align: center; width: 300px;}</style>"
st.markdown(style, unsafe_allow_html=True)

show_title()

# === CHOOSE MODE ===
mode = st.radio("Select Mode:", ["Single Crater", "Compare Two Craters"])

st.divider()

# === SIDEBAR ===
show_sidebar()


# === SINGLE CRATER MODE ===
if mode == "Single Crater":
    exec(open("modes/single_crater.py", encoding="utf-8").read())

# === COMPARISON MODE ===
if mode == "Compare Two Craters":
    exec(open("modes/comparison.py", encoding="utf-8").read())

