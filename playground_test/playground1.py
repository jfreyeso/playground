from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.github import GithubTools
from agno.tools.giphy import GiphyTools
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.models.aws import Claude
import bedrockAgent as BA

import os
from dotenv import load_dotenv

load_dotenv()

MODELS = "arn:aws:bedrock:us-east-2:204664655215:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"

agent_Claude = Agent(
    name="Claude Agent",
    model=Claude(id=MODELS),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

agent_bedrock = BA.BedRockAgent(model_id=MODELS)

#Giphy Agent
giphy_agent = Agent(
name="Giphy Agent",
role="Find relevant GIFs",
model=Claude(id=MODELS),
tools=[GiphyTools(
api_key=os.getenv("GIPHY_API_KEY"),
limit=1 # Number of GIFs to return
)],
instructions="Find relevant and appropriate GIFs related to the query.",
show_tool_calls=True,
markdown=True,
debug_mode=True
)

#GitHub Code Agent
github_agent = Agent(
name="GitHub Code Agent",
role="Find code examples on GitHub",
model=Claude(id=MODELS),
tools=[GithubTools()],
instructions="review the repo https://github.com/jfreyeso/playground/ and anwser questions about it.",
show_tool_calls=True,
markdown=True,
debug_mode=True
)

github_agent_2 = Agent(
name="GitHub Code Agent 2",
role="Find code examples on GitHub",
model=Claude(id=MODELS),
tools=[GithubTools()],
instructions="review the repo https://github.com/jfreyeso/playground/ and anwser questions about it.",
show_tool_calls=True,
markdown=True,
debug_mode=True
)

app = Playground(agents=[github_agent,github_agent_2, giphy_agent, agent_Claude,agent_bedrock,]).get_app()

if __name__ == "__main__":
    
    # Ensure the app is awaited if `get_app()` is a coroutine
    serve_playground_app("playground1:app", reload=True)