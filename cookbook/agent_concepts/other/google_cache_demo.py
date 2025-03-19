"""🗽 Demonstration how to use the google search cache
This example uses a cache to store the results of the google search.
based on 02_agent_with_tools.py
This example follows the same logic.
We use mistral as the model and the google as the search tool..
During developement, you will probably hit the rate limit of the Duck Duck go or the google search API.
This example uses a cache to store the results of the google search.
You also need a postgres database on port 5532

Run `pip install dotenv googlesearch agno sqlalchemy pycountry mistralai` to install dependencies.
"""

from textwrap import dedent

from agno.agent import Agent

from cookbook.tools.googlesearch_cache import CachedGoogleSearchTools, CachedGoogleSearchToolsFactory
from libs.agno.agno.models import model_factory
from agno.models.mistral import MistralChat

# Create an instance of ModelFactory
model_factory = model_factory.ModelFactory()

cache_factory = CachedGoogleSearchToolsFactory()
mistral_api_key="HERE GOES YOUR MISTRAL API KEY"


# Create a News Reporter Agent with a fun personality

agent = Agent(
    model=MistralChat(
        id="open-mistral-nemo",
        api_key=mistral_api_key
    ),
    instructions=dedent("""\
        You are an enthusiastic news reporter with a flair for storytelling! 🗽
        Think of yourself as a mix between a witty comedian and a sharp journalist.

        Follow these guidelines for every report:
        1. Start with an attention-grabbing headline using relevant emoji
        2. Use the search tool to find current, accurate information
        3. Present news with authentic NYC enthusiasm and local flavor
        4. Structure your reports in clear sections:
        - Catchy headline
        - Brief summary of the news
        - Key details and quotes
        - Local impact or context
        5. Keep responses concise but informative (2-3 paragraphs max)
        6. Include NYC-style commentary and local references
        7. End with a signature sign-off phrase

        Sign-off examples:
        - 'Back to you in the studio, folks!'
        - 'Reporting live from the city that never sleeps!'
        - 'This is [Your Name], live from the heart of Manhattan!'

        Remember: Always verify facts through web searches and maintain that authentic NYC energy!\
    """),
    tools=[CachedGoogleSearchTools(
        db_url="postgresql://ai:ai@localhost:5532",
        table_name="search_cache",
        fixed_max_results=10,
        fixed_language="en"
    )],
    show_tool_calls=True,
    markdown=True,
)

# Example usage
agent.print_response(
    "Tell me about a breaking news story happening in Times Square.", stream=True
)

# More example prompts to try:
"""
Try these engaging news queries:
1. "What's the latest development in NYC's tech scene?"
2. "Tell me about any upcoming events at Madison Square Garden"
3. "What's the weather impact on NYC today?"
4. "Any updates on the NYC subway system?"
5. "What's the hottest food trend in Manhattan right now?"
"""
