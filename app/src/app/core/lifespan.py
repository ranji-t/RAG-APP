# Standard Imports
import os
from contextlib import asynccontextmanager

# Third Party Imports
from fastapi import FastAPI
from qdrant_client import QdrantClient, AsyncQdrantClient
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI

# Internal Imports
from ..utils import EMBEDDING_MODEL


# Define Lifetime for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle context manager for the FastAPI application.
    Initializes and cleans up resources like the Qdrant client and Embedder.
    """
    # 1. Set the states for opening app
    app.state.embedder: OllamaEmbeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL, base_url=os.getenv("OLLAMA_URL")
    )
    app.state.qd_async: AsyncQdrantClient = AsyncQdrantClient(
        url=os.getenv("QDRANT_URL")
    )
    app.state.qd_sync: QdrantClient = QdrantClient(url=os.getenv("QDRANT_URL"))
    app.state.llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # 2. Pause the programm is running
    yield

    # 3. App closing steps
    app.state.embedder = None
    app.state.llm = None
    await app.state.qd_async.close()
    app.state.qd_sync.close()
