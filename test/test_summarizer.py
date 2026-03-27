from tools.news_fetcher import fetch_news
from agents.llm_filter import filter_ai_news_llm_batch
from agents.summarizer import summarize_news

news = fetch_news()
filtered = filter_ai_news_llm_batch(news)

summary = summarize_news(filtered)

print("\n=== FINAL SUMMARY ===\n")
print(summary)