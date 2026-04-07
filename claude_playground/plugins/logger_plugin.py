"""
Logger Plugin
Provides logging and monitoring functionality
"""

from datetime import datetime
from typing import Any


class LoggerPlugin:
    """Simple logging plugin for tracking events"""
    
    def __init__(self, name: str):
        self.name = name
        self.logs = []
    
    def log(self, level: str, message: str) -> None:
        """Log a message with timestamp"""
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.logs.append(entry)
        print(f"[{timestamp}] {level.upper()}: {message}")
    
    def info(self, message: str) -> None:
        """Log info level message"""
        self.log("info", message)
    
    def error(self, message: str) -> None:
        """Log error level message"""
        self.log("error", message)
    
    def get_logs(self) -> list:
        """Retrieve all logs"""
        return self.logs
    
    def clear_logs(self) -> None:
        """Clear all logs"""
        self.logs = []


if __name__ == "__main__":
    logger = LoggerPlugin("main")
    logger.info("Plugin initialized")
    logger.info("Processing data")
    logger.error("Something went wrong")
    print("\nAll logs:", logger.get_logs())
