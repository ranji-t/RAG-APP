# RAG Application Backend

This repository houses the high-performance backend for a **Retrieval-Augmented Generation (RAG)** application. Built with **FastAPI**, it orchestrates a powerful pipeline integrating **Qdrant** for vector storage, **Ollama** for efficient embeddings, and **OpenAI's GPT-4o** for advanced language understanding.

## 🚀 Features

-   **High-Performance API**: Asynchronous, scalable backend powered by **FastAPI**.
-   **Intelligent RAG Pipeline**: Seamless integration of retrieval and generation using **LangChain**.
-   **Vector Search**: **Qdrant** integration for lightning-fast similarity searches.
-   **Flexible Embeddings**: Utilizes **Ollama** for local or remote embedding generation.
-   **Advanced LLM Support**: Harnesses **OpenAI GPT-4o** for high-quality responses.
-   **Document Management**: robust APIs to chunk, embed, and store documents.
-   **Collection Management**: Dynamic control over Qdrant collections.
-   **Modern Tooling**: Managed with `uv` for lightning-fast dependency resolution.
-   **Docker Ready**: Full containerization support.

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.13+ | The core programming language. |
| **Framework** | FastAPI | Modern, fast web framework for building APIs. |
| **Vector Store** | Qdrant | Vector similarity search engine. |
| **Embeddings** | Ollama | Local LLM and embedding runner. |
| **LLM** | OpenAI GPT-4o | State-of-the-art language model. |
| **Orchestration** | LangChain | Framework for developing applications powered by LLMs. |

## 📋 Prerequisites

Ensure you have the following ready before starting:

1.  **Python 3.13+** installed.
2.  **uv** package manager installed (`pip install uv` or via other methods).
3.  **Qdrant** instance running (Local Docker or Cloud).
4.  **Ollama** instance running.
5.  **OpenAI API Key**.

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone <repository_url>
cd RAG_App/app
```

### 2. Configure Environment

The environment variables are managed in the `.env/` directory:

-   **`.env/.env.local`**: For **local development**.
-   **`.env/.env`**: For **Docker/Production** (configured for service-to-service communication).

**Example `.env/.env.local` (Local):**
```env
OLLAMA_URL=http://localhost:11435
QDRANT_URL=http://localhost:6333
FLUTTER_URL=http://localhost:8888
OPENAI_API_KEY=sk-...
```

**Example `.env/.env` (Docker):**
```env
OLLAMA_URL=http://embedder_container:11434
QDRANT_URL=http://vector_db_container:6333
FLUTTER_URL=http://localhost:80
LOCAL_URL=http://localhost
OPENAI_API_KEY=sk-...
```

### 3. Install Dependencies

Use `uv` to sync dependencies instantly:

```bash
uv sync
```

### 4. Run the Application

#### 🖥️ Local Development (Hot Reload)

Runs on port `8000` by default.

```bash
uv run uvicorn main:app --host "localhost" --port 8000 --env-file .env/.env.local --app-dir ./src/ --reload
```

#### 🐳 Docker Container

The Docker image is optimized for production and exposes port `8088`.

Build the image:
```bash
docker build -t rag-backend .
```

Run the container:
```bash
```bash
docker run -p 8088:8088 --env-file .env/.env rag-backend
```

**Note on Connectivity:**
If your Qdrant or Ollama services are running on the host machine (localhost):
-   **Mac/Windows**: Use `OLLAMA_URL=http://host.docker.internal:11434` in your `.env`.
-   **Linux**: Add `--add-host=host.docker.internal:host-gateway` to the `docker run` command.

## 🔌 API Endpoints

The API is versioned (`v1`) and organized by resource. You can explore the interactive docs at `/docs`.

### System
-   `GET /` - Welcome message.
-   `GET /health` - Health check status.

### Collections (`/collections`)
-   `GET /collections` - List all available Qdrant collections.
-   `POST /collections` - Create a new collection.
-   `DELETE /collections` - Delete an existing collection.

### Documents (`/documents`)
-   `POST /documents/add` - Process, chunk, and store a document.
-   `POST /documents/query` - Perform a similarity search against stored documents.

### Embeddings (`/embed`)
-   `GET /embed` - Generate an embedding for a single text query.
-   `POST /embed` - Generate embeddings for a list of texts.

### RAG (`/rag`)
-   `POST /rag/ask` - The core RAG endpoint. Retrieves context and answers a question using GPT-4o.

## 📂 Project Structure

```plaintext
app/
├── .env/                 # Environment configuration (Directory)
├── Dockerfile            # Container definition
├── pyproject.toml        # Project dependencies & config
├── uv.lock               # Dependency lock file
├── README.md             # Documentation
├── README.Docker.md      # Extended Docker instructions
├── notebooks/            # Jupyter notebooks for experiments
├── src/
│   ├── main.py           # App entry point
│   └── app/
│       ├── api/          # Route handlers (v1/)
│       ├── core/         # Lifespan & Config
│       ├── services/     # Business logic (RAG, Collections)
│       └── utils/        # Constants, Loaders, Network helpers
└── test/                 # Test suite
```

## 🧪 Development

This project uses `ruff` for linting/formatting and `mypy` for static type checking.

```bash
uv run ruff check .
uv run ruff format .
uv run mypy src/
```
