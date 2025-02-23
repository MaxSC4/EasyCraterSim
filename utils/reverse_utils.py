import numpy as np
import random
import streamlit as st
import pandas as pd

known_craters = {
    "Chicxulub": {"Dp": 150000, "depth": 30000, "a": 10000, "u": 25000, "energy": 10**23},
    "Meteor Crater": {"Dp": 1200, "depth": 170, "a": 500, "u": 15000, "energy": 10**19},
    "Tycho": {"Dp": 86000, "depth": 4500, "a": 8000, "u": 20000, "energy": 10**22},
    "Gale": {"Dp": 154000, "depth": 5000, "a": 12000, "u": 18000, "energy": 10**22}
}

def generate_impact_scenarios(Dp_final, depth_final, rho_surface, rho_planet):
    """Generate different possible combos of impactors for a given crater"""

    scenarios = []
    
    # Different speed and density
    velocity_range = np.linspace(5, 50, 10) * 1000  # 5 à 50 km/s
    density_range = np.linspace(2, 8, 5) * 1000  # 2 à 8 g/cm³ en kg/m³
    
    for U in velocity_range:
        for delta_impactor in density_range:
            # Inversed empirical equation
            a = (Dp_final / (1.82 * (rho_planet / delta_impactor) ** -0.26 * (9.81 * Dp_final / U ** 2) ** -0.22))
            
            # Impact energy
            volume = (4/3) * np.pi * (a ** 3)
            mass = volume * delta_impactor
            energy = 0.5 * mass * (U ** 2)
            
            # Check the impact has the right depth
            depth_calc = 0.3 * a * (delta_impactor / rho_surface) ** (1/3)
            if abs(depth_calc - depth_final) / depth_final < 0.2:  # 20% tolerance
                scenarios.append([a, U / 1000, delta_impactor / 1000, energy])

    return scenarios


def similarity_score(Dp, depth, a, energy):
    """
    Compare results with a known crater and give a similarity score
    """
    scores = {}

    for name, crater in known_craters.items():
        d_score = abs(Dp - crater["Dp"]) / max(crater["Dp"], 1)
        depth_score = abs(depth - crater["depth"]) / max(crater["depth"], 1)
        impactor_score = abs(a - crater["a"]) / max(crater["a"], 1)
        energy_score = abs(energy - crater["energy"]) / max(crater["energy"], 1)

        total_score = (0.25 * d_score) + (0.25 * depth_score) + (0.25 * impactor_score) + (0.25 * energy_score)

        scores[name] = max(0, (1 - total_score) * 100)  

    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3])
    return sorted_scores


def generate_random_scenario():
    max_attempts = 200
    found_valid = False

    for _ in range(max_attempts):
        Dp_final = random.choice([random.uniform(0.5, 5) * 1000, 
                                  random.uniform(5, 50) * 1000, 
                                  random.uniform(50, 300) * 1000])
        
        depth_final = random.uniform(50, 30000)  
        rho_planet = random.uniform(2.0, 5.0) * 1000
        rho_surface = random.uniform(1.5, 3.5) * 1000

        scenarios = generate_impact_scenarios(Dp_final, depth_final, rho_surface, rho_planet)

        for a, U, density, energy in scenarios:
            similarities = similarity_score(Dp_final, depth_final, a, energy)
            best_match, best_similarity = max(similarities.items(), key=lambda x: x[1])
            if best_similarity > 10:
                found_valid = True
                break  

        if found_valid:
            break  

    if not found_valid:
        st.error("🚨 No valid random scenario found after multiple attempts. Try again!")
        scenarios = []



    return Dp_final, depth_final, rho_planet, rho_surface, scenarios