def normalize_sentiment(sentiment_label):
    if sentiment_label == "Positive":
        return 1.0
    elif sentiment_label == "Neutral":
        return 0.5
    else:
        return 0.0

def calculate_final_score(sentiment_score, similarity, truth, credibility):

    # Updated weights
    w1 = 0.15   # sentiment
    w2 = 0.25   # similarity
    w3 = 0.4    # truth
    w4 = 0.2    # credibility

    final_score = (
        w1 * sentiment_score +
        w2 * similarity +
        w3 * truth +
        w4 * credibility
    )

    return round(final_score, 3)

def final_decision(sentiment_score, similarity, truth, credibility):
    """Make final decision with verdict based on score"""
    score = calculate_final_score(sentiment_score, similarity, truth, credibility)
    
    if score >= 0.7:
        verdict = "Likely TRUE"
    elif score >= 0.4:
        verdict = "UNCERTAIN"
    else:
        verdict = "Likely FALSE"
    
    return {
        "final_score": score,
        "label": verdict
    }