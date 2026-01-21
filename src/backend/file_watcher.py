"""File watching for markdown workspace."""

import asyncio
import logging
from pathlib import Path
from typing import Optional

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from .indexer import Indexer
from .config import Config

logger = logging.getLogger(__name__)


class MarkdownHandler(FileSystemEventHandler):
    """Handle markdown file changes."""
    
    def __init__(self, indexer: Indexer, workspace_root: Path, event_loop: Optional[asyncio.AbstractEventLoop] = None):
        self.indexer = indexer
        self.workspace_root = workspace_root
        self.event_loop = event_loop
    
    def _schedule_async(self, coro):
        """Schedule async task safely."""
        if self.event_loop and self.event_loop.is_running():
            asyncio.run_coroutine_threadsafe(coro, self.event_loop)
        else:
            # Fallback: run in new event loop (not ideal but works)
            asyncio.create_task(coro)
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if path.suffix == ".md":
            logger.info(f"File modified: {path}")
            self._schedule_async(self.indexer.index_file(path))
    
    def on_created(self, event: FileSystemEvent):
        """Handle file creation."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if path.suffix == ".md":
            logger.info(f"File created: {path}")
            self._schedule_async(self.indexer.index_file(path))
    
    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if path.suffix == ".md":
            logger.info(f"File deleted: {path}")
            self._schedule_async(self.indexer.remove_file(path))


class FileWatcher:
    """Watch workspace for markdown file changes."""
    
    def __init__(self, config: Config, indexer: Indexer, event_loop: Optional[asyncio.AbstractEventLoop] = None):
        self.config = config
        self.indexer = indexer
        self.observer: Optional[Observer] = None
        self.handler = MarkdownHandler(indexer, config.workspace_root, event_loop)
    
    def start(self):
        """Start watching the workspace."""
        self.observer = Observer()
        self.observer.schedule(
            self.handler,
            str(self.config.workspace_root),
            recursive=True
        )
        self.observer.start()
        logger.info(f"Started watching {self.config.workspace_root}")
    
    def stop(self):
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped file watcher")
