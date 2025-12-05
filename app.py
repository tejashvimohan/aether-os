import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
import os  # <--- CRITICAL IMPORT

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="AETHER | Generative OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the Futuristic CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("style.css")
except FileNotFoundError:
    pass # prevent crash if css is missing

# --- 2. SESSION STATE MANAGEMENT ---
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "active_mode" not in st.session_state:
    st.session_state.active_mode = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# --- 3. SIDEBAR (CONTROL PANEL) ---
with st.sidebar:
    st.markdown("## 💠 AETHER  OS")
    st.caption("v3.0.1 | LIQUID INTERFACE ENGINE")
    st.markdown("---")
    
    # 🔑 ROBUST KEY HANDLING (Fixed for Render)
    api_key = None
    
    # Check 1: Render/System Environment Variable
    if os.environ.get("GEMINI_API_KEY"):
        api_key = os.environ.get("GEMINI_API_KEY")
        st.success("☁️ CLOUD ACCESS ENABLED")
    
    # Check 2: Streamlit Secrets (Fall back if env var not found)
    elif not api_key:
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
                st.success("☁️ CLOUD ACCESS ENABLED")
        except:
            pass # Ignore errors if secrets.toml doesn't exist

    # Check 3: User Input (If no cloud key found)
    if not api_key:
        api_key = st.text_input("ACCESS KEY (Gemini)", type="password", help="Get a free key from Google AI Studio")
        if not api_key:
            st.warning("⚠️ Please enter a Key to start.")
            st.markdown("[Get a Free Key](https://aistudio.google.com/app/apikey)")

    st.markdown("### 🎛️ ENGINE SELECTOR")
    engine_mode = st.radio(
        "Select Core:",
        ["⚡ Logic Architect", "🎨 Visual Designer"],
        captions=["Python/Streamlit Tools", "HTML/Tailwind Interfaces"]
    )
    
    st.markdown("---")
    
    # Quick Prompts
    st.markdown("### 🚀 QUICK BOOT")
    if st.button("Calc: Mortgage Estimator"):
        st.session_state.last_prompt = "Create a Mortgage Calculator with sliders for Principal, Rate, and Years. Show monthly payment and a pie chart of Total Interest vs Principal."
        st.session_state.active_mode = "⚡ Logic Architect"
    
    if st.button("Vis: Cyberpunk Landing"):
        st.session_state.last_prompt = "A landing page for 'Neon Coffee' with a dark theme, glowing neon buttons, a menu grid, and a footer."
        st.session_state.active_mode = "🎨 Visual Designer"

    st.markdown("---")
    
    st.markdown("###  Designed By Tejashvi ")
    st.markdown("---")
    
# --- 4. MAIN INTERFACE ---
st.title("AETHER INTELLIGENCE")
st.markdown("#### *State your intent. The system will forge the interface.*")

# Main Input Area
col_input, col_btn = st.columns([4, 1])
with col_input:
    user_prompt = st.text_input("", placeholder="> Describe the tool or interface you need...", value=st.session_state.last_prompt if st.session_state.last_prompt else "")

with col_btn:
    # Spacer to align button
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("BUILD ⚡", use_container_width=True)

# --- 5. GENERATION LOGIC ---
if generate_btn and user_prompt:
    if not api_key:
        st.error("⛔ CRITICAL ERROR: API KEY MISSING")
    else:
        # Update Session State
        st.session_state.last_prompt = user_prompt
        st.session_state.active_mode = engine_mode
        
        try:
            # Initialize Gemini (Using 1.5-flash for speed/reliability)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Progress Animation
            progress_bar = st.progress(0, text="Parsing User Intent...")
            time.sleep(0.5)
            
            # --- ENGINE 1: LOGIC ARCHITECT (PYTHON) ---
            if engine_mode == "⚡ Logic Architect":
                progress_bar.progress(40, text="Architecting Logic Modules...")
                
                system_prompt = f"""
                You are an Expert Python Streamlit Developer.
                Task: Write a COMPLETE, RUNNABLE Python script to satisfy: "{user_prompt}".
                
                CRITICAL RULES:
                1. Return ONLY raw Python code. NO markdown blocks.
                2. Do NOT use st.set_page_config.
                3. Use 'st' for Streamlit, 'pd' for pandas, 'np' for numpy, 'px' for plotly.
                4. Create interactive widgets (sliders, inputs, buttons).
                5. Use st.columns for layout.
                6. Ensure all variables are defined before use.
                """
                
                response = model.generate_content(system_prompt)
                st.session_state.generated_code = response.text.replace("```python", "").replace("```", "").strip()
            
            # --- ENGINE 2: VISUAL DESIGNER (HTML) ---
            else:
                progress_bar.progress(40, text="Compiling Visual Assets...")
                
                system_prompt = f"""
                You are a World-Class UI/UX Designer.
                Task: Create a Single-File HTML/CSS/JS website based on: "{user_prompt}".
                
                CRITICAL RULES:
                1. Use Tailwind CSS via CDN (<script src="https://cdn.tailwindcss.com"></script>).
                2. Use FontAwesome for icons.
                3. Make it BEAUTIFUL: Gradients, shadows, rounded corners.
                4. Make it RESPONSIVE and centered.
                5. Return ONLY raw HTML code. NO markdown blocks.
                """
                
                response = model.generate_content(system_prompt)
                st.session_state.generated_code = response.text.replace("```html", "").replace("```", "").strip()

            progress_bar.progress(100, text="Rendering Interface...")
            time.sleep(0.5)
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"GENERATION FAILED: {str(e)}")

# --- 6. RENDERER (THE SANDBOX) ---
if st.session_state.generated_code:
    st.markdown("---")
    
    # LOGIC CORE RENDERER
    if st.session_state.active_mode == "⚡ Logic Architect":
        st.caption("🟢 RUNTIME ENVIRONMENT: PYTHON KERNEL ACTIVE")
        with st.container(border=True):
            # Safe Local Scope
            local_scope = {"st": st, "pd": pd, "np": np, "px": px, "plt": plt}
            try:
                exec(st.session_state.generated_code, {}, local_scope)
            except Exception as e:
                st.error("RUNTIME ERROR IN GENERATED CODE:")
                st.code(e)
                st.warning("Try tweaking your prompt.")

    # DESIGN CORE RENDERER
    else:
        st.caption("🔵 RUNTIME ENVIRONMENT: WEBKIT RENDERER ACTIVE")
        with st.container(border=True):
            components.html(st.session_state.generated_code, height=700, scrolling=True)

    # SOURCE CODE VIEWER (For Examiners)
    with st.expander("👁️ VIEW GENERATED SOURCE CODE"):
        lang = "python" if st.session_state.active_mode == "⚡ Logic Architect" else "html"
        st.code(st.session_state.generated_code, language=lang)