# Standard Imports
import os
import uuid
from contextlib import asynccontextmanager

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

    # 2. Pause the programm is running
    yield

    # 3. App closing steps
    app.state.embedder = None
    await app.state.qd_async.close()
    app.state.qd_sync.close()


# The apps and services
app = FastAPI(lifespan=lifespan, debug=True, title="The RAG backend", version="0.0.1")


@app.get("/")
async def home() -> dict[str, str]:
    """Root endpoint verifying the application is running."""
    return {"message": "Welcome to the RAG backend"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "OK"}


@app.get("/embed_query")
async def embed_query(text: str) -> dict[str, list[float]]:
    """Embed a single query string using the configured embedding model."""
    # 1. Gater resources
    embedder = app.state.embedder

    # 2. Get Embeddings of the query
    results = await embedder.aembed_query(text)

    # 3. Return
    return {"embedding": results}


@app.post("/embed")
async def embed(texts: list[str]) -> dict[str, list[list[float]]]:
    """Embed a list of text strings using the configured embedding model."""
    # 1. Gater resources
    embedder = app.state.embedder

    # 2. Get Embeddings of the texts
    results = await embedder.aembed_documents(texts)

    # 3. Return the Embeddings
    return {"embeddings": results}


@app.get("/collections")
async def collections() -> dict[str, list[str]]:
    """Retrieve the list of available collections in Qdrant."""
    # 1. Gater resources
    qd_client = app.state.qd_async

    # 2. Return the collections list
    return {
        "collections": [
            col.name for col in (await qd_client.get_collections()).collections
        ]
    }


@app.post("/collections")
async def create_collection(name: str | None = DEFAULT_COLLECTIONS):
    """Create a new collection in Qdrant if it does not already exist."""
    # 1. Gater resources
    qd_client = app.state.qd_async

    # 2. Create the collection
    collection_name = name if name is not None else DEFAULT_COLLECTIONS
    if await qd_client.collection_exists(collection_name):
        message = f"Collection {collection_name} already exists"
    else:
        await qd_client.create_collection(collection_name, vectors_config=VECTOR_CONFIG)
        message = "Collection created"

    # 3. Return the message
    return {"message": message}


@app.delete("/collections")
async def flush_collection(collection_name: str = DEFAULT_COLLECTIONS):
    """Delete a specific collection from Qdrant."""
    # 1. Gater resources
    qd_client = app.state.qd_async

    # 2. Delete the collection
    await qd_client.delete_collection(collection_name)

    # 3. Return the message
    return {"message": "Collection deleted"}


async def chunk_docs(page_content: str, metadata_source: str) -> list[Document]:
    """Split the documents into chunks."""
    # 1. Convert to Documents
    doc = Document(page_content=page_content, metadata={"source": metadata_source})

    # 2. Document chunks
    doc_splits = RecursiveCharacterTextSplitter(
        chunk_size=1_000, chunk_overlap=100, add_start_index=True
    ).split_documents([doc])

    # 3. Return document chunks
    return doc_splits


@app.post("/add_docs")
async def add_docs(
    page_content: str, metadata_source: str, collection_name: str = DEFAULT_COLLECTIONS
):
    """Add documents to the Qdrant vector store after chunking and embedding them."""
    # 1. Gater resources
    qd_client_sync = app.state.qd_sync
    embedder = app.state.embedder

    # 2. Split the docs
    doc_splits = await chunk_docs(
        page_content=page_content, metadata_source=metadata_source
    )

    # 3. Get IDs
    ids = [uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc.metadata}") for doc in doc_splits]

    # 4. Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)

    # 5. Add the docs to images
    await vecstore.aadd_documents(doc_splits, ids=ids)

    # 6. Return the message with number of docs added
    return {"message": f"Added {len(doc_splits)} documents to {collection_name}"}


@app.post("/query")
async def query(query: str, k: int = 5, collection_name: str = DEFAULT_COLLECTIONS):
    """Search for similar documents in the Qdrant vector store based on the query."""
    # 1. Gater resources
    qd_client_sync = app.state.qd_sync
    embedder = app.state.embedder

    # 2. Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)

    # 3. Get results
    results = await vecstore.asimilarity_search(query, k=k)

    # 4. Return the results
    return {"results": results}
