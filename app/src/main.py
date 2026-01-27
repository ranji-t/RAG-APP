# Third Party Imports
from fastapi import FastAPI

# Internal Imports
from app.core import lifespan
from app.api.v1 import system, collections, embed, documents, rag


# The apps and services
app = FastAPI(lifespan=lifespan, debug=True, title="The RAG backend", version="0.0.1")

# Include the router
app.include_router(system.router, prefix="", tags=["System"])
app.include_router(collections.router, prefix="/collections", tags=["Collections"])
app.include_router(embed.router, prefix="/embed", tags=["Embed"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
