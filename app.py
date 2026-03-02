import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# --- 1. DATABASE CONNECTION ---
try:
    if "MONGO_URI" in st.secrets:
        MONGO_URL = st.secrets["MONGO_URI"]
        # Stable connection for cloud servers
        client = MongoClient(MONGO_URL, tlsAllowInvalidCertificates=True)
        db = client['news_aggregator']
        collection = db['articles']
    else:
        st.error("Missing Secret: Please add 'MONGO_URI' in Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Database Connection Failed: {e}")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="AI News", page_icon="🌐", layout="wide")
st.title("🌐 AI-Powered Industry News")

# --- 3. SIDEBAR ---
st.sidebar.title("Filters")
# Fixed industry list (no missing quotes)
industries = ["All", "Tech", "Finance", "Healthcare", "Energy", "Sports", "Politics"]
selected_industry = st.sidebar.selectbox("Select Category", industries)

# --- 4. FETCH & DISPLAY ---
query = {} if selected_industry == "All" else {"industry": selected_industry}

try:
    # Get latest 50 news items
    news_items = list(collection.find(query).sort("captured_at", -1).limit(50))
    
    if not news_items:
        st.warning("No articles found. Run your GitHub Action to fetch data!")
    else:
        for item in news_items:
            with st.container():
                st.write(f"**{item.get('industry', 'General').upper()}**")
                st.subheader(item['title'])
                st.write(item.get('description', 'No summary available.'))
                st.link_button("Read Article", item['link'])
                st.caption(f"Source: {item.get('source')} | {item['captured_at'].strftime('%Y-%m-%d %H:%M')}")
                st.divider()
except Exception as e:
    st.error(f"Error loading news: {e}")
