# Third Party Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Internal Imports
from app.core import lifespan
from app.api.v1 import system, collections, embed, documents, rag
from app.utils.network import get_allowed_origins


# The apps and services
app = FastAPI(
    root_path="/api",
    lifespan=lifespan,
    debug=True,
    title="The RAG backend",
    version="0.0.1",
)


# Origins
# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the router
app.include_router(system.router, prefix="", tags=["System"])
app.include_router(collections.router, prefix="/collections", tags=["Collections"])
app.include_router(embed.router, prefix="/embed", tags=["Embed"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
