import streamlit as st

from modes.gaming import guess_the_crater
from utils.ui.utils_ui import *

st.set_page_config(
    page_title="EasyCraterSim - Games", 
    page_icon="🎮",
    menu_items={
        'About': "# EasyCraterSim\nEasyCraterSim is a numerical simulation tool for modeling impact crater formation. It is based on the work of O'Keefe & Ahrens (1999) and developed as part of the Mathematical Modeling course at Université Paris-Saclay. More on the GitHub!\nby M. Soares Correia"
    }
    )

show_title()
show_sidebar()

st.markdown(
    """<h2 style="text-align: center"> 
            Games 
        </h2>
    """, unsafe_allow_html=True)



# 📌 Choix du mode de jeu
game_choice = st.radio("Choose your challenge:", ["🔎 Guess the Crater"])

# 📌 Affichage du jeu sélectionné
if game_choice == "🔎 Guess the Crater":
    guess_the_crater()
