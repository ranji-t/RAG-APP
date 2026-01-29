# RAG Assistant UI

A Flutter-based frontend for the RAG (Retrieval-Augmented Generation) Assistant application. This user interface interacts with a backend API to allow users to ask questions and receive AI-generated answers based on a knowledge base.

## Features

*   **Clean Interface:** A dark-themed, user-friendly interface powered by Flutter's Material Design.
*   **Query Input:** A large, expandable text field for entering detailed questions.
*   **Real-time Interaction:** Sends queries to a backend server and asynchronously awaits the response.
*   **Response Display:** Clearly displays the AI's answer in a highlighted container once received.
*   **Cross-Platform:** Built with Flutter, capable of running on Web, Windows, macOS, Linux, Android, and iOS.

## Prerequisites

Before running this application, ensure you have the following installed:

*   [Flutter SDK](https://docs.flutter.dev/get-started/install) (Version 3.10.7 or higher recommended)
*   A running instance of the RAG Backend (FastAPI).
    *   **Note:** The app expects the backend to be running at `http://localhost:8000`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd RAG_App/ui
    ```

2.  **Install dependencies:**
    ```bash
    flutter pub get
    ```

## Usage

1.  **Start the Backend:**
    Ensure your FastAPI backend is running locally on port 8000.

2.  **Run the App:**
    To run the application in Chrome with experimental hot reload enable on a specific port, navigate to the UI root directory and use the following command:

    ```bash
    flutter run -d chrome --web-experimental-hot-reload --web-port 8888 --dart-define=BACKEND_URL=http://localhost:8000
    ```

## Application Screenshot

Here is a preview of the RAG Assistant UI in action:



## Configuration

The API endpoint is currently hardcoded in `lib/main.dart`:

```dart
final url = Uri.parse(
  "http://localhost:8000/rag/ask?question=$encodedText&collection_name=DEFAULT_COLLECTIONS",
);
```

If your backend is running on a different host or port, please update this URL in `_RAGHomeScreenState.sendDataOnButtonPress`.

## Project Structure

*   `lib/main.dart`: The main entry point and UI logic for the application.
*   `pubspec.yaml`: Project metadata and dependencies.
