from typing import List

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

class Source(BaseModel):
    """Scheme for a source used by the agent"""

    url : str = Field(description="The url of the source")

class AgentResponse(BaseModel):
    """Scheme for agent response with answer and sources"""

    answer : str = Field(description="The agent's answer to the query")
    sources : List[Source] = Field(default_factory = list, description="List of sources used to generate the answer")

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format = AgentResponse)

def main():
    print("Starting the agent...")
    result = agent.invoke({"messages": HumanMessage(content="Search for 3 job postings for an ai engineer using langchain in Monterrey Nuevo Leon en linkedin y sus detalles")})
    print(f"Result: {result['structured_response'].answer}")

if __name__ == "__main__":
    main()