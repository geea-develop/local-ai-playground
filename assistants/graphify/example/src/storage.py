class Storage:
    """
    Simulates a vector database storage layer.
    """
    def __init__(self, db_type: str = "sqlite"):
        self.db_type = db_type
        print(f"Initialized storage with {self.db_type}")

    def save(self, data: str):
        """Saves data to the 'database'."""
        print(f"Saving to {self.db_type}: {data[:20]}...")
