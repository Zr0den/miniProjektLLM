import asyncio
from tools.coingecko_tools import get_coin_data_tool, get_market_chart_tool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

async def main():
    model_client = OllamaChatCompletionClient(model="mistral")
    researcher = AssistantAgent(
        name="SearchAgent",
        model_client=model_client,
        tools=[get_market_chart_tool],
        system_message = """
        You are an expert cryptocurrency search, data and evaluation agent.
        Use tools to get accurate real-time cryptocurrency stats.
        Use tools to fetch the market chart data for the given coin within the last month, and determine if the coin is trending up or down.
        Your goal is to return clear and helpful summaries of a coin's 30-day performance.
        Use the following output format when responding with market chart data:
        ______________________________________
        {coin_name} Market Data — Last 30 Days

        Coin ID: {coin_id}

        Currency: {vs_currency}

        Time Span: 30 days

        Price Summary (USD)

        Start Price: ${start_price}

        End Price: ${end_price}

        Highest Price: ${max_price}

        Lowest Price: ${min_price}
    
        Price Trend: {trend_direction} 📈 or 📉

        Market Cap Summary (USD)

        Start Market Cap: ${start_market_cap}

        End Market Cap: ${end_market_cap}

        Max Market Cap: ${max_market_cap}

        Total Volume Summary (USD)

        Start Volume: ${start_volume}

        End Volume: ${end_volume}

        Max Volume: ${max_volume}
        ______________________________________
        """,
        )

    while True:
        user_input = input("Enter your task (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        stream = researcher.run_stream(task=user_input)
        await Console(stream)

asyncio.run(main())