"""
Filename: llm_filter.py
Description: LLM-based filtering for high-quality AI news articles
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("LLM_API")
if not api_key:
    raise ValueError("LLM_API key not found in environment variables")

# Initialize LLM (NVIDIA endpoint)
llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
    model="abacusai/dracarys-llama-3.1-70b-instruct",
    temperature=0
)


def pre_filter(article):
    """
    Removes obvious low-value or irrelevant articles before LLM.
    """
    title = article["title"].lower()

    blacklist = [
        "show hn",
        "ask hn",
        "course",
        "tutorial",
        "how to",
        "discussion"
    ]

    return not any(word in title for word in blacklist)


def is_ai_relevant_llm(article):
    """
    Classifies a single article as high-quality AI-related or not.
    """

    prompt = f"""
        You are a strict AI news classifier.

        Decide if this article is HIGH-QUALITY AI news.

        INCLUDE ONLY IF:
        - AI is the MAIN focus
        - New AI models, research, or major product launches
        - Significant AI startup activity

        EXCLUDE:
        - Tutorials, courses, discussions
        - Low-value or vague AI mentions

        Return ONLY: YES or NO

        Title: {article['title']}
        Summary: {article['summary']}
        """
        # - Politics with minor AI mention
        # - General tech/business news

    try:
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ]).content.strip().upper()

        return response.startswith("YES")

    except Exception as e:
        print("Error in single LLM filter:", e)
        return False


def filter_ai_news_llm(articles):
    """
    Filters articles using per-article LLM calls (slower, for debugging).
    """

    filtered = []

    for article in articles:
        if pre_filter(article) and is_ai_relevant_llm(article):
            filtered.append(article)

    return filtered


def filter_ai_news_llm_batch(articles):
    """
    Filters articles using a single batch LLM call (recommended).
    """

    if not articles:
        return []

    # Apply pre-filter first
    articles = [a for a in articles if pre_filter(a)]

    # Limit size for stability
    MAX_ARTICLES = 10
    articles = articles[:MAX_ARTICLES]

    # Format articles
    formatted = "\n\n".join(
        [f"{i}. {a['title']}\n{a['summary']}" for i, a in enumerate(articles)]
    )

    prompt = f"""
        You are a strict AI news classifier.

        Keep ONLY high-quality AI news.

        INCLUDE:
        - AI models, LLMs, research
        - Major AI product launches
        - Important AI startups/funding

        EXCLUDE:
        - Tutorials, courses, "Show HN", discussions
        - Low-value or vague content

        STRICT RULES:
        - Output ONLY: index: YES or NO
        - No explanations
        - Be conservative (prefer NO)

        Example:
        0: YES
        1: NO

        Articles:
        {formatted}
        """
        # - Politics with minor AI mention
        # - General business/tech news

    try:
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ]).content

        results = []

        for line in response.splitlines():
            if ":" in line:
                try:
                    idx, label = line.split(":", 1)
                    idx = idx.strip()
                    label = label.strip().upper()

                    if idx.isdigit():
                        index = int(idx)

                        if index < len(articles):
                            if label.startswith("YES"):
                                results.append(articles[index])

                except:
                    continue

        return results

    except Exception as e:
        print("Error in batch LLM filter:", e)
        return []