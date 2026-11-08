from dotenv import load_dotenv

load_dotenv()
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

tavily = TavilyClient()

@tool
def search(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    print(f"Searching for: {query}")
    return tavily.search(query = query)

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")
tools = [search]
agent = create_agent(model=llm, tools=tools)

def main():
    print("Starting the agent...")
    result = agent.invoke({"messages": HumanMessage(content="Search for 3 job postings for an ai engineer using langchain in Monterrey Nuevo Leon en linkedin y sus detalles")})
    print(f"Result: {result['messages'][-1].text}")

if __name__ == "__main__":
    main()