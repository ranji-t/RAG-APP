# Standard Imports
import os

# Third Party Imports
from fastapi import FastAPI
from langchain_ollama import OllamaEmbeddings


app = FastAPI(debug=True, title="The RAG backend", version="0.0.1")
embedder = OllamaEmbeddings(model="nomic-embed-text", base_url=os.getenv("OLLAMA_URL"))


@app.get("/")
async def home() -> dict[str, str]:
    return {"message": "Welcome to the RAG backend"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"message": "OK"}


@app.get("/embed_query")
async def embed_query(text: str) -> dict[str, list[float]]:
    # get results
    results = await embedder.aembed_query(text)
    # Return
    return {"embedding": results}


@app.post("/embed")
async def embed(texts: list[str]) -> dict[str, list[list[float]]]:
    # Get results
    results = await embedder.aembed_documents(texts)
    # Return the data
    return {"embeddings": results}
