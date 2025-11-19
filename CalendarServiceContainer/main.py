"""
FastAPI entrypoint for uvicorn.

This top-level main.py enables launching the app via:
    uvicorn main:app --host 0.0.0.0 --port 3001 --reload

It imports the FastAPI app instance constructed in src.api.main.
The app will be available at http://localhost:3001 and OpenAPI docs at /docs.
"""

from src.api.main import app  # PUBLIC_INTERFACE

__all__ = ["app"]  # Ensures 'app' is visible as a module attribute for uvicorn and silences unused import lint.

# No additional setup is needed; configuration (middleware, routers, etc.) is all in src.api.main.
