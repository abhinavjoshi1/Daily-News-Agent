from tools.news_fetcher import fetch_news
from agents.llm_filter import filter_ai_news_llm_batch

news = fetch_news(limit=5)
filtered = filter_ai_news_llm_batch(news)

print("\nFiltered:\n")

for i, article in enumerate(filtered, 1):
    print(f"{i}. {article['title']}")