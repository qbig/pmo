"""SQLite-based indexer for markdown files."""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

import frontmatter
from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .config import Config
from .models import FileType, parse_file_type

logger = logging.getLogger(__name__)

# Optional semantic search
_semantic_search = None

def set_semantic_search(search_instance):
    """Set semantic search instance for indexing."""
    global _semantic_search
    _semantic_search = search_instance

Base = declarative_base()


class FileIndex(Base):
    """SQLite table for file index."""
    
    __tablename__ = "files"
    
    id = Column(String, primary_key=True)  # File ID from frontmatter
    path = Column(String, unique=True, nullable=False)
    file_type = Column(String, nullable=False)  # project, risk, decision, etc.
    title = Column(String)
    owner = Column(String)
    status = Column(String)
    content = Column(Text)  # Full markdown content
    frontmatter = Column(JSON)  # Parsed frontmatter as JSON
    indexed_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Indexer:
    """Index markdown files in workspace."""
    
    def __init__(self, config: Config):
        self.config = config
        self.engine = create_engine(
            f"sqlite:///{config.database_path}",
            echo=False
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._lock = asyncio.Lock()
    
    async def initialize(self):
        """Initialize database schema."""
        Base.metadata.create_all(self.engine)
        logger.info("Database initialized")
    
    async def close(self):
        """Close database connections."""
        self.engine.dispose()
    
    def count(self) -> int:
        """Get count of indexed files."""
        session = self.SessionLocal()
        try:
            return session.query(FileIndex).count()
        finally:
            session.close()
    
    async def index_workspace(self):
        """Index all markdown files in workspace."""
        async with self._lock:
            workspace = self.config.workspace_root
            md_files = list(workspace.rglob("*.md"))
            
            logger.info(f"Found {len(md_files)} markdown files")
            
            for md_file in md_files:
                await self.index_file(md_file)
    
    async def index_file(self, file_path: Path):
        """Index a single markdown file."""
        async with self._lock:
            try:
                # Read file
                content = file_path.read_text(encoding="utf-8")
                
                # Parse frontmatter
                post = frontmatter.loads(content)
                metadata = post.metadata
                body = post.content
                
                # Determine file type from path
                file_type = parse_file_type(file_path, self.config.workspace_root)
                
                # Extract ID (from frontmatter or generate from path)
                file_id = metadata.get("id")
                if not file_id:
                    # Generate ID from relative path
                    rel_path = file_path.relative_to(self.config.workspace_root)
                    file_id = f"{file_type}:{rel_path.stem}"
                
                # Extract title (from frontmatter or first heading)
                title = metadata.get("title")
                if not title and body:
                    # Try to extract from first H1
                    lines = body.split("\n")
                    for line in lines:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            break
                
                if not title:
                    title = file_path.stem
                
                # Extract common fields
                owner = metadata.get("owner")
                status = metadata.get("status")
                
                # Store in database
                session = self.SessionLocal()
                try:
                    # Check if exists
                    existing = session.query(FileIndex).filter_by(path=str(file_path)).first()
                    
                    if existing:
                        # Update
                        existing.id = file_id
                        existing.file_type = file_type.value
                        existing.title = title
                        existing.owner = owner
                        existing.status = status
                        existing.content = content
                        existing.frontmatter = metadata
                        existing.updated_at = datetime.utcnow()
                    else:
                        # Insert
                        file_index = FileIndex(
                            id=file_id,
                            path=str(file_path),
                            file_type=file_type.value,
                            title=title,
                            owner=owner,
                            status=status,
                            content=content,
                            frontmatter=metadata,
                            indexed_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        session.add(file_index)
                    
                    session.commit()
                    logger.debug(f"Indexed: {file_path} ({file_type.value})")
                    
                    # Index for semantic search if available
                    if _semantic_search:
                        _semantic_search.index_file(file_id, content)
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error indexing {file_path}: {e}")
                finally:
                    session.close()
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
    
    async def remove_file(self, file_path: Path):
        """Remove file from index."""
        async with self._lock:
            session = self.SessionLocal()
            try:
                file_index = session.query(FileIndex).filter_by(path=str(file_path)).first()
                if file_index:
                    file_id = file_index.id
                    session.delete(file_index)
                    session.commit()
                    logger.info(f"Removed from index: {file_path}")
                    
                    # Remove from semantic search if available
                    if _semantic_search:
                        _semantic_search.remove_file(file_id)
            except Exception as e:
                session.rollback()
                logger.error(f"Error removing {file_path}: {e}")
            finally:
                session.close()
    
    def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file by ID."""
        session = self.SessionLocal()
        try:
            file_index = session.query(FileIndex).filter_by(id=file_id).first()
            if file_index:
                return {
                    "id": file_index.id,
                    "path": file_index.path,
                    "file_type": file_index.file_type,
                    "title": file_index.title,
                    "owner": file_index.owner,
                    "status": file_index.status,
                    "content": file_index.content,
                    "frontmatter": file_index.frontmatter,
                    "updated_at": file_index.updated_at.isoformat() if file_index.updated_at else None
                }
            return None
        finally:
            session.close()
    
    def list_files(self, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all files, optionally filtered by type."""
        session = self.SessionLocal()
        try:
            query = session.query(FileIndex)
            if file_type:
                query = query.filter_by(file_type=file_type)
            
            files = query.all()
            return [
                {
                    "id": f.id,
                    "path": f.path,
                    "file_type": f.file_type,
                    "title": f.title,
                    "owner": f.owner,
                    "status": f.status,
                    "updated_at": f.updated_at.isoformat() if f.updated_at else None
                }
                for f in files
            ]
        finally:
            session.close()
