from tools.news_fetcher import fetch_news

news = fetch_news()

for i, article in enumerate(news[:5], 1):
    print(f"{i}. {article['title']}")
    print(article['link'])
    print()