from dotenv import load_dotenv
from src.utils.nodes import create_analysts,human_feedback
from src.utils.states import GenerateAnalystsState
from langgraph.graph import START,END,StateGraph
from src.utils.edges import should_continue
load_dotenv()

#creating our graph
builder=StateGraph(GenerateAnalystsState)
builder.add_node("create_analysts",create_analysts)
builder.add_node("human_feedback",human_feedback)
builder.add_edge(START,"create_analysts")
builder.add_edge("create_analysts","human_feedback")
builder.add_conditional_edges("human_feedback",END)

graph = builder.compile()