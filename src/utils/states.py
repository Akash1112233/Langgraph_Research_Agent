from typing_extensions import TypedDict,NotRequired
from typing import Optional,List
from objects import Analyst

class GenerateAnalystsState(TypedDict):
    topic:str # topic name
    max_analysts:int # no of analysts
    human_analyst_feedback:NotRequired[Optional[str]]
    analysts:NotRequired[List[Analyst]]