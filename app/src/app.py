# Standard Imports
import os
import uuid

# Third Party Imports
from fastapi import FastAPI
from qdrant_client import QdrantClient
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Internal Imports
from utils import EMBEDDING_MODEL, DEFAULT_COLLECTIONS, VECTOR_CONFIG


# The apps and services
app = FastAPI(debug=True, title="The RAG backend", version="0.0.1")
embedder = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=os.getenv("OLLAMA_URL"))
qd_client = AsyncQdrantClient(url=os.getenv("QDRANT_URL"))
qd_client_sync = QdrantClient(url=os.getenv("QDRANT_URL"))


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


@app.get("/collections")
async def collections() -> dict[str, list[str]]:
    return {
        "collections": [
            col.name for col in (await qd_client.get_collections()).collections
        ]
    }


@app.post("/collections")
async def create_collection(name: str | None = None):
    collection_name = name if name is not None else DEFAULT_COLLECTIONS
    if await qd_client.collection_exists(collection_name):
        message = f"Collection {collection_name} already exists"
    else:
        await qd_client.create_collection(collection_name, vectors_config=VECTOR_CONFIG)
        message = "Collection created"
    return {"message": message}


async def chunk_docs(page_content: str, metadata_source: str) -> list[Document]:
    # Convert to Documents
    doc = Document(page_content=page_content, metadata={"source": metadata_source})
    # Document chunks
    doc_splits = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=200, add_start_index=True
    ).split_documents([doc])
    # Return document chunks
    return doc_splits


@app.post("/add_docs")
async def add_docs(
    page_content: str, metadata_source: str, collection_name: str = DEFAULT_COLLECTIONS
):
    # Split the docs
    doc_splits = await chunk_docs(
        page_content=page_content, metadata_source=metadata_source
    )
    # Get IDs
    ids = [uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc.metadata}") for doc in doc_splits]

    # Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)
    # Add the docs to images
    await vecstore.aadd_documents(doc_splits, ids=ids)


@app.post("/query")
async def query(query: str, k: int = 5, collection_name: str = DEFAULT_COLLECTIONS):
    # Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)
    # Get results
    results = await vecstore.asimilarity_search(query, k=k)
    # Return the data
    return {"results": results}
