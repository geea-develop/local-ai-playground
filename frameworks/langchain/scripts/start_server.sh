#!/bin/bash

# Start the server
source venv/bin/activate && uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000