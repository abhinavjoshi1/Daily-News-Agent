from tools.news_fetcher import fetch_news
from agents.llm_filter import filter_ai_news_llm_batch

news = fetch_news(limit=10)

print("\n--- RAW NEWS ---\n")
for i, article in enumerate(news, 1):
    print(f"{i}. {article['title']}")

filtered = filter_ai_news_llm_batch(news)

print("\n--- FILTERED NEWS ---\n")
for i, article in enumerate(filtered, 1):
    print(f"{i}. {article['title']}")

print(f"\nTotal: {len(news)} | Filtered: {len(filtered)}")