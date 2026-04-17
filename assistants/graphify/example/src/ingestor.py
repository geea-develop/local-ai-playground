import requests

class Ingestor:
    """
    Handles fetching data from external URLs or local files.
    Demonstrates a dependency on the 'requests' library.
    """
    def __init__(self):
        self.timeout = 10

    def fetch(self, source: str) -> str:
        """Fetches raw content from the source."""
        if source.startswith("http"):
            # Mocking a network call
            return f"Raw content from web: {source}"
        return f"Raw content from file: {source}"
