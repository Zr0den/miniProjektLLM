import asyncio
from tools.coingecko_tools import get_coin_data_tool
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
        tools=[get_coin_data_tool],
        system_message=("""
            You are an expert cryptocurrency search, data and evaluation agent. 
            Use tools to get accurate real-time crypto stats. 
            Format it in a clean, readable markdown format.
            
            Output Format Template:
            Coin Data for coin_name (coin_symbol)
            - **Price**: $price
            - **Market Cap**: $market_cap
            - **24h Volume**: $volume_24h
            - **Last Updated**: last_updated
            - **Coin ID**: coin_id
            
        """)
    )

    while True:
        user_input = input("Enter your task (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        stream = researcher.run_stream(task=user_input)
        await Console(stream)

asyncio.run(main())