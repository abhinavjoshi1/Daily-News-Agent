"""
Filename: main.py
Description: Entry point for Daily AI News Agent
"""

from tools.news_fetcher import fetch_news
from agents.llm_filter import filter_ai_news_llm_batch
from agents.summarizer import summarize_news
from tools.email_sender import send_email


def run_pipeline():
    print("Fetching news...")
    news = fetch_news()

    print(f"Fetched {len(news)} articles")

    print("Filtering AI news...")
    filtered = filter_ai_news_llm_batch(news)

    print(f"Filtered down to {len(filtered)} articles")

    print("Summarizing...")
    summary = summarize_news(filtered)

    print("Sending email...")
    send_email(summary)

    print("Done.")


if __name__ == "__main__":
    run_pipeline()