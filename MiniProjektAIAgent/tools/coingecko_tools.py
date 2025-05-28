from autogen_core.tools import FunctionTool
from typing import Dict, Any, List, Literal
import requests
import os
from datetime import datetime

def get_coin_data(coin_id: str, currency: str = "usd") -> Dict[str, Any]:
    """
    Fetch current market data for a given cryptocurrency using CoinGecko's API.

    Args:
        coin_id (str): The CoinGecko coin ID (e.g., 'bitcoin', 'ethereum').
        currency (str): The fiat currency to convert against (e.g., 'usd').

    Returns:
        dict: Contains price, market cap, 24h volume, etc.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "ids": coin_id.lower()
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        return {"error": f"No data found for '{coin_id}'"}

    coin = data[0]
    return {
        "coin": coin["id"],
        "symbol": coin["symbol"],
        "name": coin["name"],
        "price": coin["current_price"],
        "market_cap": coin["market_cap"],
        "volume_24h": coin["total_volume"],
            "last_updated": coin["last_updated"]
        }

get_coin_data_tool = FunctionTool(
        func=get_coin_data,
        description="Get real-time market data for a cryptocurrency from CoinGecko.",
    )
#def fetch_market_chart(coin_id: str, vs_currency: str = "usd", days: Literal[1, 7, 14, 30, 90, 180, 365, 'max'] = 30) -> Dict:

def fetch_market_chart(coin_id: str, vs_currency: str = "usd", days: int = 30) -> Dict:
    """
    Fetch historical market chart data (price, market cap, volume) over a given period.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
    "vs_currency": vs_currency,
    "days": days
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    def format_entries(entries):
        return [
            {
                "timestamp": datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "value": val
            } for ts, val in entries
        ]

    return {
        "prices": format_entries(data.get("prices", [])),
        "market_caps": format_entries(data.get("market_caps", [])),
        "total_volumes": format_entries(data.get("total_volumes", []))
    }

get_market_chart_tool = FunctionTool(
        func=fetch_market_chart,
        description="Fetch historical market chart data (price, market cap, volume) over a given period for a cryptocurrency from CoinGecko.",
    )