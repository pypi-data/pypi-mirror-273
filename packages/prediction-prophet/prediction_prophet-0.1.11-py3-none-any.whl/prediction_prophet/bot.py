import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from typing import cast
import discord
from discord import app_commands
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

from prediction_prophet.benchmark.agents import _make_prediction
from prediction_prophet.functions.create_embeddings_from_results import (
    create_embeddings_from_results,
)
from prediction_prophet.functions.generate_subqueries import generate_subqueries
from prediction_prophet.functions.is_predictable_and_binary import (
    is_predictable_and_binary,
)
from prediction_prophet.functions.prepare_report import prepare_report
from prediction_prophet.functions.rerank_subqueries import rerank_subqueries
from prediction_prophet.functions.scrape_results import scrape_results
from prediction_prophet.functions.search import search
from prediction_market_agent_tooling.tools.utils import secret_str_from_env
from prediction_market_agent_tooling.benchmark.utils import OutcomePrediction

load_dotenv()


model: str = "gpt-4-0125-preview"
initial_subqueries_limit: int = 20
subqueries_limit: int = 4
scrape_content_split_chunk_size: int = 800
scrape_content_split_chunk_overlap: int = 225
top_k_per_query: int = 8

tavily_api_key = secret_str_from_env("TAVILY_API_KEY")
discord_bot_token = secret_str_from_env("DISCORD_BOT_TOKEN")

if tavily_api_key == None:
    raise Exception("No Tavily API Key provided")

if discord_bot_token == None:
    raise Exception("No discord bot token provided")

executor = ThreadPoolExecutor()


async def handle_prediction(
    goal: str, message: discord.Message, thread: discord.Thread, message_prophet: str
):
    loop = asyncio.get_running_loop()
    queries = await loop.run_in_executor(
        executor, generate_subqueries, goal, initial_subqueries_limit, model
    )
    message_prophet = message_prophet + "\n### Reranking subqueries..."
    await message.edit(content=message_prophet)
    queries = (
        (await loop.run_in_executor(executor, rerank_subqueries, queries, goal, model))[
            :subqueries_limit
        ]
        if initial_subqueries_limit > subqueries_limit
        else queries
    )

    message_prophet = message_prophet + "\n### Searching the web..."
    await message.edit(content=message_prophet)
    search_results_with_queries = await loop.run_in_executor(
        executor,
        search,
        queries,
        lambda result: not result.url.startswith("https://www.youtube"),
        tavily_api_key,
    )

    if not search_results_with_queries:
        message_prophet = message_prophet = "\n### No search results found for goal"
        await message.edit(content=message_prophet)
        return

    message_prophet = message_prophet + "\n### Scraping web results..."
    await message.edit(content=message_prophet)
    scrape_args = [result for (_, result) in search_results_with_queries]

    scraped = await loop.run_in_executor(executor, scrape_results, scrape_args)
    scraped = [result for result in scraped if result.content != ""]

    message_prophet = message_prophet + "\n### Performing similarity searches..."
    await message.edit(content=message_prophet)

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", "  "],
        chunk_size=scrape_content_split_chunk_size,
        chunk_overlap=scrape_content_split_chunk_overlap,
    )
    collection = create_embeddings_from_results(scraped, text_splitter)

    vector_result_texts: list[str] = []
    for query in queries:
        top_k_per_query_results = collection.similarity_search(query, k=top_k_per_query)
        vector_result_texts += [
            result.page_content
            for result in top_k_per_query_results
            if result.page_content not in vector_result_texts
        ]

    message_prophet = message_prophet + "\n### Preparing report..."
    await message.edit(content=message_prophet)

    report = await loop.run_in_executor(executor, prepare_report, goal, vector_result_texts, model)

    message_prophet = message_prophet + "\n### Making prediction..."
    await message.edit(content=message_prophet)

    prediction = await loop.run_in_executor(executor, _make_prediction, goal, report, model, 0.0)

    if prediction.outcome_prediction == None:
        await message.edit(content="\n### The agent failed to generate a prediction")
        return

    outcome_prediction = cast(OutcomePrediction, prediction.outcome_prediction)
    await message.edit(
        content=f"With **{outcome_prediction.confidence * 100}% confidence**, I'd say this outcome has a **{outcome_prediction.p_yes * 100}% probability** of happening"
    )
    report_file_name = f"report-{str(thread.id)}.md"
    with open(report_file_name, "w") as f:
        f.write(report)
    await thread.send(file=discord.File(report_file_name, filename="report.md"))
    os.remove(report_file_name)


POLYWRAP_SERVER = discord.Object(id=1232966117480206356)


class PolywrapBot(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=POLYWRAP_SERVER)
        await self.tree.sync(guild=POLYWRAP_SERVER)


intents = discord.Intents(messages=True)
intents.message_content = True
bot = PolywrapBot(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.tree.command(
    name="predict", description="Ask any yes-or-no question about a future outcome"
)
@app_commands.describe(question="Question about a future outcome")
async def predict(interaction: discord.Interaction, question: str):
    await interaction.response.defer(ephemeral=True)
    (is_predictable, reasoning) = is_predictable_and_binary(question)
    if not is_predictable:
        await interaction.followup.send(
            content=f"The agent thinks this question is not predictable: \n{reasoning}"
        )
        return

    follow_up_message = await interaction.followup.send(
        content="Evaluating question..."
    )
    await interaction.followup.delete_message(follow_up_message.id)
    prediction_message = await interaction.channel.send(content=question)
    thread = await prediction_message.create_thread(
        name="Assessing the likelihood of question happening"
    )
    message_prophet = "# Evaluating question..."
    message = await thread.send(message_prophet)
    await handle_prediction(question, message, thread, message_prophet)


bot.run(discord_bot_token.get_secret_value())
