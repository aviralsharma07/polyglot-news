import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWSAPI_KEY")

def fetch(query="technology", page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": page_size,
        "apiKey": API_KEY,
        "language": "en",
        "sortBy": "publishedAt"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()   # ← learn what this does
    return response.json()

