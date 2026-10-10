from dotenv import load_dotenv
from src.utils.states import GenerateAnalystsState,InterviewState,ResearchGraphState
from typing import Literal
from langgraph.graph import END
from langchain.messages import AIMessage
from langgraph.types import Send
from langchain.messages import HumanMessage
load_dotenv()

def should_continue(state:GenerateAnalystsState)->Literal["create_analysts",END]:
    """Return the next node to excute"""

    human_analyst_feedback = state.get("human_analyst_feedback",None)

    if human_analyst_feedback:
        return "create_analysts"
    return END

def route_messages(state:InterviewState,name:str="expert"):
    """Route Between questiona and Answer"""
    #Get Messages
    messages = state["messages"]
    max_num_turns= state.get("max_num_turns",2)
    #check the no of expert answers
    num_responces = len([m for m in messages if isinstance(m,AIMessage) and m.name == name])

    if num_responces >= max_num_turns:
        return "save_interview"

    return "ask_question"

def initiate_all_interviews(state: ResearchGraphState):
    """This is the map step where we run each interview in a subgraph using Send API"""

    human_analyst_feedback = state.get("human_analyst_feedback")

    if human_analyst_feedback:
        return "create_analysts"
    else:
        topic = state["topic"]
        return [
            Send("conduct_interview", {
                "analyst": analyst,
                "messages": [
                    HumanMessage(
                        content=f"So you said you were writing an article on {topic}?"
                    )
                ]
            })
            for analyst in state["analysts"]
        ]

