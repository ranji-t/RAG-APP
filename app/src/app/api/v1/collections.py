# Third Party Imports
from fastapi import APIRouter, Request

# Internal Imports
from ...services import CollectionsService
from ...utils import DEFAULT_COLLECTIONS


# Create Router
router = APIRouter()


@router.get("")
async def list_collections(request: Request) -> dict[str, list[str]]:
    """Retrieve the list of available collections in Qdrant."""
    # 1. Gater resources
    qd_client = request.app.state.qd_async

    # 2. Return the collections list
    return {
        "collections": [
            col.name
            for col in (
                await CollectionsService.list_collections(qd_client)
            ).collections
        ]
    }


@router.post("")
async def create_collection(
    request: Request, name: str | None = DEFAULT_COLLECTIONS
) -> dict[str, str]:
    """Create a new collection in Qdrant if it does not already exist."""
    # 1. Gater resources
    qd_client = request.app.state.qd_async

    # 2. Create the collection
    collection_name = name if name is not None else DEFAULT_COLLECTIONS
    message = await CollectionsService.create_collection(qd_client, collection_name)

    # 3. Return the message
    return {"message": message}


@router.delete("")
async def delete_collection(
    request: Request,
    collection_name: str = DEFAULT_COLLECTIONS,
) -> dict[str, str]:
    """Delete a specific collection from Qdrant."""
    # 1. Gater resources
    qd_client = request.app.state.qd_async

    # 2. Delete the collection
    message = await CollectionsService.delete_collection(qd_client, collection_name)

    # 3. Return the message
    return {"message": message}
