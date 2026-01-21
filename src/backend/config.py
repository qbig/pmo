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
        provider = os.getenv("PMO_LLM_PROVIDER", "gemini").strip().lower()
        self.llm_provider = provider
        default_model = "gemini-2.0-flash" if provider == "gemini" else "llama2"
        self.llm_model = os.getenv("PMO_LLM_MODEL", default_model)
        default_base_url = (
            "https://generativelanguage.googleapis.com"
            if provider == "gemini"
            else "http://localhost:11434"
        )
        self.llm_base_url = os.getenv("PMO_LLM_BASE_URL", default_base_url)
        self.llm_api_key = os.getenv("PMO_LLM_API_KEY")
        
        # Embedding model
        self.embedding_model = os.getenv("PMO_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        
        # Server configuration
        self.host = os.getenv("PMO_HOST", "127.0.0.1")
        self.port = int(os.getenv("PMO_PORT", "8000"))
