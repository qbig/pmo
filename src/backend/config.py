"""Configuration management."""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize configuration.
        
        Args:
            workspace_root: Path to workspace directory. Defaults to ./workspace
        """
        # Determine project root (parent of src/)
        project_root = Path(__file__).parent.parent.parent
        
        # Workspace root
        if workspace_root is None:
            workspace_root = project_root / "workspace"
        self.workspace_root = Path(workspace_root).resolve()
        
        # Ensure workspace exists
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        
        # Database path (in workspace for easy backup)
        self.database_path = self.workspace_root / ".pmo.db"
        
        # LLM configuration
        self.llm_provider = os.getenv("PMO_LLM_PROVIDER", "ollama")
        self.llm_model = os.getenv("PMO_LLM_MODEL", "llama2")
        self.llm_base_url = os.getenv("PMO_LLM_BASE_URL", "http://localhost:11434")
        
        # Embedding model
        self.embedding_model = os.getenv("PMO_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        
        # Server configuration
        self.host = os.getenv("PMO_HOST", "127.0.0.1")
        self.port = int(os.getenv("PMO_PORT", "8000"))
