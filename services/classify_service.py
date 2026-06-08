from transformers import pipeline
from typing import Dict, List

class ClassifyService:
    """Article classification service"""
    
    def __init__(self):
        self.topics = [
            "Technology", "Science", "Business", "Finance",
            "Health", "Medicine", "Sports", "Politics",
            "Entertainment", "Education", "Environment", "World News"
        ]
        print("Loading classification service...")
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        print("Classification service loaded!")
    
    def classify(self, text: str) -> Dict:
        """Classify text into topic"""
        if not text or len(text) < 50:
            return {"topic": "General", "confidence": 0.0}
        
        text = text[:500]
        
        try:
            result = self.classifier(text, candidate_labels=self.topics, multi_class=False)
            return {
                "topic": result["labels"][0],
                "confidence": round(result["scores"][0], 3)
            }
        except Exception as e:
            return {"topic": "General", "confidence": 0.0, "error": str(e)}
    
    def classify_batch(self, texts: List[str]) -> List[Dict]:
        """Classify multiple texts"""
        return [self.classify(text) for text in texts]

classify_service = ClassifyService()