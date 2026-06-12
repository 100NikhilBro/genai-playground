import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000,
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(docs)

# print("total chunks ",len(split_docs))

# huggingFace - Local
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Gemini

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
#
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="gemini-embedding-001"
# )


# OpenAi

# from langchain_openai import OpenAIEmbeddings
#
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-large",
#     api_key=os.getenv("OPENAI_API_KEY")
# )


# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333/",
#     collection_name="learning_langchain_hf",
#     embedding=embeddings
# )


# vector_store.add_documents(split_docs)

# print("Injection Done - Local embeddings )")




retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333/",
    collection_name="learning_langchain_hf",
    embedding=embeddings
) 

relevant_chunks = retriever.similarity_search(
    query='What is FS Module?'
)


# print("Relevant Chunks" , relevant_chunks)



SYSTEM_PROMPT = f"""

You are a helpful AI Assistant who responds based on the available Context.

Context:
{relevant_chunks}


"""