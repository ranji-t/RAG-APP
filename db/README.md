# Vector Database (Qdrant)

This directory holds the **Qdrant** vector database service and its persistent data volume. Qdrant stores document embeddings and enables fast similarity search for the RAG pipeline.

## Overview

| Property | Value |
| :--- | :--- |
| **Image** | `qdrant/qdrant:latest` |
| **Container Name** | `vector_db_container` |
| **Network** | `backend_net` (internal only) |
| **Volume** | `./db/data` → `/qdrant/storage` |

## Directory Structure

```plaintext
db/
└── data/    # Persistent volume for Qdrant collections and embeddings
```

> **Note**: The `data/` directory is populated at runtime by the running Qdrant container. Do not manually modify its contents.

## Role in the RAG Pipeline

Qdrant serves two primary functions:

1. **Indexing**: When documents are added via the `/documents/add` API, their embeddings (768-dimensional vectors from `nomic-embed-text`) are stored here, organised into named collections.
2. **Retrieval**: When a question is asked, the question embedding is compared against stored vectors using **cosine similarity** to find the `k=3` most relevant document chunks.

## Collection Configuration

Embeddings are stored with the following vector configuration (defined in `app/src/app/utils/const.py`):

| Parameter | Value |
| :--- | :--- |
| **Dimensions** | `768` |
| **Distance Metric** | Cosine |

## Network Security

This service sits exclusively on `backend_net`, an **internal Docker network**. It has:
- **No inbound access** from the host, the frontend, or the internet.
- **No outbound internet access**.
- Only the FastAPI backend (`app` service) can communicate with it.

## Data Persistence

The `./db/data` directory is bind-mounted into the container at `/qdrant/storage`. This means all collections, vectors, and metadata survive container restarts. To reset the database, stop the stack and clear this directory:

```bash
# Stop the stack first
docker compose down

# Clear all stored embeddings (irreversible)
rm -rf db/data/*
```

## Accessing the Qdrant Dashboard (Development Only)

Qdrant exposes a web dashboard on port `6333`. To access it during development, temporarily expose the port:

```bash
docker run -p 6333:6333 -v ./db/data:/qdrant/storage qdrant/qdrant:latest
```

Then open [http://localhost:6333/dashboard](http://localhost:6333/dashboard) in your browser.

> In the standard `compose.yaml`, port `6333` is **not** exposed to the host for security reasons.
