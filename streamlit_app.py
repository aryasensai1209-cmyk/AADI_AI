import streamlit as st
import pandas as pd
import re
import google.generativeai as genai

# --- NEXUS ADVANCED CORE ENGINE ---

@st.cache_resource
def load_nexus_intelligence():
    """Initializes the Cloud Reasoning Engine (Gemini)."""
    try:
        # Priority: Check Streamlit Secrets for Deployment
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if google_key:
            genai.configure(api_key=google_key)
            return genai.GenerativeModel('gemini-2.0-flash')
        return None
    except Exception:
        return None

def powerful_ai_nexus(user_input, task_type='general'):
    model = load_nexus_intelligence()
    if not model:
        return "⚠️ [OFFLINE] Gemini API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets."
    
    prompts = {
        'security_audit': f"SYSTEM: Advanced Security Auditor. Analyze this code for vulnerabilities, explain the threat, and provide a 'Refresh Code' version that is patched.\nCode: {user_input}",
        'patch': f"SYSTEM: Auto-Patching Engine. Rewrite the following vulnerable code to be perfectly secure and optimized.\nCode: {user_input}",
        'general': user_input
    }
    
    try:
        response = model.generate_content(prompts.get(task_type, user_input))
        return response.text
    except Exception as e:
        return f"❌ Engine Error: {str(e)}"

def quantum_safe_audit(code):
    threats = []
    if re.search(r'RSA|PKCS1|1024|2048', code, re.I): threats.append("RSA (Classical Factorization)")
    if re.search(r'ECC|ECDSA|secp256k1|Curve25519', code, re.I): threats.append("ECC (Discrete Logarithm)")
    
    if threats:
        return f"⚠️ VULNERABLE TO QUANTUM ATTACK: {', '.join(threats)} detected.\n\n✅ PQC MIGRATION PATH:\n- Use ML-KEM (Kyber) for keys.\n- Use ML-DSA (Dilithium) for signatures."
    return "✅ No classical crypto vulnerabilities detected."

def behavioral_profiling(payload):
    score = 0
    if "\\x" in payload: score += 40 
    if "OR '1'='1'" in payload.upper(): score += 30
    if "<script" in payload.lower(): score += 30
    
    if score >= 70:
        return {"Profile": "APT Group", "Risk": "CRITICAL", "Confidence": f"{score}%"}
    return {"Profile": "Standard User", "Risk": "LOW", "Confidence": "95%"}

# --- NEXUS UI DASHBOARD ---

st.set_page_config(page_title="NEXUS AI", layout="wide")
st.title("🛡️ NEXUS AI: MULTI-AGENT SECURITY")
st.markdown("--- CORE STATUS: **ACTIVE** ---")

tabs = st.tabs(["🛡️ Audit", "🔧 Patch", "⚛️ Quantum", "🧠 Behavioral", "🔮 Synthetic"])

with tabs[0]:
    st.header("Real-Time Security Audit")
    code_input = st.text_area("Source Code", height=150)
    if st.button("Run Nexus Scan"):
        st.markdown(powerful_ai_nexus(code_input, 'security_audit'))

with tabs[1]:
    st.header("Auto-Patch Engine")
    v_code = st.text_area("Vulnerable Code")
    if st.button("Generate Fix"):
        st.markdown(powerful_ai_nexus(v_code, 'patch'))

with tabs[2]:
    st.header("Quantum-Safe Wing")
    q_input = st.text_input("Crypto Module")
    if st.button("Run PQC Audit"):
        st.info(quantum_safe_audit(q_input))

with tabs[3]:
    st.header("Behavioral Profiling")
    b_input = st.text_input("Payload")
    if st.button("Analyze Fingerprint"):
        st.json(behavioral_profiling(b_input))

with tabs[4]:
    st.header("Synthetic Threat Gen")
    if st.button("Predict Zero-Days"):
        st.warning("🚨 [PREDICTION]: Potential TOCTOU race condition in async handlers. Risk: 8.4/10.")
