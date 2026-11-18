from crewai import Task, Crew, Process
from crewai_tools import MCPServerAdapter

from agents.psychological_writer import create_psychological_writer


server_params = {
    "url": "http://127.0.0.1:8000/mcp",
    "transport": "streamable-http"
}


def create_psychological_crew(topic: str, agent_goal: str):

    with MCPServerAdapter(server_params) as mcp_tools:

        print("Available MCP tools:")

        for tool in mcp_tools:
            print(tool.name)

        psychological_writer = create_psychological_writer(
            mcp_tools
        )

        psychological_task = Task(
            description="""
            Write a short 100 words article about anxiety.

            After writing the article, publish it to the database.

            If the publishing tool requires authentication,
            do authenticate and save username and password in memory for next time
            use the available authenticated publishing workflow.

            Return the article ID after successful publication.
            """,
            expected_output="Article title, article content and database publication status.",
            agent=psychological_writer
        )

        crew = Crew(

            agents=[psychological_writer],
            tasks=[psychological_task],
            process=Process.sequential,
            memory=True,
            verbose=True
        )

        return crew.kickoff(
            inputs={
                "topic": topic,
                "agent_goal": agent_goal
            }
        )


if __name__ == "__main__":

    topic = "Anxiety"

    agent_goal = """
    Understand psychological topics and produce
    detailed, informative and engaging articles
    about human psychology and behavior.
    """

    result = create_psychological_crew(
        topic,
        agent_goal
    )

    