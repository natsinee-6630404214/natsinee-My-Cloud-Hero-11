import os
import logging
import google.cloud.logging

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from google.genai import types
from google.adk.tools import exit_loop

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# ------------------ Logging ------------------
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")
if not model_name:
    raise ValueError("MODEL environment variable not set")


# ------------------ Tools ------------------

def append_to_state(tool_context: ToolContext, field: str, response: str):
    existing = tool_context.state.get(field, [])
    tool_context.state[field] = existing + [response]
    logging.info(f"[STATE UPDATED] {field}")
    return {"status": "success"}


def write_file(tool_context: ToolContext, directory: str, filename: str, content: str):
    path = os.path.join(directory, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return {"status": "success"}


wiki_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# ------------------ Investigation Agents (Parallel) ------------------

admirer_agent = Agent(
    name="admirer_agent",
    model=model_name,
    description="Collects positive achievements.",
    instruction="""
TOPIC: { topic? }

Research ONLY achievements, successes, contributions.

Use keywords:
achievements, contributions, success, positive impact

Use Wikipedia tool and save to state key 'pos_data'
""",
    tools=[wiki_tool, append_to_state],
)

critic_agent = Agent(
    name="critic_agent",
    model=model_name,
    description="Collects negative aspects and controversies.",
    instruction="""
TOPIC: { topic? }

Research ONLY criticisms, failures, controversies.

Use keywords:
controversy, criticism, failure, negative impact

Save to state key 'neg_data'
""",
    tools=[wiki_tool, append_to_state],
)

investigation_team = ParallelAgent(
    name="investigation_team",
    sub_agents=[admirer_agent, critic_agent],
)

# ------------------ Judge (Loop Controller) ------------------

judge_agent = Agent(
    name="judge_agent",
    model=model_name,
    description="Ensures balance between both sides.",
    instruction="""
POSITIVE DATA:
{ pos_data? }

NEGATIVE DATA:
{ neg_data? }

If one side lacks detail → explain what is missing so research continues.
If BOTH sides are balanced → call 'exit_loop'.
""",
    tools=[exit_loop],
)

trial_loop = LoopAgent(
    name="trial_loop",
    sub_agents=[investigation_team, judge_agent],
    max_iterations=3,
)

# ------------------ Verdict Writer ------------------

file_writer = Agent(
    name="file_writer",
    model=model_name,
    description="Writes a neutral court-style report.",
    instruction="""
POSITIVE SIDE:
{ pos_data? }

NEGATIVE SIDE:
{ neg_data? }

Write a neutral comparative historical verdict.
Do not take sides.

Use write_file tool:
directory="output"
filename="verdict.txt"
content=full report
""",
    tools=[write_file],
)

# ------------------ Full Court System ------------------

historical_court = SequentialAgent(
    name="historical_court",
    sub_agents=[trial_loop, file_writer],
)

# ------------------ Root Agent ------------------

root_agent = Agent(
    name="court_clerk",
    model=model_name,
    instruction="""
Ask the user which historical person or event should be examined.

Store the answer using:
append_to_state(field="topic")

Then transfer to 'historical_court'
""",
    tools=[append_to_state],
    sub_agents=[historical_court],
)
