import requests
from bs4 import BeautifulSoup
import logging
import time
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging
logging.basicConfig(level=logging.WARNING)

def extract_article(url, timeout=10):
    """
    Extract article content from a URL with multiple fallback strategies.
    """
    if not url:
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # Try to get the page content
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, timeout=timeout, allow_redirects=True, verify=False)
        response.raise_for_status()
        
        # Decode content
        if response.encoding and response.encoding.lower() == 'utf-8':
            content = response.text
        else:
            response.encoding = 'utf-8'
            content = response.text

        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()

        # Try to extract article title
        title = None
        for tag in soup.find_all(['h1', 'h2']):
            if tag.get_text(strip=True):
                title = tag.get_text(strip=True)
                break

        # Extract paragraphs
        paragraphs = soup.find_all('p')
        
        text_parts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                text_parts.append(text)
        
        text = '\n'.join(text_parts)
        
        # If we got meaningful content, return it
        if text and len(text) > 50:
            return {
                "text": text,
                "authors": [],
                "publish_date": "Unknown"
            }
        
        # Fallback: try to get any text from the body
        if soup.body:
            body_text = soup.body.get_text(separator='\n', strip=True)
            if body_text and len(body_text) > 100:
                # Clean up excessive whitespace
                lines = [line.strip() for line in body_text.split('\n') if line.strip()]
                clean_text = '\n'.join(lines[:50])  # Limit to 50 lines
                if len(clean_text) > 50:
                    return {
                        "text": clean_text,
                        "authors": [],
                        "publish_date": "Unknown"
                    }

    except requests.exceptions.RequestException as e:
        logging.debug(f"Request failed for {url}: {e}")
    except Exception as e:
        logging.debug(f"Failed to extract article from {url}: {e}")

    return None