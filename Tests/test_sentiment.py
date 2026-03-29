import joblib
import re
import os

# Model variables (lazy loaded)
model = None
vectorizer = None

def _load_models():
    global model, vectorizer
    if model is None:
        # Try multiple path strategies
        paths_to_try = [
            "Models/sentiment_model.joblib",
            os.path.join(os.getcwd(), "Models", "sentiment_model.joblib"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Models", "sentiment_model.joblib")
        ]
        
        for path in paths_to_try:
            try:
                model = joblib.load(path)
                print(f"Loaded sentiment model from: {path}")
                break
            except FileNotFoundError:
                continue
        
        if model is None:
            raise FileNotFoundError("Could not find sentiment_model.joblib")
    
    if vectorizer is None:
        paths_to_try = [
            "Models/tfidf_vectorizer.joblib",
            os.path.join(os.getcwd(), "Models", "tfidf_vectorizer.joblib"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Models", "tfidf_vectorizer.joblib")
        ]
        
        for path in paths_to_try:
            try:
                vectorizer = joblib.load(path)
                print(f"Loaded vectorizer from: {path}")
                break
            except FileNotFoundError:
                continue
        
        if vectorizer is None:
            raise FileNotFoundError("Could not find tfidf_vectorizer.joblib")

# Simple preprocessing (must match training)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# Label mapping (change if needed)
labels = {
    0: "Negative",
    1: "Neutral",
    2: "Positive",
    "negative": "Negative",
    "neutral": "Neutral",
    "positive": "Positive"
}

# Prediction function
def predict_sentiment(text, likes=0, retweets=0, comments=0, verified=False):
    """Predict sentiment from text (engagement metrics ignored for now)"""
    _load_models()
    
    clean_text = preprocess_text(text)
    text_tfidf = vectorizer.transform([clean_text])

    prediction = model.predict(text_tfidf)[0]
    probabilities = model.predict_proba(text_tfidf)[0]

    confidence = max(probabilities)
    
    # Handle both string and integer predictions
    predicted_label = labels.get(prediction, labels.get(str(prediction).lower(), "Unknown"))

    return {
        "label": predicted_label,
        "score": float(confidence),
        "confidence": float(confidence)
    }


# User input function (can be imported)
def get_user_input():
    """Get user input for sentiment analysis"""
    user_input = input("Enter financial text: ")
    return user_input


# Main program function
def main():
    print("\n📊 Financial Sentiment Analysis (Joblib Model)")
   
    
    user_input = get_user_input()
    sentiment, confidence = predict_sentiment(user_input)
    
    print(f"\n🔹 Sentiment: {sentiment}")
    print(f"🔹 Confidence: {confidence:.2f}\n")


# Run main program if this file is executed directly
if __name__ == "__main__":
    main()