from typing_extensions import TypedDict,NotRequired,Annotated
from typing import Optional,List
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
import operator

class GenerateAnalystsState(TypedDict):
    topic:str # topic name
    max_analysts:int # no of analysts
    human_analyst_feedback:NotRequired[Optional[str]]
    analysts:NotRequired[List[Analyst]]

class InterviewState(MessagesState):
    max_num_turns:int # no turns of conversations
    context : Annotated[list,operator.add] #source of docs
    analyst : Analyst # My analyst
    interview:str #interview Transcript
    section:list

class ResearchGraphState(TypedDict):
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    human_analyst_feedback: NotRequired[Optional[str]]  # Human feedback
    analysts: List[Analyst]  # Analysts asking questions
    sections: Annotated[list, operator.add]  # Send() API key
    introduction: str  # Introduction for the final report
    content: str  # Content for the final report
    conclusion: str  # Conclusion for the final report
    final_report: str  # Final report