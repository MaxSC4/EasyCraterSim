import streamlit as st
from EasyCraterSim.utils.crater_functions import *
from plot_craters import *
from EasyCraterSim.utils.crater_types import crater_types

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

st.markdown(
    """<h1 style="text-align: center">
            ☄️ EasyCraterSim
        </h1>
    """, unsafe_allow_html=True)

st.markdown(
    """<div style="text-align: center">
            <i>by M. Soares Correia</i>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# === CHOOSE MODE ===
mode = st.radio("Select Mode:", ["Single Crater", "Compare Two Craters"])

st.divider()

# === SIDEBAR ===
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
    st.sidebar.write("M. Soares Correia")

# === SINGLE CRATER MODE ===
if mode == "Single Crater":
    exec(open("modes/single_crater.py", encoding="utf-8").read())

# === COMPARISON MODE ===
if mode == "Compare Two Craters":
    exec(open("modes/comparison.py", encoding="utf-8").read())

