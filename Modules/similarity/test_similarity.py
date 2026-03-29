import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Modules.keyWordExtractor.keyword_finder import KeywordExtractor
from Modules.newsScraper.google_news import get_news_links
from Modules.similarity.similarity import similarity_pipeline

try:
    # Input
    tweet = input("Enter tweet: ").strip()
    if not tweet:
        print("❌ Please enter a valid tweet")
        exit()
        
    time_range = input("Enter time (1d/1w/1m): ").strip()
    if time_range not in ['1d', '1w', '1m']:
        time_range = '1w'
        print(f"⚠️  Invalid time range, using default: 1w")

    # Step 1: Extract keywords
    print("\n📊 Extracting keywords...")
    extractor = KeywordExtractor()
    keywords = extractor.extract_keywords(tweet)
    print(f"✓ Keywords extracted: {keywords}")

    # Step 2: Fetch news titles
    print("\n📰 Fetching news titles...")
    news_articles = get_news_links(keywords, time_range, max_results=10)
    
    if not news_articles:
        print("❌ No news titles found for the extracted keywords")
        exit()
        
    print(f"✓ Found {len(news_articles)} news titles.")

    # Step 3: Run similarity pipeline
    print("\n🔄 Calculating similarity scores...")
    result = similarity_pipeline(tweet, news_articles)
    
    # Calculate the average of the top 3 scores
    top_3_scores = [n['score'] for n in result["top_news"][:3]]
    final_score = sum(top_3_scores) / len(top_3_scores) if top_3_scores else 0.0
    
    print("✓ Similarity calculation complete.")

    # Output
    print(f"\n{'='*70}")
    print(f"🔑 Keywords: {keywords}")
    print(f"🎯 Final Score (Avg of Top 3): {final_score:.3f}")
    print(f"{'='*70}")

    print("\n🔥 Top 3 Similar News Titles:\n")
    for i, n in enumerate(result["top_news"][:3], 1):
        print(f"{i}. Score: {n['score']:.3f}")
        print(f"   Title: {n['title']}")
        print(f"   {'-'*70}")

except KeyboardInterrupt:
    print("\n\n⚠️  Process interrupted by user")
except Exception as e:
    print(f"\n❌ An error occurred: {str(e)}")