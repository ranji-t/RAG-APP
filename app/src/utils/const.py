# Third Party Imports
from qdrant_client import models

EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 768
DEFAULT_COLLECTIONS = "DEFAULT_COLLECTIONS"
VECTOR_CONFIG = models.VectorParams(
    size=EMBEDDING_DIM,
    distance=models.Distance.COSINE,  # Safe default for text
)
