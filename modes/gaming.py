import streamlit as st
import random
import difflib

from utils.ui.utils_ui import *
from utils.craters_database import CRATERS

def clear_session():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

def clear_text():
    st.session_state.text = ""

def guess_the_crater():
    if "selected_crater" not in st.session_state:
        st.session_state.selected_crater = random.choice(CRATERS)
    if "show_hint" not in st.session_state:
        st.session_state.show_hint = False
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0 
    if "text" not in st.session_state:
        st.session_state.text = "✍️ Type the crater name:"

    selected_crater = st.session_state.selected_crater

    st.write("### Can you guess the name of this crater?")
    st.write(f"🌍 **Planet:** {selected_crater['planet']}")
    st.write("📌 You can ask for a hint if needed!")

    if st.button("🔍 Show Hint"):
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        st.write(f"💡 **Hint:** {selected_crater['hint']}")

    user_guess = st.text_input(st.session_state.text, on_change=clear_text).strip()

    crater_names = [c["name"] for c in CRATERS]
    close_matches = difflib.get_close_matches(user_guess, crater_names, n=1, cutoff=0.8)

    if st.button("Submit Guess"):
        st.session_state.attempts += 1  

        if close_matches and close_matches[0].lower() == selected_crater["name"].lower():
            st.success(f"🎉 Correct! The crater is **{selected_crater['name']}**.")
            
            st.write(f"🔹 **Diameter:** {selected_crater['diameter']} km")
            st.write(f"🔹 **Depth:** {selected_crater['depth']} km")
            st.write(f"🔹 **Impact Energy:** {selected_crater['energy']:.2e} J")
            st.write(f"🎯 **Attempts Taken: {st.session_state.attempts}**")

            st.image(selected_crater["image"], caption=selected_crater["caption"], use_container_width=True)

            st.button("Try Another Crater", on_click=clear_session)
        else:
            st.error("❌ Wrong guess! Try again.")

