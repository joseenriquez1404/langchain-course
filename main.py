import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore 

load_dotenv()

print("Initializing chat components...")

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

vector_store = PineconeVectorStore(
    index_name = os.environ["INDEX_NAME"],
    embedding = embeddings
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

prompt_template = ChatPromptTemplate.from_template(
    """Answer the question based only on the following context:

    {context}

    Question: {question}
    Provide a detailed answer.
    """
)

def format_docs(docs):
    """Format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def retrieval_chain_without_lcel(query: str):
    """
    Simple retrieval chain without LCEL
    Manually retrieves documents, formats them, and generates a response.
    
    Limitations:
    - Manual step-by-step process.
    - No built-in streaming support.
    - No async support without additional code
    - Harder to compose with other chains.
    - More verbose and error-prone.
    """

    docs = retriever.invoke(query)

    context = format_docs(docs)

    messages = prompt_template.format_messages(context = context, question = query)

    response = llm.invoke(messages)

    return response.content



if __name__ == "__main__":
    print("Retrieving relevant documents from Pinecone index...")

    query = "What is Pinecone in Machine Learning?"

    print("\n" + "=" * 70)
    print("Implementation 1 without LCEL")
    print("=" * 70 + "\n")
    result_without_lcel = retrieval_chain_without_lcel(query)
    print("\nAnswer without LCEL:\n")
    print(result_without_lcel)