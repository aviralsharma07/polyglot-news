import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GNEWSAPI_KEY")

def fetch(query="technology", max_results=10):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "max": max_results,
        "token": API_KEY,
        "lang": "en"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()   # ← learn what this does
    return response.json()
