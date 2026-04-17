import re

class Processor:
    """
    Cleans and prepares data for storage.
    Uses regex to remove noise.
    """
    def clean(self, raw_text: str) -> str:
        """Removes special characters and whitespace."""
        clean_text = re.sub(r'[^\w\s]', '', raw_text)
        return clean_text.strip().lower()
