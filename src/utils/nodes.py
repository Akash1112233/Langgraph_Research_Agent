from dotenv import load_dotenv
from src.utils.states import GenerateAnalystsState,InterviewState,ResearchGraphState
from src.utils.models import llm
from src.utils.objects import Analyst,Perspectives,SearchQuery
from src.utils.prompts import analyst_instructions,report_writer_instructions,intro_conclusion_instructions,question_instructions,section_writer_instructions,search_instructions,answer_instructions
from langchain.messages import SystemMessage,HumanMessage
from langgraph.types import interrupt
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string

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

def generate_question(state: InterviewState):
    """Generate the analyst's next interview question."""

    analyst = state["analyst"]

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    messages = state["messages"]

    system_message = question_instructions.format(
        goals=analyst.persona
    )

    question = llm.invoke(
        [
            SystemMessage(content=system_message),
            *messages,
            HumanMessage(
                content=(
                    "Ask the next specific question to the expert. "
                    "If you have enough information, end the interview "
                    "with: Thank you so much for your help!"
                )
            )
        ]
    )

    return {"messages": [question]}


def search_web(state:InterviewState):
    """Retrive docs from web"""

    # search query
    structured_llm = llm.with_structured_output(SearchQuery)

    # Search Instruction
    search_instruction_system_message = SystemMessage(content = search_instructions)
    tavily_search = TavilySearch(max_results = 2)

    search_query = structured_llm.invoke(
        [search_instruction_system_message]
        + state["messages"]
        + [
            HumanMessage(
                content="Convert the analyst's final question into a well-structured web search query."
            )
        ]
)

    # Search
    data = tavily_search.invoke({"query":search_query.search_query})
    search_docs = data.get("results",data)

    #format
    # format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context":[formatted_search_docs]}


def search_web2(state:InterviewState):
    """Retrive docs from web"""

    # search query
    structured_llm = llm.with_structured_output(SearchQuery)

    # Search Instruction
    search_instruction_system_message = SystemMessage(content = search_instructions)
    tavily_search = TavilySearch(max_results = 2)

    search_query = structured_llm.invoke(
        [search_instruction_system_message]
            + state["messages"]
            + [
                HumanMessage(
                content="Convert the analyst's final question into a well-structured web search query."
                )
            ]
)

    # Search
    data = tavily_search.invoke({"query":search_query.search_query})
    search_docs = data.get("results",data)

    #format
    # format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context":[formatted_search_docs]}


def generate_answer(state: InterviewState):
    """Node to answer the analyst's question."""

    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    # Prepare the system instructions
    system_message = answer_instructions.format(
        goals=analyst.persona,
        context=context
    )

    # Generate the expert's answer
    answer = llm.invoke(
        [
            SystemMessage(content=system_message),
            *messages,
            HumanMessage(
                content="Answer the analyst's latest question using only the provided context."
            )
        ]
    )

    # Mark the response as coming from the expert
    answer.name = "expert"

    # Append the expert's answer to the conversation history
    return {"messages": [answer]}

def save_interview(state:InterviewState):
    """save the interviews"""
    messages = state["messages"]
    interview = get_buffer_string(messages)

    return {"interview":interview}

def write_section(state:InterviewState):
    """node ot answer a question"""

    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    system_message = section_writer_instructions.format(focus = analyst.description)

    section = llm.invoke(
    [
        SystemMessage(content=system_message),
        HumanMessage(content=f"Use this source to write your section: {context}")
    ]
    )

    return {"sections":[section.content]}

def write_report(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)    
    report = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Write a report based upon these memos.")]) 
    return {"content": report.content}

def write_introduction(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)    
    intro = llm.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")]) 
    return {"introduction": intro.content}

def write_conclusion(state: ResearchGraphState):

    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)    
    conclusion = llm.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")]) 
    return {"conclusion": conclusion.content}

def finalize_report(state: ResearchGraphState):
    """ The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """
    # Save full final report
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {"final_report": final_report}