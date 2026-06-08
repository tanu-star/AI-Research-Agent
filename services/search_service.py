import requests
from typing import List, Dict
from app.config import Config

class SearchService:
    """Web search service using Serper API"""
    
    def __init__(self):
        self.api_key = Config.SERPER_API_KEY
        self.url = "https://google.serper.dev/search"
    
    def search(self, query: str, num: int = 5) -> List[Dict]:
        if not self.api_key:
            return [{"error": "SERPER_API_KEY not configured"}]
        
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": num}
        
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=15)
            data = response.json()
            results = []
            for item in data.get("organic", []):
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })
            return results
        except Exception as e:
            return [{"error": str(e)}]

search_service = SearchService()
