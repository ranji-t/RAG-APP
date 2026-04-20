# Embedder Service

This directory contains the **Ollama**-based embedding and inference service. It is responsible for generating vector embeddings from text, which are then stored in the Qdrant vector database.

## Overview

| Property | Value |
| :--- | :--- |
| **Base Image** | `ollama/ollama:0.15.1` |
| **Container Name** | `embedder_container` |
| **Network** | `backend_net` (internal only) |
| **Volume** | `./embedder/data` → `/root/.ollama` |

## Bundled Model

The Dockerfile pre-pulls the following model at **build time**, so it is available immediately on container startup with no internet access required at runtime:

| Model | Dimensions | Use Case |
| :--- | :--- | :--- |
| `nomic-embed-text` | 768 | Text embeddings for RAG retrieval |

## Directory Structure

```plaintext
embedder/
├── Dockerfile    # Builds Ollama image with nomic-embed-text pre-loaded
└── data/         # Volume-mapped model storage (/root/.ollama)
```

## How It Works

1. During the Docker build, Ollama is started briefly to pull the `nomic-embed-text` model, then shut down.
2. At runtime, the container serves the Ollama API on its internal port (`11434`).
3. The FastAPI backend connects to it via `http://embedder_container:11434` to generate embeddings for documents and queries.

## Network Security

This service sits exclusively on `backend_net`, an **internal Docker network**. It has:
- **No inbound access** from the host or the frontend.
- **No outbound internet access** at runtime (model is baked in at build time).

## Health Check

The container health is verified with:

```bash
ollama list
```

Checked every `1m30s`, with a `30s` start-up grace period and `5` retries before marking unhealthy.

## Local Development

To interact with the Ollama service directly during development, you can expose the port temporarily:

```bash
docker run -p 11434:11434 embedder_image
```

Then query embeddings via the Ollama REST API:

```bash
curl http://localhost:11434/api/embeddings \
  -d '{"model": "nomic-embed-text", "prompt": "your text here"}'
```
