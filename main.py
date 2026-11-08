from dotenv import load_dotenv

load_dotenv()
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)

def main():
    print("Starting the agent...")
    result = agent.invoke({"messages": HumanMessage(content="Search for 3 job postings for an ai engineer using langchain in Monterrey Nuevo Leon en linkedin y sus detalles")})
    print(f"Result: {result['messages'][-1].text}")

if __name__ == "__main__":
    main()