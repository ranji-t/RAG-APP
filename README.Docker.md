# Docker Orchestration Guide

This guide details the full-stack container orchestration for the RAG Application using **Docker Compose**. It manages the lifecycle and networking of the Frontend, Backend, Vector DB, and Embedder services.

## 🐳 Stack Overview

The `compose.yaml` defines four interacting services:

| Service | Container Name | Description | Networks |
| :--- | :--- | :--- | :--- |
| **Frontend** | `fultter_app` | Nginx serving the Flutter Web UI. | `frontend_net` |
| **Backend** | `fastapi_app` | FastAPI application. | `frontend_net`, `backend_net` |
| **Vector DB** | `vector_db_container` | Qdrant database instance. | `backend_net` |
| **Embedder** | `embedder_container` | Ollama service hosting the embedding model. | `backend_net` |

### Networking
-   **`backend_net`**: An **internal** network. The Embedder and Vector DB are isolated here; they cannot be accessed directly by the Frontend or the outside world (except via mapped ports if specified, but in this setup, they are internal to the backend).
-   **`frontend_net`**: Connecting the Frontend and Backend.

## 🛠️ Configuration

There are two layers of configuration required for the stack to function:

### 1. Root Environment (`.env`)
Located at `./.env`, this file provides **build-time arguments** for Docker Compose. Specifically, it tells the Frontend container where the Backend API is located from the browser's perspective.

```env
BACKEND_URL=http://localhost:8088
```

### 2. Backend Environment (`app/.env/.env`)
Located at `./app/.env/.env`, this file provides **runtime environment variables** for the FastAPI backend, such as database credentials and internal service URLs.

## 🚀 Usage

### Start the Application
To build the images and start all services in detached mode:

```bash
docker compose up --build -d
```

### View Logs
To see the logs of all services:
```bash
docker compose logs -f
```

To view logs for a specific service (e.g., the backend):
```bash
docker compose logs -f app
```

### Stop the Application
To stop the containers:
```bash
docker compose down
```

### Clean Up
To stop the containers and **remove the persistent data volumes** (Database and Embedder data):
```bash
docker compose down -v
```

## 🏥 Health Checks

The composition includes health checks to ensure services start in the correct order:

-   **Wrapper/App**: Waits for `embedder` and `vector_db` to be healthy.
    -   *Check*: `curl ... /health`
-   **Frontend**: Waits for `app` to be running.

If a service fails to start, check the logs (`docker compose logs <service>`) to diagnose the issue.

## 🔧 Troubleshooting

-   **"Connection Refused" on Frontend**: Ensure `BACKEND_URL` in the root `.env` matches the port exposed by the `app` service (default: `8088`).
-   **Ollama/Qdrant not found**: Ensure the `app/.env/.env` uses the container names (e.g., `http://embedder_container:11434`) and not `localhost`.
