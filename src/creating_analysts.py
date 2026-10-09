from dotenv import load_dotenv
from utils.nodes import create_analysts
from utils.states import GenerateAnalystsState
from langgraph.graph import START,END,StateGraph
load_dotenv()

#creating our graph
builder=StateGraph(GenerateAnalystsState)
builder.add_node("create_analysts",create_analysts)
builder.add_edge(START,"create_analysts")
builder.add_edge("create_analysts",END)
graph = builder.compile()