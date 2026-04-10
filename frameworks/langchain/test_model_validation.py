#!/usr/bin/env python3
"""Test script to verify model validation functions."""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from backend.model_loader import validate_model_path, get_model_path

print("=" * 80)
print("Testing Model Validation")
print("=" * 80)

# Test 1: Check environment variables
print("\n1. Environment Variables:")
print(f"   MODELS_DIR_PATH={os.getenv('MODELS_DIR_PATH')}")
print(f"   MODEL_DIR_PATH={os.getenv('MODEL_DIR_PATH')}")

# Test 2: Get model path
model_path = get_model_path()
print(f"\n2. Model Path: {model_path}")

# Test 3: Validate model path
is_valid, error_msg = validate_model_path()
print(f"\n3. Model Validation:")
print(f"   Valid: {is_valid}")
if error_msg:
    print(f"   Error: {error_msg}")
else:
    print(f"   Model path is ready!")
    if model_path and os.path.isdir(model_path):
        files_in_model = os.listdir(model_path)
        print(f"   Model directory contents: {len(files_in_model)} items")
        for f in files_in_model[:5]:  # Show first 5
            print(f"      - {f}")

print("\n" + "=" * 80)
