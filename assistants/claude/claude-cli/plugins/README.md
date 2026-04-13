# Plugins

This directory contains plugin implementations that extend the functionality of the Claude playground.

Plugins are modular extensions that can be loaded, configured, and executed independently.

Current plugins include:
- `cache_plugin.py`: in-memory cache helper
- `config_plugin.py`: config manager
- `logger_plugin.py`: in-process logger
- `user_validation_plugin.py`: adapter to external user-validation API
- `currency_conversion_plugin.py`: adapter to external exchange-rate API

## Structure

Each plugin should:
- Implement a clear interface (e.g., `execute()` method)
- Include configuration options
- Provide comprehensive documentation
- Be independently testable

## Getting Started

1. Review the example plugins
2. Create new plugins by extending the base pattern
3. Load plugins dynamically in your applications
