import joblib
import re
import nltk
import os
# nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)

# Model variables (lazy loaded)
model = None
vectorizer_truth = None

def _load_truth_model():
    global model, vectorizer_truth
    if model is None:
        paths_to_try = [
            "Models/truth_model.joblib",
            os.path.join(os.getcwd(), "Models", "truth_model.joblib"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "Models", "truth_model.joblib")
        ]
        
        for path in paths_to_try:
            try:
                data = joblib.load(path)
                model = data["model"]
                vectorizer_truth = data["vectorizer"]
                print(f"Loaded truth model from: {path}")
                return
            except (FileNotFoundError, KeyError):
                continue
        
        raise FileNotFoundError("Could not find truth_model.joblib")


def get_truth_score(text):
    _load_truth_model()
    
    clean = clean_text(text)

    vec = vectorizer_truth.transform([clean])

    probabilities = model.predict_proba(vec)[0]
    
    # Truth score is the probability of class 1 (True)
    truth_score = round(probabilities[1], 3)
    
    # Confidence is the maximum probability (how confident the model is)
    confidence = round(max(probabilities), 3)

    return truth_score, confidence

print("Final Score ", get_truth_score("Tesla is likely to hit 1 billion valuation"))