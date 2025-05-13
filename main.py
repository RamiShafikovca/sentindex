# Stock News Sentiment Analysis - Project Skeleton

import requests
import pandas as pd
import numpy as np
from datetime import datetime

# --- Configuration ---git 
TICKERS = ["AAPL", "TSLA", "MSFT" , "COIN", "AMZN"]
NEWS_API_KEY = "your_newsapi_key"
LLM_API_KEY = "your_llm_api_key"

# --- Functions ---

def fetch_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    records = []
    for article in articles:
        records.append({
            "ticker": ticker,
            "title": article["title"],
            "summary": article["description"],
            "published_at": article["publishedAt"],
            "source_url": article["url"]
        })
    return records

def analyze_sentiment_llm(title, summary):
    prompt = f"""
    Analyze the sentiment of this news headline and summary. Label as Positive, Negative, or Neutral.

    Title: {title}
    Summary: {summary}
    """
    headers = {"Authorization": f"Bearer {LLM_API_KEY}"}
    # Replace with actual LLM API call
    # Example placeholder result
    return {
        "sentiment_label": "Neutral",
        "llm_commentary": "This news has a balanced tone without strong positive or negative implications."
    }

# --- Main Execution ---
all_news = []
for ticker in TICKERS:
    news = fetch_news(ticker)
    for item in news:
        sentiment_result = analyze_sentiment_llm(item["title"], item["summary"])
        item.update(sentiment_result)
    all_news.extend(news)

# Convert to DataFrame
df = pd.DataFrame(all_news)

# Sentiment Scoring
def sentiment_score(label):
    return {"Positive": 1, "Neutral": 0, "Negative": -1}.get(label, 0)

df["sentiment_score"] = df["sentiment_label"].apply(sentiment_score)

# Aggregate by ticker
summary = df.groupby("ticker").agg(
    avg_sentiment_score=("sentiment_score", "mean"),
    latest_sentiment=("sentiment_label", lambda x: x.iloc[-1]),
    news_count=("title", "count")
).reset_index()

# Save results
df.to_csv("detailed_news_sentiment.csv", index=False)
summary.to_csv("summary_sentiment.csv", index=False)

print(summary)
