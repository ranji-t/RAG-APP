# Standard Imports
import os


def get_allowed_origins() -> list[str]:
    """
    Retrieves a list of allowed origins from environment variables.

    Checks for specific environment variables ('OLLAMA_URL', 'QDRANT_URL', 'FLUTTER_URL').
    If any are found, they are returned as the allowed origins.
    If none are found, returns ["*"] to allow all origins (default behavior).

    Returns:
        list[str]: A list of allowed origin URLs or ["*"].
    """
    # Define the keys to check in the environment
    required_keys = (
        "LOCAL_URL",
        "FLUTTER_URL",
    )

    # Collect values for these keys if they exist in the environment
    urls = [val for key in required_keys if (val := os.getenv(key, None)) is not None]

    # Return the specific list if populated, otherwise default to allowing all origins
    return ["*"] if (not urls) else urls
