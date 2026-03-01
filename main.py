import os
import requests
from google import genai
from google.genai import types
from pymongo import MongoClient
from datetime import datetime

# Get Secrets
NEWSDATA_KEY = os.getenv("NEWSDATA_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Clients
ai_client = genai.Client(api_key=GEMINI_KEY)
db_client = MongoClient(MONGO_URI)
db = db_client['news_aggregator']
collection = db['articles']

def classify_industry(title, snippet):
    prompt = f"Title: {title}\nSnippet: {snippet}"
    try:
        response = ai_client.models.generate_content(
            model="gemini-2.0-flash", # Use 2.0 Flash for stability
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="Categorize into EXACTLY one: [Tech, Finance, Healthcare, Energy, Sports, Politics]. Respond with ONLY the word.",
                temperature=0.1
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "General"

def run_pipeline():
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_KEY}&language=en"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Fetch failed: {res.status_code}")
        return

    articles = res.json().get("results", [])
    for item in articles:
        if collection.find_one({"link": item['link']}):
            continue 
        industry = classify_industry(item['title'], item.get('description', ''))
        doc = {
            "title": item['title'],
            "link": item['link'],
            "description": item.get('description', ''),
            "industry": industry,
            "source": item.get('source_id', 'Unknown'),
            "captured_at": datetime.utcnow()
        }
        collection.insert_one(doc)
        print(f"Saved: [{industry}] {item['title'][:50]}")

if __name__ == "__main__":
    run_pipeline()
