import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import os

# --- 1. DATABASE CONNECTION ---
# We use a try-except block to catch connection issues early
try:
    # This pulls the MONGO_URI from your Streamlit "Advanced Settings > Secrets"
    if "MONGO_URI" in st.secrets:
        MONGO_URL = st.secrets["MONGO_URI"]
        # tlsAllowInvalidCertificates helps prevent connection drops on some cloud servers
        client = MongoClient(MONGO_URL, tlsAllowInvalidCertificates=True)
        db = client['news_aggregator']
        collection = db['articles']
    else:
        st.error("Missing Secret: Please add 'MONGO_URI' in Streamlit Advanced Settings.")
        st.stop()
except Exception as e:
    st.error(f"Database Connection Failed: {e}")
    st.stop()

# --- 2. PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="AI Industry News", 
    page_icon="🌐", 
    layout="wide"
)

# Custom CSS to make it look modern
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .news-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        background-color: white;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🔍 Filter News")
industries = ["All", "Tech", "Finance", "
