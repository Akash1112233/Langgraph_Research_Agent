from dotenv import load_dotenv
from src.utils.states import GenerateAnalystsState
from src.utils.models import llm
from src.utils.objects import Analyst,Perspectives
from src.utils.prompts import analyst_instructions
from langchain.messages import SystemMessage,HumanMessage
from langgraph.types import interrupt

load_dotenv()

def create_analysts(state:GenerateAnalystsState):
    """Create Analysts"""

    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback","")

    # Enfore Stucture Output 
    structured_llm = llm.with_structured_output(Perspectives)

    # System Message
    system_message = analyst_instructions.format(topic = topic,
                                                 human_analyst_feedback=human_analyst_feedback,
                                                 max_analysts=max_analysts)

    # Generate Analyst
    analysts = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Please Generate the set of analysts.")])

    return {"analysts":analysts.analysts}

def human_feedback(state:GenerateAnalystsState):
    """this is where the human gives feedback about the analysts given"""

    feedback = interrupt({
        "question":"Are analysts ok for you ?",
        "analysts":[
            analyst.model_dump() if hasattr(analyst,"model_dump") else analyst for analyst in state.get("analysts",[])
        ],
        "instructions":"Return feedback to regenerate analysts or return empty/perfect/continue/okay to approve and continue the graph"
    })

    if feedback is None:
        return {"human_analyst_feedback":None}

    if isinstance(feedback,str):
        feedback = feedback.strip()
        if feedback == "":
            return {"human_analyst_feedback":None}
        if feedback.lower() in {"perfect","okay","continue","yes"}:
            return {"human_analyst_feedback":None}
        return {"human_analyst_feedback":feedback}
    return {"human_analyst_feedback":feedback}