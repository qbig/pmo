"""Data models for PMO file types."""

from enum import Enum
from pathlib import Path


class FileType(Enum):
    """File type enumeration."""
    PROJECT = "project"
    EPIC = "epic"
    DECISION = "decision"
    RISK = "risk"
    MEETING = "meeting"
    PERSON = "person"
    LOG = "log"
    UNKNOWN = "unknown"


def parse_file_type(file_path: Path, workspace_root: Path) -> FileType:
    """
    Determine file type from path.
    
    Args:
        file_path: Absolute path to file
        workspace_root: Workspace root directory
        
    Returns:
        FileType enum value
    """
    try:
        rel_path = file_path.relative_to(workspace_root)
        parts = rel_path.parts
        
        if len(parts) == 0:
            return FileType.UNKNOWN
        
        # First directory determines type
        directory = parts[0]
        
        type_map = {
            "projects": FileType.PROJECT,
            "epics": FileType.EPIC,
            "decisions": FileType.DECISION,
            "risks": FileType.RISK,
            "meetings": FileType.MEETING,
            "people": FileType.PERSON,
            "logs": FileType.LOG,
        }
        
        return type_map.get(directory, FileType.UNKNOWN)
    except ValueError:
        # File not in workspace
        return FileType.UNKNOWN
