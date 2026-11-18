from crewai import Task, Crew, Process
from agents.psychological_writer import psychological_writer


def create_psychological_crew(topic: str, agent_goal: str):

    psychological_task = Task(

        description="""
        Write a comprehensive psychological article about:

        {topic}

        Additional objective from the requesting agent:

        {agent_goal}

        Follow these requirements:

        1. Understand the psychological topic.
        2. Explain the relevant psychological concepts.
        3. Discuss human behavior.
        4. Explain relevant psychological theories.
        5. Include practical real-life examples.
        6. Discuss emotional and cognitive aspects.
        7. Include scientific evidence where appropriate.
        8. Avoid unsupported assumptions.
        9. Explain practical applications.
        10. Finish with a meaningful conclusion.

        Do not diagnose individuals.
        Use Markdown formatting.
        """,

        expected_output="""
        A comprehensive psychological article containing:

        - SEO-friendly title
        - Introduction
        - Psychological concepts
        - Relevant theories
        - Real-life examples
        - Practical applications
        - Conclusion
        """,

        agent=psychological_writer
    )

    crew = Crew(
        agents=[psychological_writer],
        tasks=[psychological_task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff(
        inputs={
            "topic": topic,
            "agent_goal": agent_goal
        }
    )