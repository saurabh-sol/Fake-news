import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Modules.keyWordExtractor.keyword_finder import KeywordExtractor
from Modules.newsScraper.google_news import get_news_links

try:
    tweet = input("Enter tweet: ").strip()
    if not tweet:
        print("❌ Please enter a valid tweet")
        exit()
    
    time_range = input("Enter time (1d/1w/1m): ").strip()
    if time_range not in ['1d', '1w', '1m']:
        time_range = '1w'
        print(f"⚠️  Invalid time range, using default: 1w")

    # Step 1: Extract Keywords
    print("\n📊 Extracting keywords from tweet...")
    extractor = KeywordExtractor()
    keywords = extractor.extract_keywords(tweet)

    if not keywords:
        print("❌ No keywords could be extracted from the tweet")
        exit()

    print(f"\n✓ Keywords extracted: {keywords}")

    # Step 2: Fetch news titles
    print("\n📰 Fetching news titles...")
    news_titles = get_news_links(keywords, time_range, max_results=10)

    # Step 3: Display results
    if not news_titles:
        print("❌ No news titles found for the extracted keywords")
        exit()

    # Extract only the titles into a list
    titles_list = [article['title'] for article in news_titles]

    print(f"\n{'='*70}")
    print(f"🔑 Keywords: {keywords}")
    print(f"📰 Found {len(titles_list)} news titles.")
    print(f"{'='*70}")

    # Print the list of titles
    print("\n📄 List of titles for similarity check:\n")
    for i, title in enumerate(titles_list, 1):
        print(f"{i}. {title}")

except KeyboardInterrupt:
    print("\n\n⚠️  Process interrupted by user")
except Exception as e:
    print(f"\n❌ An error occurred: {str(e)}")