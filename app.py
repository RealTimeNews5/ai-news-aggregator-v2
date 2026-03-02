import streamlit as st
from pymongo import MongoClient
import dns.resolver

try:
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
except:
pass

st.set_page_config(page_title="AI News Dashboard", layout="wide")

@st.cache_resource
def init_connection():
return MongoClient(st.secrets["MONGO_URI"], tlsAllowInvalidCertificates=True)

try:
client = init_connection()
db = client['news_aggregator']
collection = db['articles']
st.title("🌐 AI-Powered Industry News")
industries = ["All", "Tech", "Finance", "Healthcare", "Energy", "Sports", "Politics"]
selected = st.sidebar.selectbox("Category Filter", industries)
query = {} if selected == "All" else {"industry": selected}
articles = list(collection.find(query).sort("captured_at", -1).limit(20))
if not articles:
st.info("Connected! No articles found yet.")
else:
for art in articles:
st.subheader(art['title'])
st.write(art.get('description', 'No description.'))
st.link_button("Read Full Story", art['link'])
st.divider()
except Exception as e:
st.error(f"Connection Error: {e}")
