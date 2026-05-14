import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CURRENTAPI_KEY")

def fetch(query="technology", page_size=10):
    url = "https://api.currentsapi.services/v1/search"
    params = {
        "keywords": query,
        "apiKey": API_KEY,
        "language": "en",
        "limit": page_size
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()