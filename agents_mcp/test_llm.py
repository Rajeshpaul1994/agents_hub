from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gpt-5.4-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),
    temperature=0.2,
    max_completion_tokens=4000
)

response = llm.call(
    messages=[
        {
            "role": "user",
            "content": "Explain anxiety in three sentences."
        }
    ]
)

print("LLM Response:")
print(response)