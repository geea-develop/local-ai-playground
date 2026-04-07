"""
Config Plugin
Provides configuration management functionality
"""

import json
from typing import Any, Dict, Optional


class ConfigPlugin:
    """Configuration management plugin"""
    
    def __init__(self, default_config: Optional[Dict] = None):
        self.config = default_config or {}
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_all(self) -> Dict:
        """Get all configuration"""
        return self.config.copy()
    
    def load_from_dict(self, config_dict: Dict) -> None:
        """Load configuration from dictionary"""
        self.config.update(config_dict)
    
    def load_from_json(self, json_string: str) -> None:
        """Load configuration from JSON string"""
        self.config.update(json.loads(json_string))
    
    def to_json(self) -> str:
        """Convert configuration to JSON string"""
        return json.dumps(self.config, indent=2)
    
    def reset(self) -> None:
        """Reset configuration"""
        self.config = {}


if __name__ == "__main__":
    config = ConfigPlugin()
    
    # Set individual values
    config.set("app_name", "Claude Playground")
    config.set("debug", True)
    config.set("max_workers", 4)
    
    print(f"App name: {config.get('app_name')}")
    print(f"Debug: {config.get('debug')}")
    print(f"\nAll config:\n{config.to_json()}")
    
    # Load from JSON
    json_config = '{"database": "sqlite", "timeout": 30}'
    config.load_from_json(json_config)
    print(f"\nAfter JSON load:\n{config.to_json()}")
