# Third Party Impots
from qdrant_client import AsyncQdrantClient

# Internla Imports
from ..utils import VECTOR_CONFIG


class CollectionsService:
    def __init__(self):
        pass

    @classmethod
    async def list_collections(cls, qd_client: AsyncQdrantClient):
        return qd_client.get_collections()

    @classmethod
    async def create_collection(
        cls, qd_client: AsyncQdrantClient, collection_name: str
    ) -> str:
        # Create the collection
        if await qd_client.collection_exists(collection_name):
            message = f"Collection {collection_name} already exists"
        else:
            await qd_client.create_collection(
                collection_name, vectors_config=VECTOR_CONFIG
            )
            message = "Collection created"
        return message

    @classmethod
    async def delete_collection(
        cls, qd_client: AsyncQdrantClient, collection_name: str
    ) -> str:
        await qd_client.delete_collection(collection_name)
        return f"Collection deleted: {collection_name}"
