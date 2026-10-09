from pydantic import BaseModel,Field
from typing import List

#creating our object analyst
class Analyst(BaseModel):
    affiliation:str = Field(description="Primary Affiliation of the analyst")
    name:str = Field(description="Name of the Analyst")
    role:str = Field(description="Role of the Analyst in the context of topic")
    description:str = Field(description="Description of the analyst foucs,concerns and motives")

    @property
    def persona(self)->str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}"


class Perspectives(BaseModel):
    analyst:List[Analyst] = Field(description="comprehensive list of analysts with their roles affiliation")