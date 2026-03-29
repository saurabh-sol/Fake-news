import feedparser
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

def get_news_links(keywords, time_range="1w", max_results=10):
    """
    Fetch news links from Google News RSS feed based on keywords
    
    Args:
        keywords: List of keywords to search for
        time_range: Time range for news ('1d', '1w', '1m')
        max_results: Maximum number of results to return
    
    Returns:
        List of dictionaries with 'title' and 'link' keys
    """
    
    if not keywords:
        return []
    
    # URL encode each keyword and join with +
    encoded_keywords = [quote(kw) for kw in keywords]
    query = "+".join(encoded_keywords)

    time_map = {
        "1d": "1d",
        "1w": "7d",
        "1m": "1m"
    }

    when = time_map.get(time_range, "7d")

    url = f"https://news.google.com/rss/search?q={query}&when={when}"

    try:
        # Fetch the RSS feed with timeout and headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            return []

        news_links = []

        for entry in feed.entries[:max_results]:
            try:
                # Extract link from entry
                link = entry.get('link', '')
                if not link and hasattr(entry, 'links'):
                    for l in entry.links:
                        if l.get('rel') == 'alternate':
                            link = l.get('href', '')
                            break
                
                if link:
                    news_links.append({
                        "title": entry.get('title', 'No Title'),
                        "link": link,
                        "summary": entry.get('summary', '')
                    })
            except Exception as e:
                continue
        
        return news_links
    
    except requests.exceptions.RequestException as e:
        return []
    except Exception as e:
        return []