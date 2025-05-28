import asyncio
from tools.fetch_news_redacted import fetch_news_by_top_headlines, fetch_news_by_topic_and_date_range
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
        system_message=("""
    You are SearchAgent, a precise assistant tasked with retrieving up-to-date news articles from NewsAPI.org.
    You must read your task to choose the appropriate tool for fetching news articles.
                        
    You have access to 2 tools.

    You can not request articles from dates earlier than 2025-04-27
    You must use one of these tools to complete your task. Use the results from the tool to build your response.
    If no results are returned from a tool, respond: No articles were found for the given criteria. You are not allowed to fabricate articles if the tool returns an empty list.
                                     
    When returning results:
    - Start your response with the name of the used tool.
    - Format output in clean, readable markdown.
    - Group articles under a clear heading, e.g. "Top News for May 27, 2025" or "AI News: May 20–27, 2025".
    - List each article as a bullet point with the title as a hyperlink and Include the publication date.
    
    Output Format Template:
    
    News Brief: {Contextual Title}
    Retrieved Articles
    - [{Article Title}]({url})
      Published: {PublishedAt}
      {Short Description}
    
    - [{Article Title}]({url})
      Published: {PublishedAt}
      {Short Description}

    """),
        tools=[fetch_news_by_top_headlines, fetch_news_by_topic_and_date_range],
    )

    fact_checker = AssistantAgent(
    name="FactCheckerAgent",
    model_client=model_client,
    system_message=("""
    You are FactCheckerAgent, an expert in factual verification and date validation.
    Your task is to verify the factual accuracy and temporal relevance of each article provided by SearchAgent.

    Your responsibilities:
    1. Cross-check article content (title, description) for factual consistency based on common knowledge and context.
    2. If the user requested date specific aritcles, validate that the publication dates of all articles match the user’s original request (e.g., "today", "past 7 days", etc.).
    3. Flag any articles that appear misleading, incorrect, or unrelated to the time period specified.
    4. Validate that the articles are legitimate (for example, not from example-news.com or similar placeholder sites).

    Output Format Template:

    Fact Check Report
    {Article Title}
    - Published: {PublishedAt}
    - Verdict: ✅ Accurate | ❌ Issue Found
    - Notes: {Brief explanation of any issues or confirmations}

    Summary
    All articles are verified and consistent with the user’s request.
    Proceed to summarization.

    OR

    Summary
    One or more articles failed fact-checking.
    Terminate the conversation.

    Notes:
    - Be objective, use caution, and do not hallucinate.
    - If any article fails, do not proceed further. Instead, clearly state that the conversation should terminate.
    - End your response with TERMINATE if issues are found.
    """)
    )

    summarizer = AssistantAgent(
    name="SummarizerAgent",
    model_client=model_client,
    system_message=("""
    You are SummarizerAgent, an expert summarizer. Your role is to create clear and concise summaries from fact-verified news articles.

    Preconditions:
    - Do not begin your task unless the articles have been explicitly approved by FactCheckerAgent.
    - Only work on content that has been validated as both factually accurate and date-aligned.
    - If you detect any sign that the articles were not fact-checked or failed the fact-check, do not respond. Wait or TERMINATE.

    Input:
    - A list of articles in markdown format, each with a title, URL, publication date, and description.

    Your responsibilities:
    1. Summarize each article clearly in 5–6 informative sentences.
    2. Capture the essence of the article without adding or omitting core information.
    3. Provide a brief overall summary of the news trend or theme.

    Output Format:

    Article Summaries
    [Article Title](URL)  
    {Summary of article}

    Overall Summary
    {High-level trend or common theme in a few sentences}  

    Notes:
    - Maintain the structure and readability of the markdown format.
    - Keep summaries focused, objective, and free of speculation.
    """)
    )

    team = RoundRobinGroupChat([researcher, fact_checker, summarizer],
    termination_condition=TextMentionTermination("TERMINATE"),
    max_turns=3
    )

    while True:
        user_input = input("Enter your task (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        stream = team.run_stream(task=user_input)
        await Console(stream)

asyncio.run(main())