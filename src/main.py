# src/main.py
"""
Main FastAPI application setup.

This file:
1. Initializes the FastAPI app
2. Configures CORS
3. Registers all API route modules
4. Initializes the Qdrant vector collection at startup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.products import router as products_router
from src.api.routes.search import router as search_router
from src.api.routes.semantic import router as semantic_router
from src.services.vector_service import init_qdrant_collection


# ------------------------------------------------------------
# FastAPI Application Initialization
# ------------------------------------------------------------
app = FastAPI(title="Contextual Search Platform")


# ------------------------------------------------------------
# CORS Middleware (Allows Frontend to Access API)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins (safe for dev mode)
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------
# API Route Registration
# ------------------------------------------------------------
app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(search_router, prefix="/api/v1/search", tags=["Search"])
app.include_router(semantic_router, prefix="/api/v1/search", tags=["Semantic Search"])


# ------------------------------------------------------------
# Startup Event — Ensure Qdrant Collection Exists
# ------------------------------------------------------------
@app.on_event("startup")
def startup_event():
    """
    Called automatically when the server starts.

    Ensures Qdrant collection is created before
    any ingestion or search requests are made.
    """
    init_qdrant_collection()
