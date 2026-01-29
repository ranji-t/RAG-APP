# Docker Instructions

This guide provides instructions on how to build and run the RAG App Frontend (Flutter Web) using Docker.

## Prerequisites

-   [Docker](https://docs.docker.com/get-docker/) installed on your machine.
-   A running instance of the **RAG Backend**.

## Building the Image

The Dockerfile utilizes a **multi-stage build**:
1.  **Builder**: An Ubuntu image that installs Flutter and compiles the web application.
2.  **Runner**: A lightweight Nginx image that serves the static files.

### 1. Build Command

To build the image, run the following command from the `ui` directory. You can optionally pass the `BACKEND_URL` as a build argument if you want to bake a default URL into the static files (though runtime configuration is preferred for flexibility, Flutter Web compiles this into the JS bundle).

```bash
docker build -t rag-frontend .
```

**With a custom Backend URL:**
```bash
docker build --build-arg BACKEND_URL=http://localhost:8088 -t rag-frontend .
```

## Running the Container

The Nginx server listens on port **80** inside the container.

### 1. Basic Run

```bash
docker run -p 8888:80 rag-frontend
```
*Access the app at `http://localhost:8888`*

### 2. Connecting to the Backend

Since this is a client-side application (running in the user's browser, not strictly "inside" the container network in the same way a backend service is), the `BACKEND_URL` needs to be accessible from the **browser**.

-   **If running locally**: `http://localhost:8000` (or `8088` if using the Docker backend) usually works.
-   **If configuring via `compose.yaml`**: Ensure the environment variable or build arg points to the URL where the browser can reach the backend.

### 3. Using Docker Compose

For a complete setup, use the `compose.yaml` in the root of the repository, which orchestrates both the backend and frontend.

```bash
docker compose up --build
```

## Important Notes

-   **Hot Reload**: Docker is **NOT** recommended for active development requiring hot reload. Use `flutter run` on your host machine for that.
-   **Build Time**: The first build may take a few minutes as it downloads the Flutter SDK. Subsequent builds will be faster due to layer caching.