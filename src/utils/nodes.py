from dotenv import load_dotenv
from states import GenerateAnalystsState
from models import llm
from objects import Analyst,Perspectives
from prompts import analyst_instructions
from langchain.messages import SystemMessage,HumanMessage
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
