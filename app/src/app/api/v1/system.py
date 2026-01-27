# Third Party Imports
from fastapi import APIRouter


# Create Router
router = APIRouter()


@router.get("/")
async def home() -> dict[str, str]:
    """Root endpoint verifying the application is running."""
    return {"message": "Welcome to the RAG backend"}


@router.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "OK"}
