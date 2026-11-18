from crewai import Task, Crew, Process
from agents.technical_writer import technical_writer


def create_technical_crew(topic: str, agent_goal: str):

    technical_task = Task(

        description="""
        Write a comprehensive technical article about:

        {topic}

        Additional objective from the requesting agent:

        {agent_goal}

        Follow these requirements:

        1. Understand the technical topic.
        2. Explain the fundamental concepts.
        3. Explain how the technology works.
        4. Include architecture where relevant.
        5. Include practical programming examples.
        6. Explain code step by step.
        7. Discuss real-world applications.
        8. Explain advantages and limitations.
        9. Include common mistakes.
        10. Finish with a conclusion.

        Ensure all programming examples are syntactically correct.
        Do not invent technical specifications.
        Use Markdown formatting.
        """,

        expected_output="""
        A complete technical article containing:

        - SEO-friendly title
        - Introduction
        - Detailed explanations
        - Technical examples
        - Code examples where appropriate
        - Real-world applications
        - Advantages and limitations
        - Conclusion
        """,

        agent=technical_writer
    )

    crew = Crew(
        agents=[technical_writer],
        tasks=[technical_task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff(
        inputs={
            "topic": topic,
            "agent_goal": agent_goal
        }
    )