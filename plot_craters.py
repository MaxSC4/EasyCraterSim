import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from crater_functions import *

def simulate(dp, Dp, crater_type, R_current, Z_current, params, t_slider):
    st.write("### Results")
    st.write(f"**Penetration depth** : {dp:.2f} m")
    st.write(f"**Transitory crater diameter** : {Dp:.2f} m")
    st.write(f"**Crater type** : {crater_type}")
    
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
    
    ax.fill_between(r, np.minimum(z, z_lip), -3, color='tan', alpha=0.6, label="Impacted Surface")
    ax.fill_between(r, z_lip, 0.1, color='white')
    ax.plot(r, z_lip, color='darkred', linewidth=2, label=f"{crater_type} Crater")
    ax.set_xlabel("Normalized radius (r/a)")
    ax.set_ylabel("Normalized depth (z/a)")
    ax.legend()
    ax.set_xlim(-1.5 * r_crater, 1.5 * r_crater)
    ax.set_ylim(-3, 3)
    
    ax.text(0.02, 0.9, f"T = {t_slider:.1f}", transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    
    st.pyplot(fig)

def animate(dp, Dp, crater_type, R_values, Z_values, params, t_values):
    st.write("### Results")
    st.write(f"**Penetration depth** : {dp:.2f} m")
    st.write(f"**Transitory crater diameter** : {Dp:.2f} m")
    st.write(f"**Crater type** : {crater_type}")

    placeholder = st.empty()
    
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
        
        ax.fill_between(r, np.minimum(z, z_lip), -3, color='tan', alpha=0.6, label="Impacted Surface")
        ax.fill_between(r, z_lip, 0.1, color='white')
        ax.plot(r, z_lip, color='darkred', linewidth=2, label=f"{crater_type} Crater")
        ax.set_xlabel("Normalized radius (r/a)")
        ax.set_ylabel("Normalized depth (z/a)")
        ax.legend()
        ax.set_xlim(-1.5 * r_crater, 1.5 * r_crater)
        ax.set_ylim(-3, 3)
        ax.text(0.02, 0.9, f"T = {t_values[frame]:.1f}", transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        
        placeholder.pyplot(fig)
        plt.close(fig)
        
        time.sleep(0.05)


def generate(t_values, R_values, Z_values, params, crater_type):
    with st.spinner("Generating animation..."):
        gif_path = generate_crater_gif(t_values, R_values, Z_values, params["a"], crater_type)
        st.success("Animation generated successfully!")

    with open(gif_path, "rb") as file:
        gif_bytes = file.read()

    st.image(gif_bytes, caption="Crater Evolution Animation", use_container_width=True)
    st.download_button(
        label="📥 Download Animation (GIF)",
        data=gif_bytes,
        file_name="crater_evolution.gif",
        mime="image/gif"
    )

    os.remove(gif_path)