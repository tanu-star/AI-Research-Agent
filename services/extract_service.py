from newspaper import Article
from typing import Dict
import requests
from bs4 import BeautifulSoup

class ExtractService:
    """Content extraction service"""
    
    def extract(self, url: str) -> Dict:
        try:
            article = Article(url)
            article.download()
            article.parse()
            if article.text and len(article.text) > 100:
                return {
                    "title": article.title,
                    "text": article.text,
                    "date": str(article.publish_date) if article.publish_date else "Unknown",
                    "authors": article.authors
                }
        except:
            pass
        
        # Fallback to BeautifulSoup
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            title = soup.title.string if soup.title else "Unknown"
            text = soup.get_text(separator="\n")
            lines = [line.strip() for line in text.split("\n")]
            text = "\n".join(line for line in lines if line)
            return {"title": title, "text": text[:5000], "date": "Unknown", "authors": []}
        except Exception as e:
            return {"error": str(e)}

extract_service = ExtractService()
