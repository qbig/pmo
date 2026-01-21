#!/usr/bin/env python3
"""Simple validation script to check project structure."""

import sys
from pathlib import Path

def validate_structure():
    """Validate project structure exists."""
    project_root = Path(__file__).parent
    errors = []
    warnings = []
    
    # Required directories
    required_dirs = [
        "workspace/projects",
        "workspace/risks",
        "workspace/decisions",
        "workspace/epics",
        "workspace/meetings",
        "workspace/people",
        "workspace/logs",
        "src/backend",
        "src/frontend",
        "specs",
    ]
    
    # Required files
    required_files = [
        "src/backend/main.py",
        "src/backend/config.py",
        "src/backend/indexer.py",
        "src/backend/api.py",
        "src/frontend/package.json",
        "src/frontend/vite.config.js",
        "specs/file-schemas.md",
        "README.md",
        "ralph/PRD.md",
    ]
    
    print("Validating project structure...")
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            errors.append(f"Missing directory: {dir_path}")
        else:
            print(f"✓ {dir_path}")
    
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists():
            errors.append(f"Missing file: {file_path}")
        else:
            print(f"✓ {file_path}")
    
    # Check example files
    example_files = [
        "workspace/projects/proj-alpha.md",
        "workspace/risks/risk-vendor-delay.md",
        "workspace/decisions/dec-use-postgres.md",
    ]
    
    for file_path in example_files:
        full_path = project_root / file_path
        if not full_path.exists():
            warnings.append(f"Example file missing: {file_path}")
        else:
            print(f"✓ {file_path} (example)")
    
    print("\n" + "="*50)
    if errors:
        print(f"❌ Found {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Project structure is valid!")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        return True

if __name__ == "__main__":
    success = validate_structure()
    sys.exit(0 if success else 1)
