import os

from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model=f"groq/{os.getenv('GROQ_MODEL')}",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)