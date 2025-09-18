from deepagents import DeepAgentState, create_deep_agent
from langchain_core.tools import tool
from typing import Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()

# ----------------------------
# State Schema
# ----------------------------
class AgentState(DeepAgentState):
    counter: int = 0

@tool
def increment_tool(state: AgentState):
    """Increment the counter in state."""
    state.counter += 1
    state.last_message = f"Counter is now {state.counter}"
    # Return the state updates as a dict
    return {"counter": state.counter, "last_message": state.last_message}


@tool
def reset_tool(state: AgentState):
    """Reset the counter in state."""
    state.counter = 0
    state.last_message = "Counter reset!"
    return {"counter": state.counter, "last_message": state.last_message}


# Create the agent
agent = create_deep_agent(
    tools=[increment_tool, reset_tool],
    instructions="You are a simple counter bot.",
    state_schema=AgentState,
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.2)
)

state = AgentState(counter=5, messages=[HumanMessage(content="please increment count")])
response = agent.invoke(state)
print(response.content)