import streamlit as st
from pymongo import MongoClient
import os

# 1. Connection (This pulls from Streamlit's Secret Vault)
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client['news_aggregator']
collection = db['articles']

# 2. Page Design
st.set_page_config(page_title="AI News Aggregator", layout="wide")
st.title("🌐 AI Industry News Dashboard")

# 3. Sidebar Filter
industries = ["All", "Tech", "Finance", "Healthcare", "Energy", "Sports", "Politics"]
selected = st.sidebar.selectbox("Choose Industry", industries)

# 4. Show the News
query = {} if selected == "All" else {"industry": selected}
articles = list(collection.find(query).sort("captured_at", -1))

if not articles:
    st.warning(f"No articles found for {selected}. Run your GitHub Action to fetch some!")
else:
    for art in articles:
        with st.container():
            st.subheader(f"[{art['industry']}] {art['title']}")
            st.write(art.get('description', 'No summary available.'))
            st.link_button("Read Original Article", art['link'])
            st.caption(f"Source: {art.get('source')} | Captured: {art['captured_at']}")
            st.divider()
