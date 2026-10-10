# from dotenv import load_dotenv
# load_dotenv()
# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",temperature= 0)

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

# Main model for the LangGraph Research Agent
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0,
    max_tokens=2048,
)

# Use the same model for structured output, if needed
structured_llm = llm

