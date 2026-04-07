#!/usr/bin/env python3
"""Test script to verify model validation without importing mlx."""

import sys
import os
from pathlib import Path

# Load env first
from dotenv import load_dotenv
load_dotenv()

print("=" * 80)
print("Testing Model Validation")
print("=" * 80)

# Test 1: Check environment variables
print("\n1. Environment Variables:")
models_dir = os.getenv("MODELS_DIR_PATH")
model_dir = os.getenv("MODEL_DIR_PATH")
print(f"   MODELS_DIR_PATH={models_dir}")
print(f"   MODEL_DIR_PATH={model_dir}")

# Test 2: Get model path
print(f"\n2. Model Path Construction:")
if models_dir and model_dir:
    model_path = os.path.join(models_dir, model_dir)
    print(f"   Full path: {model_path}")
else:
    print(f"   Cannot construct path (missing env vars)")

# Test 3: Validate model path
print(f"\n3. Model Validation:")
if not models_dir:
    print(f"   ✗ MODELS_DIR_PATH not set - model will fail to load")
elif not model_dir:
    print(f"   ✗ MODEL_DIR_PATH not set - model will fail to load")
else:
    model_path = os.path.join(models_dir, model_dir)
    if os.path.isdir(model_path):
        print(f"   ✓ Model path is valid: {model_path}")
        files_in_model = os.listdir(model_path)
        print(f"   Directory contains {len(files_in_model)} items")
        for f in files_in_model[:5]:  # Show first 5
            print(f"      - {f}")
    else:
        print(f"   ✗ Model directory not found: {model_path}")
        if os.path.exists(model_path):
            print(f"      (exists but is not a directory)")
        else:
            print(f"      (does not exist)")

print("\n" + "=" * 80)
