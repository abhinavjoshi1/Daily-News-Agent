"""
Filename : 
Description :
"""

# ------------- Imports -------------
import feedparser


AI_RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://hnrss.org/newest?q=AI"
]

def fetch_news(limit = 10) :
    """
    
    """

    articles = []

    for feed_url in AI_RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit]:
            article = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")
            }

            articles.append(article)

    return articles