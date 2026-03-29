import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google_news import get_news_links
from article_parser import extract_article


def get_full_news(keywords, time_range="1w", max_results=10):
    """
    Fetch full news articles based on keywords
    
    Args:
        keywords: List of keywords to search for
        time_range: Time range for news ('1d', '1w', '1m')
        max_results: Maximum number of articles to fetch
    
    Returns:
        List of dictionaries with 'title', 'content', and 'link'
    """
    
    if not keywords:
        return []

    news_links = get_news_links(keywords, time_range, max_results)

    if not news_links:
        return []

    full_news = []

    for news in news_links:
        try:
            article_data = extract_article(news["link"])

            if article_data and article_data["text"]:
                full_news.append({
                    "title": news["title"],
                    "content": article_data["text"],
                    "link": news["link"],
                    "authors": article_data.get("authors", []),
                    "publish_date": article_data.get("publish_date", "Unknown")
                })
            else:
                # Keep article with title as fallback content
                full_news.append({
                    "title": news["title"],
                    "content": news["title"],
                    "link": news["link"],
                    "authors": [],
                    "publish_date": "Unknown"
                })
        except Exception as e:
            # Still add article with title on error
            full_news.append({
                "title": news["title"],
                "content": news["title"],
                "link": news["link"],
                "authors": [],
                "publish_date": "Unknown"
            })

    return full_news