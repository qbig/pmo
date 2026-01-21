"""Basic end-to-end tests for PMO Assistant."""

import asyncio
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config import Config
from src.backend.indexer import Indexer
from src.backend.models import parse_file_type, FileType


def test_file_type_parsing():
    """Test file type parsing from paths."""
    workspace = Path("/tmp/test_workspace")
    
    test_cases = [
        (workspace / "projects" / "test.md", FileType.PROJECT),
        (workspace / "risks" / "test.md", FileType.RISK),
        (workspace / "decisions" / "test.md", FileType.DECISION),
        (workspace / "unknown" / "test.md", FileType.UNKNOWN),
    ]
    
    for file_path, expected_type in test_cases:
        result = parse_file_type(file_path, workspace)
        assert result == expected_type, f"Expected {expected_type}, got {result} for {file_path}"
    
    print("✓ File type parsing tests passed")


async def test_indexer():
    """Test indexer functionality."""
    # Create temporary workspace
    temp_dir = tempfile.mkdtemp()
    workspace = Path(temp_dir) / "workspace"
    workspace.mkdir()
    
    # Create test directories
    (workspace / "projects").mkdir()
    (workspace / "risks").mkdir()
    
    try:
        # Create test project file
        project_file = workspace / "projects" / "proj-test.md"
        project_file.write_text("""---
id: proj-test
owner: test-user
status: active
---

# Test Project

## Goal
Test the system.

## Current Status
🟢 On track
""")
        
        # Create test risk file
        risk_file = workspace / "risks" / "risk-test.md"
        risk_file.write_text("""---
id: risk:test
severity: high
probability: medium
owner: test-user
status: open
---

# Test Risk

## Description
This is a test risk.
""")
        
        # Initialize indexer
        config = Config(workspace_root=workspace)
        indexer = Indexer(config)
        await indexer.initialize()
        
        # Index workspace
        await indexer.index_workspace()
        
        # Verify files are indexed
        assert indexer.count() == 2, f"Expected 2 files, got {indexer.count()}"
        
        # Get project
        project = indexer.get_file("proj-test")
        assert project is not None, "Project not found"
        assert project["file_type"] == "project", "Wrong file type"
        assert project["title"] == "Test Project", "Wrong title"
        
        # Get risk
        risk = indexer.get_file("risk:test")
        assert risk is not None, "Risk not found"
        assert risk["file_type"] == "risk", "Wrong file type"
        
        # List files by type
        projects = indexer.list_files(file_type="project")
        assert len(projects) == 1, "Should have 1 project"
        
        risks = indexer.list_files(file_type="risk")
        assert len(risks) == 1, "Should have 1 risk"
        
        # Test file update
        project_file.write_text("""---
id: proj-test
owner: test-user
status: active
---

# Updated Test Project

## Goal
Test the system update.
""")
        await indexer.index_file(project_file)
        
        updated_project = indexer.get_file("proj-test")
        assert "Updated Test Project" in updated_project["content"], "Update not reflected"
        
        # Test file deletion
        await indexer.remove_file(risk_file)
        assert indexer.count() == 1, "Should have 1 file after deletion"
        
        await indexer.close()
        print("✓ Indexer tests passed")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_diff_generation():
    """Test diff generation."""
    from src.backend.diff import DiffGenerator, DiffSummary
    import sys
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    original = """Line 1
Line 2
Line 3"""
    
    updated = """Line 1
Line 2 Modified
Line 3
Line 4"""
    
    # Test unified diff
    unified = DiffGenerator.generate_unified_diff(original, updated, "test.md")
    assert "Line 2" in unified, "Unified diff should contain changes"
    
    # Test hunk list
    hunks = DiffGenerator.generate_hunk_list(original, updated)
    assert len(hunks) > 0, "Should have hunks"
    
    # Test summary
    summary = DiffSummary(original, updated)
    assert summary.added_lines > 0, "Should have added lines"
    assert summary.total_changes > 0, "Should have changes"
    
    print("✓ Diff generation tests passed")


async def run_tests():
    """Run all tests."""
    print("Running basic end-to-end tests...\n")
    
    try:
        test_file_type_parsing()
        await test_indexer()
        test_diff_generation()
        
        print("\n✅ All tests passed!")
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)
