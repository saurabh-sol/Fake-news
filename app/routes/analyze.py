from fastapi import APIRouter
from app.schemas import AnalyzeRequest

from Tests.test_sentiment import predict_sentiment
from Modules.keyWordExtractor.keyword_finder import KeywordExtractor
from Modules.newsScraper.google_news import get_news_links
from Modules.similarity.similarity import similarity_pipeline
from Modules.truth_detection.test_detection import get_truth_score
from Modules.Scores.user_credibility import compute_user_credibility
from Modules.Scores.scoring import final_decision, normalize_sentiment

router = APIRouter()

@router.post("/analyze")
def analyze(data: AnalyzeRequest):

    try:
        tweet = data.tweet

        # 🔹 Sentiment
        sentiment_result = predict_sentiment(
            tweet,
            data.likes,
            data.retweets,
            data.comments,
            data.verified
        )

        # Convert sentiment label to score
        sentiment_score = normalize_sentiment(sentiment_result.get("label", "Neutral"))

        # 🔹 Keywords
        extractor = KeywordExtractor()
        keywords = extractor.extract_keywords(tweet)

        # 🔹 News
        news = get_news_links(keywords, data.time_range)

        # Handle case with no news
        if not news:
            news = [{"title": tweet, "link": ""}]

        # 🔹 Similarity
        sim_result = similarity_pipeline(tweet, news)

        # 🔹 Truth Detection
        combined_text = tweet + " " + " ".join(
            [n["title"] for n in sim_result["top_news"]]
        )

        truth_score, _ = get_truth_score(combined_text)

        # 🔹 User Credibility
        credibility = compute_user_credibility(
            data.likes,
            data.retweets,
            data.comments,
            data.verified
        )

        # 🔹 Final Score
        final = final_decision(
            sentiment_score,
            sim_result["similarity_score"],
            truth_score,
            credibility
        )

        return {
            "keywords": keywords,
            "sentiment": sentiment_result,
            "similarity": sim_result["similarity_score"],
            "truth": truth_score,
            "credibility": credibility,
            "final_score": final["final_score"],
            "verdict": final["label"]
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "An error occurred during analysis"
        }