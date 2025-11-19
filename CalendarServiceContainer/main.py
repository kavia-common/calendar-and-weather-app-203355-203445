"""
FastAPI entrypoint for uvicorn.

This top-level main.py enables launching the app via:
    uvicorn main:app --host 0.0.0.0 --port 3001 --reload

It imports the FastAPI app instance constructed in src.api.main.
The app will be available at http://localhost:3001 and OpenAPI docs at /docs.
"""

import sys
import os

# Ensure './src' is always on sys.path before imports, for uvicorn or direct python execution.
src_abspath = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if src_abspath not in sys.path:
    sys.path.insert(0, src_abspath)

from src.api.main import app  # PUBLIC_INTERFACE

__all__ = ["app"]  # Ensures 'app' is visible as a module attribute for uvicorn and silences unused import lint.

# No additional setup is needed; configuration (middleware, routers, etc.) is all in src.api.main.
