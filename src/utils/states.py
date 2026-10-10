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
    content : Annotated[list,operator.add] #source of docs
    analyst : Analyst # My analyst
    interview:str #interview Transcript
    section:list