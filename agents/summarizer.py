"""
Filename: summarizer.py
Description: LLM-based summarization of filtered AI news
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("LLM_API")
if not api_key:
    raise ValueError("LLM_API key not found")

llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
    model="abacusai/dracarys-llama-3.1-70b-instruct",
    temperature=0.3
)


def summarize_news(articles):
    """
    Takes filtered articles and returns a structured summary.
    """

    if not articles:
        return "No significant AI news today."

    # Limit input size
    articles = articles[:8]

    formatted = "\n\n".join(
        [f"{i+1}. {a['title']}\n{a['summary']}" for i, a in enumerate(articles)]
    )

    prompt = f"""
        You are an AI news analyst.

        ONLY use the articles provided below.
        DO NOT add any external information.
        DO NOT hallucinate or invent news.

        For each article:
        - Use the EXACT title
        - Write 1–2 bullet points based ONLY on the given summary

        STRICT RULES:
        - No extra articles
        - No assumptions
        - No external knowledge
        - Only summarize what is given

        Format:

        AI News — Daily Brief

        1. Title
        - Point
        - Point

        If information is insufficient, keep the summary short.

        Articles:
        {formatted}
        """

    try:
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ]).content

        return response.strip()

    except Exception as e:
        print("Error in summarization:", e)
        return "Error generating summary."