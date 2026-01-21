"""Diff and patch system for AI file edits."""

import difflib
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DiffGenerator:
    """Generate diffs between file versions."""
    
    @staticmethod
    def generate_unified_diff(
        original: str,
        updated: str,
        filename: str = "file.md",
        context_lines: int = 3
    ) -> str:
        """
        Generate unified diff between original and updated content.
        
        Args:
            original: Original file content
            updated: Updated file content
            filename: Filename for diff header
            context_lines: Number of context lines
            
        Returns:
            Unified diff string
        """
        original_lines = original.splitlines(keepends=True)
        updated_lines = updated.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            original_lines,
            updated_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm="",
            n=context_lines
        )
        
        return "".join(diff)
    
    @staticmethod
    def generate_hunk_list(
        original: str,
        updated: str
    ) -> List[Dict[str, any]]:
        """
        Generate structured list of hunks (changes).
        
        Args:
            original: Original file content
            updated: Updated file content
            
        Returns:
            List of hunk dictionaries with line numbers and changes
        """
        original_lines = original.splitlines()
        updated_lines = updated.splitlines()
        
        matcher = difflib.SequenceMatcher(None, original_lines, updated_lines)
        hunks = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                continue
            
            hunk = {
                "type": tag,  # replace, delete, insert
                "original_start": i1 + 1,  # 1-indexed
                "original_end": i2,
                "original_lines": original_lines[i1:i2] if tag != "insert" else [],
                "updated_start": j1 + 1,  # 1-indexed
                "updated_end": j2,
                "updated_lines": updated_lines[j1:j2] if tag != "delete" else [],
            }
            hunks.append(hunk)
        
        return hunks
    
    @staticmethod
    def generate_side_by_side_diff(
        original: str,
        updated: str,
        context_lines: int = 3
    ) -> List[Dict[str, any]]:
        """
        Generate side-by-side diff for UI display.
        
        Args:
            original: Original file content
            updated: Updated file content
            context_lines: Number of context lines around changes
            
        Returns:
            List of line dictionaries with original/updated content
        """
        original_lines = original.splitlines()
        updated_lines = updated.splitlines()
        
        matcher = difflib.SequenceMatcher(None, original_lines, updated_lines)
        result = []
        line_num = 1
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                # Add context lines
                for k in range(i1, i2):
                    result.append({
                        "line_num": line_num,
                        "type": "equal",
                        "original": original_lines[k],
                        "updated": updated_lines[k - i1 + j1] if k - i1 + j1 < len(updated_lines) else "",
                    })
                    line_num += 1
            elif tag == "replace":
                # Show deleted lines
                for k in range(i1, i2):
                    result.append({
                        "line_num": line_num,
                        "type": "delete",
                        "original": original_lines[k],
                        "updated": "",
                    })
                    line_num += 1
                # Show inserted lines
                for k in range(j1, j2):
                    result.append({
                        "line_num": line_num,
                        "type": "insert",
                        "original": "",
                        "updated": updated_lines[k],
                    })
                    line_num += 1
            elif tag == "delete":
                for k in range(i1, i2):
                    result.append({
                        "line_num": line_num,
                        "type": "delete",
                        "original": original_lines[k],
                        "updated": "",
                    })
                    line_num += 1
            elif tag == "insert":
                for k in range(j1, j2):
                    result.append({
                        "line_num": line_num,
                        "type": "insert",
                        "original": "",
                        "updated": updated_lines[k],
                    })
                    line_num += 1
        
        return result


class PatchApplier:
    """Apply patches to files."""
    
    @staticmethod
    def apply_patch(
        file_path: Path,
        updated_content: str,
        backup: bool = True
    ) -> bool:
        """
        Apply updated content to a file.
        
        Args:
            file_path: Path to file
            updated_content: New file content
            backup: Whether to create backup
            
        Returns:
            True if successful
        """
        try:
            # Create backup if requested
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + ".bak")
                if file_path.exists():
                    file_path.rename(backup_path)
                    logger.info(f"Created backup: {backup_path}")
            
            # Write updated content
            file_path.write_text(updated_content, encoding="utf-8")
            logger.info(f"Applied patch to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error applying patch to {file_path}: {e}")
            return False
    
    @staticmethod
    def restore_backup(file_path: Path) -> bool:
        """
        Restore file from backup.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if successful
        """
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        
        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_path}")
            return False
        
        try:
            backup_path.rename(file_path)
            logger.info(f"Restored from backup: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False


class DiffSummary:
    """Summary of changes in a diff."""
    
    def __init__(self, original: str, updated: str):
        self.original = original
        self.updated = updated
        self._analyze()
    
    def _analyze(self):
        """Analyze the diff and generate summary."""
        original_lines = self.original.splitlines()
        updated_lines = self.updated.splitlines()
        
        matcher = difflib.SequenceMatcher(None, original_lines, updated_lines)
        
        self.added_lines = 0
        self.deleted_lines = 0
        self.modified_lines = 0
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "insert":
                self.added_lines += (j2 - j1)
            elif tag == "delete":
                self.deleted_lines += (i2 - i1)
            elif tag == "replace":
                self.modified_lines += min(i2 - i1, j2 - j1)
                if (i2 - i1) > (j2 - j1):
                    self.deleted_lines += (i2 - i1) - (j2 - j1)
                elif (j2 - j1) > (i2 - i1):
                    self.added_lines += (j2 - j1) - (i2 - i1)
        
        self.total_changes = self.added_lines + self.deleted_lines + self.modified_lines
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            "added_lines": self.added_lines,
            "deleted_lines": self.deleted_lines,
            "modified_lines": self.modified_lines,
            "total_changes": self.total_changes,
        }
