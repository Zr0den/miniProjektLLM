import requests
import os
from typing import List, Dict

def fetch_news_by_topic_and_date_range(topic: str, start_date: str, end_date: str, language: str = "en", page_size: int = 5) -> List[Dict]:
    api_key = os.environ.get("NEWS_API_KEY1")
    url = "https://newsapi.org/v2/everything/"
    params = {
    "q": topic,
    "from": start_date,
    "to": end_date,
    "language": language,
    "sortBy": "popularity",
    "pageSize": page_size,
    "apiKey": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return [
    {
        "author": article["author"],
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "urlToImage": article["urlToImage"],
        "publishedAt": article["publishedAt"]
    }
    for article in data.get("articles", [])
]

def fetch_news_by_top_headlines(country: str) -> List[Dict]:
    #api_key = os.environ.get("NEWS_API_KEY")
    url = "https://newsapi.org/v2/top-headlines/?country={country}&apiKey=b7324b3af90447fca811548ec37a1854"
    #params = {
    #"country": country,
    #"apiKey": api_key
    #}

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return [
    {
        "author": article["author"],
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "urlToImage": article["urlToImage"],
        "publishedAt": article["publishedAt"]
    }
    for article in data.get("articles", [])
]