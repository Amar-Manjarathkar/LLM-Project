import streamlit as st
import requests
import json

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/analyze"
st.set_page_config(page_title="UPEF Intel Dashboard", layout="wide")

# --- Header ---
st.title("🕵️‍♂️ UPEF Intelligence Command Center (Safe Mode)")
st.markdown("---")

# --- Sidebar Status ---
with st.sidebar:
    st.header("System Status")
    try:
        status = requests.get("http://127.0.0.1:8000/", timeout=5).json()
        st.success(f"Backend: {status['status']}")
        st.caption(f"Model: {status['model']}")
    except:
        st.error("Backend Offline")
        st.info("Please ensure 'main.py' is running.")

# --- Main Interface ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Incoming Intercept")
    with st.form("analysis_form"):
        raw_text = st.text_area("Paste raw intelligence here:", height=300)
        submitted = st.form_submit_button("⚡ ANALYZE INTEL", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 Analysis Report")
    
    if submitted and raw_text:
        with st.spinner("Processing... (This may take 1-2 minutes)"):
            try:
                # TIMEOUT SET TO 300 SECONDS (5 Minutes)
                payload = {"text": raw_text}
                response = requests.post(API_URL, json=payload, timeout=300)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 1. High Level Metrics
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Language", data['language']['detected_language'])
                    c2.metric("Is Romanized?", str(data['language']['is_romanized']))
                    c3.metric("Domain", data['domain']['category'])
                    
                    st.divider()
                    
                    # 2. Entities (Standard Text Only - No HTML)
                    st.write("#### 🎯 Detected Entities")
                    if data['entities']:
                        for ent in data['entities']:
                            # Using standard streamlit containers instead of HTML
                            with st.container(border=True):
                                st.write(f"**{ent['label']}**: {ent['text']}")
                                st.caption(f"Confidence: {ent['confidence']}% | Logic: {ent['reasoning']}")
                    else:
                        st.info("No specific entities detected.")

                    # 3. Raw Data
                    st.divider()
                    with st.expander("📂 View Raw JSON"):
                        st.json(data)
                        
                else:
                    st.error(f"Server Error {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.ReadTimeout:
                st.error("❌ Timeout: The AI took too long to respond.")
                st.info("Tip: Your computer is processing it, but Streamlit gave up waiting.")
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")