import streamlit as st

def show_sidebar():
    # === SIDEBAR ===
    st.sidebar.header("☄️ EasyCraterSim")

    # === NAVIGATION ===
    st.sidebar.subheader("📃 Pages")

    st.sidebar.page_link("app.py", label="Impact Crater Simulation", icon="☄️")
    st.sidebar.page_link("pages/reverse_sim.py", label="Reverse Simulation (WIP)", icon="🔙")
    st.sidebar.page_link("pages/about.py", label="About", icon="📄")

    st.sidebar.divider()

    # === CONTACT ===
    st.sidebar.subheader("📬 Contact Info")
    st.sidebar.write("📧 Email: maxime.soares-correia@universite-paris-saclay.fr")
    st.sidebar.write("[🌍 GitHub Repo](https://github.com/MaxSC4/EasyCraterSim)")

def show_title():
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