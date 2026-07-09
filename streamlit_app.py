import streamlit as st
import pandas as pd
import re
import requests
import google.generativeai as genai
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- NEXUS V11: DUAL-ENGINE INTELLIGENCE (2.5 FLASH EDITION) ---

def nexus_query(prompt, engine_type="hybrid"):
    """Orchestrates between Gemini 2.5 Flash and Mistral 7B cores with robust failover."""
    hf_token = st.secrets.get("HF_TOKEN")
    gemini_key = st.secrets.get("GOOGLE_API_KEY")

    # 1. STRATEGIC ENGINE (Gemini 2.5 Flash)
    if engine_type in ["hybrid", "strategic"]:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            response = model.generate_content(f"Act as NEXUS V11. {prompt}")
            return re.sub(r'Mistral|Gemini|Google|OpenAI', 'NEXUS V11', response.text, flags=re.I)
        except Exception as e:
            if engine_type == "strategic": return f"┑ Strategic Core Error: {str(e)}"

    # 2. TECHNICAL ENGINE (Mistral 7B via HF) - REINFORCED FOR DNS/NETWORK STABILITY
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": f"<s>[INST] As NEXUS V11: {prompt} [/INST]", "parameters": {"max_new_tokens": 1000}}

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504], raise_on_status=False)
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        resp = session.post(API_URL, headers=headers, json=payload, timeout=(5, 20))
        if resp.status_code == 200:
            raw = resp.json()[0]['generated_text'].split('[/INST]')[-1].strip()
            return re.sub(r'Mistral|Gemini|Google|OpenAI', 'NEXUS V11', raw, flags=re.I)
        return f"☑ Technical Core Logic Unstable (Status: {resp.status_code})"
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return "⌕ NEXUS ADVISORY: Technical Core unreachable (DNS/Network). Strategic Engine remains active."
    except Exception as e:
        return f"❌ Logic Matrix Latency: {str(e)}"

st.set_page_config(page_title="NEXUS V11", layout="wide")

st.markdown("""<style>.main-header {font-size: 50px !important; font-weight: 900; color: #00FFAA; text-align: center;}.stButton>button {width: 100%; background-color: #00FFAA; color: black; font-weight: bold;}</style>""", unsafe_allow_html=True)
st.markdown('<p class="main-header">☑ NEXUS V11: THE ORCHESTRATOR</p>', unsafe_allow_html=True)

tabs = st.tabs(["☑ GLOBAL AUDIT", "☑ AUTO-PATCH", "☑ QUANTUM", "☑ NEURO-PROFILE", "☑ ZERO-DAY"])

with tabs[0]:
    st.subheader("☑ Global Infrastructure Audit (v2.5)")
    audit_in = st.text_area("Inject system logic or code for dual-engine scan:", height=150, key="audit_area")
    if st.button("ACTIVATE GLOBAL SCAN"):
        if audit_in:
            with st.spinner("☑ NEXUS CORE ANALYZING..."):
                st.info(nexus_query(f"Perform an exhaustive security audit on: {audit_in}"))

with tabs[1]:
    st.subheader("☑ Secure Auto-Patch & Refresh")
    patch_in = st.text_area("Enter Vulnerable Logic:", height=150, key="patch_area")
    if st.button("GENERATE SECURE PATCH"):
        if patch_in:
            with st.spinner("☑ RE-ENGINEERING..."):
                st.code(nexus_query(f"Rewrite this code to be secure and resistant to modern exploits: {patch_in}"), language="python")

with tabs[2]:
    st.subheader("☑ Quantum-Safe Migration Wing")
    q_in = st.text_input("Enter Cryptographic Matrix (RSA/ECC):", key="q_area")
    if st.button("RUN QUANTUM AUDIT"):
        if q_in:
            with st.spinner("☑ CALCULATING THREAT VECTORS..."):
                st.success(nexus_query(f"Analyze this for Shor's algorithm vulnerability and provide PQC path: {q_in}"))

with tabs[3]:
    st.subheader("☑ Neuro-Behavioral Profiling")
    prof_in = st.text_area("Attacker Payload Structure:", key="prof_area")
    if st.button("GENERATE FINGERPRINT"):
        if prof_in:
            with st.spinner("☑ DECODING ATTACKER INTENT..."):
                st.warning(nexus_query(f"Profile this payload for behavior signature and origin: {prof_in}"))

with tabs[4]:
    st.subheader("☑ Synthetic Zero-Day Predictor")
    z_in = st.text_area("Application Logic Flow / Documentation:", key="z_area")
    if st.button("PREDICT VULNERABILITIES"):
        if z_in:
            with st.spinner("☑ SIMULATING FUTURE EXPLOITS..."):
                st.error(nexus_query(f"Analyze this logic flow and predict potential zero-day vulnerabilities: {z_in}"))
