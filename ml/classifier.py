from transformers import pipeline
from typing import Dict

class Classifier:
    """Article topic classification"""
    
    def __init__(self):
        self.topics = ["Technology", "Science", "Business", "Finance", "Health", "Sports", "Politics", "Entertainment", "Education"]
        print("Loading classifier model...")
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        print("Classifier loaded!")
    
    def classify(self, text: str) -> Dict:
        """Classify article into topic"""
        if not text or len(text) < 50:
            return {"topic": "General", "confidence": 0.0}
        
        text = text[:500]
        
        try:
            result = self.classifier(text, candidate_labels=self.topics, multi_class=False)
            return {"topic": result["labels"][0], "confidence": round(result["scores"][0], 3)}
        except:
            return {"topic": "General", "confidence": 0.0}

classifier = Classifier()