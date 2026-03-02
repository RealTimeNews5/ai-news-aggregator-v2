import streamlit as st
from pymongo import MongoClient
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

st.set_page_config(page_title="AI News Dashboard", layout="wide")

client = MongoClient(st.secrets["MONGO_URI"], tlsAllowInvalidCertificates=True)
db = client['news_aggregator']
collection = db['articles']

st.title("🌐 AI-Powered Industry News")
industries = ["All", "Tech", "Finance", "Healthcare", "Energy", "Sports", "Politics"]
selected = st.sidebar.selectbox("Category Filter", industries)
query = {} if selected == "All" else {"industry": selected}
articles = list(collection.find(query).sort("captured_at", -1).limit(20))

if not articles:
st.info("Connected! No articles found yet. Run your 'Fetcher' on GitHub Actions.")
else:
for art in articles:
st.subheader(art['title'])
st.write(art.get('description', 'No description.'))
st.link_button("Read Full Story", art['link'])
st.divider()
