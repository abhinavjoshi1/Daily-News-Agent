"""
Filename : 
Description :
"""

# ------------- Imports -------------
import feedparser


AI_RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://hnrss.org/newest?q=AI",

    "https://openai.com/blog/rss.xml",
    "https://openai.com/news/rss.xml",
    "https://deepmind.google/blog/rss.xml",
    "https://research.google/blog/rss/",
    "https://www.anthropic.com/rss.xml",
    "https://ai.meta.com/blog/rss/",
    "https://mistral.ai/news/rss",


    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://www.theguardian.com/technology/artificialintelligenceai/rss",
    "https://www.wired.com/feed/tag/ai/latest/rss",
    "https://www.404media.co/rss",

    "https://bair.berkeley.edu/blog/feed.xml",
    "https://news.mit.edu/topic/artificial-intelligence2/rss",
    "https://magazine.sebastianraschka.com/feed",
    "https://paperswithcode.com/latest",
    "https://www.lesswrong.com/feed.xml",

    
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