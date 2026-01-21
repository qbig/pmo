#!/usr/bin/env python3
"""
PMO Assistant Backend Daemon

Local-first backend that watches markdown files, indexes them, and provides
AI-powered PMO capabilities via HTTP API.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .file_watcher import FileWatcher
from .indexer import Indexer, set_semantic_search as set_indexer_semantic_search
from .ai.engine import AIEngine
from .api import router, set_indexer, set_ai_engine, set_semantic_search

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="PMO Assistant API", version="0.1.0")

# CORS for local web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Global state
config: Optional[Config] = None
file_watcher: Optional[FileWatcher] = None
indexer: Optional[Indexer] = None
ai_engine: Optional[AIEngine] = None


@app.on_event("startup")
async def startup_event():
    """Initialize file watcher and indexer on startup."""
    global config, file_watcher, indexer
    
    config = Config()
    logger.info(f"Starting PMO Assistant backend")
    logger.info(f"Workspace: {config.workspace_root}")
    logger.info(f"Database: {config.database_path}")
    
    # Initialize indexer
    indexer = Indexer(config)
    await indexer.initialize()
    set_indexer(indexer)  # Make available to API routes
    
    # Initialize semantic search (optional)
    try:
        from .ai.embeddings import EmbeddingModel, SemanticSearch
        embedding_model = EmbeddingModel(config.embedding_model)
        if embedding_model.model:
            semantic_search = SemanticSearch(embedding_model)
            set_semantic_search(semantic_search)
            set_indexer_semantic_search(semantic_search)  # Connect to indexer
            logger.info("Semantic search initialized")
        else:
            logger.warning("Semantic search not available (install sentence-transformers)")
    except Exception as e:
        logger.warning(f"Semantic search initialization failed: {e}")
    
    # Initialize AI engine
    ai_engine = AIEngine(config, indexer)
    set_ai_engine(ai_engine)  # Make available to API routes
    logger.info("AI engine initialized")
    
    # Initial index of existing files
    logger.info("Indexing existing files...")
    await indexer.index_workspace()
    
    # Start file watcher (pass event loop for async operations)
    import asyncio
    event_loop = asyncio.get_event_loop()
    file_watcher = FileWatcher(config, indexer, event_loop)
    file_watcher.start()
    logger.info("File watcher started")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global file_watcher, indexer
    
    if file_watcher:
        file_watcher.stop()
        logger.info("File watcher stopped")
    
    if indexer:
        await indexer.close()
        logger.info("Indexer closed")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "workspace": str(config.workspace_root) if config else None,
        "indexed_files": indexer.count() if indexer else 0
    }


def main():
    """Main entry point."""
    port = int(os.getenv("PMO_PORT", "8000"))
    host = os.getenv("PMO_HOST", "127.0.0.1")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
