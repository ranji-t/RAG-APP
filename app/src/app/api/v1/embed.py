# Third Party Imports
from fastapi import APIRouter, Request


# Create Router
router = APIRouter()


@router.get("")
async def embed_query(request: Request, text: str) -> dict[str, list[float]]:
    """Embed a single query string using the configured embedding model."""
    # 1. Gater resources
    embedder = request.app.state.embedder

    # 2. Get Embeddings of the query
    results = await embedder.aembed_query(text)

    # 3. Return
    return {"embedding": results}


@router.post("")
async def embed_multiple_queries(
    request: Request, texts: list[str]
) -> dict[str, list[list[float]]]:
    """Embed a list of text strings using the configured embedding model."""
    # 1. Gater resources
    embedder = request.app.state.embedder

    # 2. Get Embeddings of the texts
    results = await embedder.aembed_documents(texts)

    # 3. Return the Embeddings
    return {"embeddings": results}
