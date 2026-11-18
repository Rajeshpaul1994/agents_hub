from crewai import Agent, LLM
import os
from dotenv import load_dotenv
load_dotenv()


llm = LLM(
    model="gpt-5.4-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),  # Or set OPENAI_API_KEY
    reasoning_effort="low",
    max_completion_tokens=2000
)



def create_psychological_writer(mcp_tools):
    your_unique_identification = "a715e77e-8d64-46cd-81de-64f112d44731"
    psychological_writer = Agent(
        role="Professional Psychological Article Writer",

        goal="""
        Research psychological topics, write comprehensive
        articles and publish them to the article database.
        """,

        backstory=f"""
        You are an experienced psychological researcher
        and professional article writer.

        You understand human psychology, behavior,
        emotional intelligence and cognitive psychology.

        your unique identification id is : {your_unique_identification}
        """,

        llm=llm,
        tools=mcp_tools,
        verbose=True,
        allow_delegation=False
    )
    return psychological_writer