from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
# The correct import for creating agents is from langgraph
from langgraph.prebuilt import create_react_agent

# 1. Define the tool
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is 25°C and sunny."

# 2. Initialize the "lite" model (gemini-2.5-flash)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 3. Create the agent using LangGraph's prebuilt ReAct agent
agent = create_react_agent(llm, tools=[get_weather])

if __name__ == "__main__":
    # LangGraph agents expect an input dict containing a list of messages
    result = agent.invoke({"messages": [("user", "What's the weather in Hyderabad?")]})
    
    # Print the resulting conversation history
    for msg in result["messages"]:
        msg.pretty_print()
