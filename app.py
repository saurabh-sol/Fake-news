import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from Tests.test_sentiment import predict_sentiment
from Modules.keyWordExtractor.keyword_finder import KeywordExtractor
from Modules.newsScraper.scraper import get_full_news
from Modules.similarity.similarity import similarity_pipeline
from Modules.truth_detection.test_detection import get_truth_score
from Modules.Scores.scoring import calculate_final_score, normalize_sentiment
from Modules.Scores.user_credibility import compute_user_credibility

def main():
    print("Welcome to the Tweet Detector!")
    tweet = input("Enter the tweet text: ")
    likes = int(input("Enter the number of likes: "))
    retweets = int(input("Enter the number of retweets: "))
    comments = int(input("Enter the number of comments: "))
    is_verified = input("Is the user verified? (yes/no): ").lower() == 'yes'
    
    # Ask for timeframe for news scraping
    print("\nSelect timeframe for news scraping:")
    print("1. Last 24 hours (1d)")
    print("2. Last 7 days (1w) - Default")
    print("3. Last month (1m)")
    timeframe_choice = input("Enter your choice (1-3) or press Enter for default: ").strip()
    
    timeframe_map = {
        "1": "1d",
        "2": "1w",
        "3": "1m"
    }
    time_range = timeframe_map.get(timeframe_choice, "1w")

    # 1. Sentiment Analysis
    sentiment_label, sentiment_confidence = predict_sentiment(tweet)
    sentiment_score = normalize_sentiment(sentiment_label)
    print(f"\n📊 Sentiment: {sentiment_label} (Confidence: {sentiment_confidence:.2f})")

    # 2. Keyword Extraction
    keyword_extractor = KeywordExtractor()
    keywords = keyword_extractor.extract_keywords(tweet)
    print(f"🔑 Keywords extracted: {len(keywords)} found")

    # 3. News Scraping
    print(f"\n📰 Searching for news articles ({time_range})...")
    news_articles = get_full_news(keywords, time_range=time_range, max_results=10)
    if not news_articles:
        print("⚠️  Could not find any relevant news articles.")
        similarity_score = 0.0
    else:
        print(f"✓ Found {len(news_articles)} news articles")
        
        # 4. Similarity Calculation
        similarity_result = similarity_pipeline(tweet, news_articles)
        similarity_score = similarity_result['similarity_score']
        print(f"📈 Similarity Score: {similarity_score}")

    # 5. Truth Detection
    truth_score, truth_confidence = get_truth_score(tweet)
    print(f"🔍 Truth Score: {truth_score} (Confidence: {truth_confidence})")

    # 6. User Credibility
    credibility_score = compute_user_credibility(likes, retweets, comments, is_verified)
    print(f"👤 User Credibility Score: {credibility_score}")

    # 7. Final Score
    final_score = calculate_final_score(sentiment_score, similarity_score, truth_score, credibility_score)
    print(f"\n✨ Final Score: {final_score}")
    if final_score > 0.7:
        print("✅ Likely TRUE")
    elif final_score > 0.4:
        print("⚠️ Uncertain")
    else:
        print("❌ Likely FALSE")

if __name__ == "__main__":
    main()


