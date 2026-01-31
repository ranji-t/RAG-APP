# RAG Assistant UI

A sleek, **Flutter-based frontend** for the **Retrieval-Augmented Generation (RAG) Assistant**. This interface allows users to seamlessly interact with knowledge bases by asking questions and receiving AI-generated answers in real-time.

## ✨ Features

-   **Modern UI**: A clean, dark-themed interface built with **Material Design 3**.
-   **Chat Interface**: Conversational entry for detailed queries.
-   **Real-time RAG**: Asynchronous communication with the backend for streaming-like responses.
-   **Cross-Platform**: Optimized for **Web**, but capable of running on Windows, macOS, Linux, Android, and iOS.
-   **Dynamic Configuration**: Backend URL can be configured at build/runtime.

## 🛠️ Tech Stack

-   **Framework**: Flutter (Dart)
-   **Networking**: `http` package
-   **Architecture**: Clean functional component widget structure.

## 📋 Prerequisites

-   **Flutter SDK**: [Install Flutter](https://docs.flutter.dev/get-started/install) (Version 3.10.7+).
-   **RAG Backend**: Ensure the FastAPI backend is running.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd RAG_App/ui
```

### 2. Install Dependencies

```bash
flutter pub get
```

### 3. Run the Application

You can run the application targeting different platforms. The default setup is optimized for **Chrome**.

#### 🖥️ Web Development (Recommended)

Run on port **8888** with the backend URL configured:

```bash
flutter run -d chrome --web-port 8888 --dart-define=BACKEND_URL=http://localhost:8000
```

> **Note**: `http://localhost:8000` is the default backend address. Update it if your backend is hosted elsewhere.

#### 🐳 Docker

To run the UI in a container (served via Nginx):

```bash
docker build -t rag-frontend .
docker run -p 80:80 -e BACKEND_URL=http://localhost:8088 rag-frontend
```

## ⚙️ Configuration

The application uses `dart-define` to inject environment variables at compile time.

-   **`BACKEND_URL`**: The base URL of the RAG backend API (e.g., `http://localhost:8000`).

If not provided, it defaults to `http://localhost:8000` inside `lib/main.dart` (ensure your codebase reflects this logic).

## 📂 Project Structure

```plaintext
ui/
├── android/            # Android native code
├── config/             # Nginx configuration (nginx.conf)
├── ios/                # iOS native code
├── lib/
│   └── main.dart       # Main entry point and UI logic
├── test/               # Unit and widget tests
├── web/                # Web entry point
├── pubspec.yaml        # Dependencies (http, cupertino_icons)
├── README.Docker.md    # Extended Docker instructions
└── Dockerfile          # Production Docker build
```

## 📸 Screenshots

*(Add screenshots here to showcase the UI)*
