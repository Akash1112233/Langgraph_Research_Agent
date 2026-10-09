from dotenv import load_dotenv
from src.utils.states import GenerateAnalystsState
from typing import Literal
from langgraph.graph import END
load_dotenv()

def should_continue(state:GenerateAnalystsState)->Literal["create_analysts",END]:
    """Return the next node to excute"""

    human_analyst_feedback = state.get("human_analyst_feedback",None)

    if human_analyst_feedback:
        return "create_analysts"
    return END