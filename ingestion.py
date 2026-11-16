import os
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader
from pathlib import Path
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

file_path = Path(__file__).parent / "mediumblog.txt"

load_dotenv()

if __name__ == "__main__":
    print("Running ingestion script...")


    loader = UnstructuredLoader(file_path = file_path, chunking_strategy = "basic", max_characters = 1000000)
    document = loader.load()

    print(f"Document loaded successfully. Number of chunks: {len(document)}")
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
    texts = text_splitter.split_documents(document)
    print(f"Document split into {len(texts)} chunks.")

    embeddings =  GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
    PineconeVectorStore.from_documents(texts, embeddings, index_name = os.environ["INDEX_NAME"])
    print(f"Document embeddings created and stored in Pinecone index '{os.environ['INDEX_NAME']}' successfully.")