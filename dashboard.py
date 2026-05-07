import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="SmartCyberDetect", layout="centered")

st.title("🛡️ SmartCyberDetect Dashboard")

st.write("AI Cyberattack Detection Platform")

# Load model
model = pickle.load(open("model.pkl", "rb"))

traffic = st.slider("Network Traffic", 0.0, 1.0, 0.5)

if st.button("Detect Attack"):

    prediction = model.predict([[traffic]])

    if prediction[0] == 1:
        st.error("⚠️ Attack Detected!")
    else:
        st.success("✅ Normal Traffic")