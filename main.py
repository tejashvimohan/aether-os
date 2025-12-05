import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# --- 1. SYSTEM CONFIG ---
st.set_page_config(
    page_title="AETHER | Liquid Interface OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- 2. SIDEBAR (SYSTEM TRAY) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/12308/12308643.png", width=50)
    st.markdown("## AETHER OS")
    st.caption("v2.5.0 | GENERATIVE KERNEL")
    
    st.markdown("---")
    
    # 🔑 KEY INPUT
    api_key = st.text_input("ACCESS TOKEN (Gemini)", type="password")
    
    st.markdown("### 🎛️ CORE SELECTOR")
    mode = st.radio(
        "Select Engine:",
        ["🎨 Web Designer (HTML/CSS)", "⚡ Logic Architect (Python)"],
        captions=["Best for Landing Pages, Cards, Visuals", "Best for Calculators, Graphs, Tools"]
    )
    
    debug_mode = st.toggle("Debug Protocol", value=False)

# --- 3. MAIN HEADER ---
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>AETHER INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; margin-bottom: 40px;'>DESCRIBE THE INTERFACE. THE SYSTEM WILL FORGE IT.</p>", unsafe_allow_html=True)

# --- 4. INPUT MATRIX ---
col_main, _ = st.columns([1, 0.01]) # Centered feel
user_prompt = col_main.text_input("", placeholder="> Describe your desired interface (e.g., 'A futuristic landing page for a Space Travel agency')", max_chars=300)

generate_btn = col_main.button("INITIATE BUILD SEQUENCE ⚡")

# --- 5. GENERATIVE CORE ---
if generate_btn and user_prompt:
    if not api_key:
        st.error("⛔ ACCESS DENIED: API KEY MISSING IN SIDEBAR")
    else:
        try:
            genai.configure(api_key=api_key)
            # Use Flash for speed and free tier access
            model = genai.GenerativeModel('gemini-2.5-flash') 
            
            with st.spinner("⚡ AETHER IS COMPILING ASSETS..."):
                
                # === ENGINE 1: WEB DESIGNER (HTML/TAILWIND) ===
                if "Web Designer" in mode:
                    system_prompt = f"""
                    You are a world-class Frontend Engineer.
                    Task: Create a Single-File HTML/CSS/JS website based on this request: "{user_prompt}".
                    
                    CRITICAL RULES:
                    1. Use Tailwind CSS via CDN for styling.
                    2. Make it BEAUTIFUL: Use gradients, shadows, rounded corners, and modern typography.
                    3. Make it RESPONSIVE and centered.
                    4. Include FontAwesome for icons.
                    5. Return ONLY the raw HTML code. Do NOT wrap in markdown blocks.
                    6. The design must be modern, clean, and impressive.
                    """
                    
                    response = model.generate_content(system_prompt)
                    html_code = response.text.replace("```html", "").replace("```", "").strip()
                    
                    st.success("Rendering Visual Interface...")
                    
                    # RENDER IN IFRAME
                    with st.container(border=True):
                        st.markdown("### 🌐 Live Preview")
                        components.html(html_code, height=600, scrolling=True)
                        
                        with st.expander("View Source (HTML)"):
                            st.code(html_code, language="html")

                # === ENGINE 2: LOGIC ARCHITECT (PYTHON/STREAMLIT) ===
                else:
                    system_prompt = f"""
                    You are a Python Streamlit Expert.
                    Task: Write a script to solve: "{user_prompt}".
                    
                    CRITICAL RULES:
                    1. Return ONLY raw Python code. NO markdown blocks.
                    2. Use st.columns, st.metric, st.container for layout.
                    3. Use Plotly Express (px) for graphs.
                    4. Do NOT use st.set_page_config.
                    5. Make it interactive (sliders, buttons).
                    """
                    
                    response = model.generate_content(system_prompt)
                    py_code = response.text.replace("```python", "").replace("```", "").strip()
                    
                    st.success("Compiling Logic Modules...")
                    
                    # EXECUTE PYTHON
                    with st.container(border=True):
                        local_scope = {"st": st, "pd": pd, "np": np, "px": px, "plt": plt}
                        try:
                            exec(py_code, {}, local_scope)
                        except Exception as e:
                            st.error(f"Runtime Error: {e}")
                            if debug_mode:
                                st.code(traceback.format_exc())
                                
                    if debug_mode:
                        with st.expander("View Logic (Python)"):
                            st.code(py_code, language="python")

        except Exception as e:
            st.error(f"SYSTEM FAILURE: {str(e)}")

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #444; font-size: 12px;'>AETHER OS v2.5 | POWERED BY GEMINI FLASH</div>", unsafe_allow_html=True)