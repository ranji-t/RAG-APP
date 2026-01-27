# Standard Impots
import uuid

# Third Party Imports
from fastapi import APIRouter, Request
from langchain_qdrant import QdrantVectorStore

# Internal Imports
from ...utils import DEFAULT_COLLECTIONS
from ...services import chunk_docs


# Create Router
router = APIRouter()


@router.post("add")
async def add_documents(
    request: Request,
    page_content: str,
    metadata_source: str,
    collection_name: str = DEFAULT_COLLECTIONS,
):
    """Add documents to the Qdrant vector store after chunking and embedding them."""
    # 1. Gater resources
    qd_client_sync = request.app.state.qd_sync
    embedder = request.app.state.embedder

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


@router.post("query")
async def query_documents(
    request: Request, query: str, k: int = 5, collection_name: str = DEFAULT_COLLECTIONS
):
    """Search for similar documents in the Qdrant vector store based on the query."""
    # 1. Gater resources
    qd_client_sync = request.app.state.qd_sync
    embedder = request.app.state.embedder

    # 2. Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)

    # 3. Get results
    results = await vecstore.asimilarity_search(query, k=k)

    # 4. Return the results
    return {"results": results}
