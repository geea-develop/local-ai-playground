# Model Loading & Debug Logging Fixes

## Summary
Added comprehensive model validation and debug logging to help identify model loading issues. The backend now validates the model configuration at startup and reports the actual model being used instead of hardcoded model names.

## Changes Made

### 1. **backend/model_loader.py**
Added three new functions for better model validation:

#### `validate_model_path() -> tuple[bool, Optional[str]]`
- Validates that both `MODELS_DIR_PATH` and `MODEL_DIR_PATH` environment variables are set
- Checks that the full model directory path exists
- Returns a tuple of (is_valid, error_message)
- **Debug logging**: Logs warnings when env vars are missing or directory doesn't exist

#### `get_model_path() -> Optional[str]`
- Returns the full path to the model directory if configured
- Returns None if environment variables are not set
- Used for reporting and validation

#### Enhanced `get_chat_model()`
- Now logs ERROR level messages when configuration is missing or directory not found
- More descriptive error messages for debugging

#### Enhanced `run_inference()`
- Added debug logging at the start of inference
- Wraps model loading in try-catch to log model loading failures
- Logs success when model loads successfully

### 2. **backend/app.py**
Added startup validation and improved model reporting:

#### New imports
```python
from .model_loader import run_inference, validate_model_path, get_model_path
```

#### Module-level state tracking
```python
_model_valid = False
_model_error_msg: Optional[str] = None
```

#### `@app.on_event("startup")` handler
- **Logs at startup with visual separators** to make validation clear
- Displays configured model directory
- Displays full model path
- Shows validation result (✓ PASSED or ✗ FAILED)
- Captures any error messages for later use

Example output:
```
================================================================================
Backend startup - validating model configuration
================================================================================
Configured MODEL_DIR_PATH: lmstudio-community/Qwen3-4B-Instruct-2507-MLX-4bit
Full model path: /<models-path>/Qwen3-4B-Instruct-2507-MLX-4bit
✓ Model path validation PASSED
================================================================================
```

#### Updated `/v1/models` endpoint
- Now checks `_model_valid` flag
- If model validation failed: logs warning and returns only "local-mlx" model with a note
- If model validation succeeded: returns the actual configured model name using `_ollama_advertised_model_name()`
- Includes compatibility aliases with notes that they route to the local MLX model

## Debugging

### To enable debug logging:
Set `LOG_LEVEL=DEBUG` in your `.env` file (already set)

### What you'll now see:
1. **On startup**: Clear validation report with model path and status
2. **On inference requests**: Debug messages about model loading
3. **On model API calls**: Logs indicating whether model paths are valid

### Environment Variables
Make sure these are set in `.env`:
```
MODELS_DIR_PATH=/path/to/models/directory
MODEL_DIR_PATH=model-subdirectory-name
LOG_LEVEL=DEBUG  # For debug output
```

## Testing
Run the validation test:
```bash
python test_model_validation_simple.py
```

This displays the current configuration without importing the heavy mlx library.

## Expected Behavior After Fix

1. **Server startup**: Backend logs clear validation report showing:
   - Configured model directory
   - Full model path
   - Validation result (✓ or ✗)

2. **Model listing**: `/v1/models` endpoint returns the actual configured model name

3. **Inference requests**: Detailed logs show when model is being loaded and any errors

4. **On error**: Clear error messages indicate exactly what's wrong (missing env var, directory not found, etc.)
