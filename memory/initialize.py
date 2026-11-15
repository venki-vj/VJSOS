#!/usr/bin/env python3
"""
Memory Engine Initialization

Creates the 4-tier memory directory structure and initializes:
- Tier 4 (Global) - Governor scope, infinite TTL
- Tier 3 (Department) - Department scope, infinite TTL
- Tier 2 (Agent) - Agent scope, 180d TTL
- Tier 1 (Session) - Session scope, 24h TTL
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from typing import Dict, Any
from datetime import datetime, timezone


def _now() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def create_directory_structure(memory_root: Path) -> None:
    """Create the 4-tier directory structure."""
    tiers = {
        "session": {"ttl": "24h", "scope": "agent"},
        "agent": {"ttl": "180d", "scope": "agent"},
        "department": {"ttl": "infinite", "scope": "department"},
        "global": {"ttl": "infinite", "scope": "governor"}
    }

    for tier_name, metadata in tiers.items():
        tier_path = memory_root / tier_name
        tier_path.mkdir(parents=True, exist_ok=True)

        # Create a README.md for each tier
        readme = f"""# {tier_name.title()} Memory Tier

**TTL:** {metadata['ttl']}
**Scope:** {metadata['scope']}
**Created:** {_now()}

## Purpose
This tier stores memory entries that persist for the specified TTL and scope.

## Structure
- Keys are UUID-based identifiers
- Each entry is a JSON file with metadata and content
- Deduplication uses semantic similarity threshold (0.95)

## Access
- **Session** tier: Agent-scoped, auto-purged after 24h
- **Agent** tier: Agent-scoped, purged after 180 days of inactivity
- **Department** tier: Department-scoped, requires director approval
- **Global** tier: Governor-scoped, requires Governor approval for modifications
"""
        (tier_path / "README.md").write_text(readme)


def initialize_global_memory(memory_root: Path) -> None:
    """Initialize Tier 4 (Global) memory with system knowledge."""
    global_path = memory_root / "global"

    # System knowledge base
    knowledge_base = {
        "version": "1.0.0",
        "initialized_at": _now(),
        "knowledge_entries": []
    }

    kb_path = global_path / "knowledge_base.json"
    if not kb_path.exists():
        kb_path.write_text(json.dumps(knowledge_base, indent=2))


def initialize_department_memory(memory_root: Path) -> None:
    """Initialize Tier 3 (Department) memory structure."""
    department_path = memory_root / "department"

    # Read department list from docs/DEPARTMENTS.md or use defaults
    departments = [
        "engineering", "media", "business", "research", "animation",
        "operations", "knowledge", "infrastructure", "improvement"
    ]

    for dept in departments:
        dept_path = department_path / dept
        dept_path.mkdir(parents=True, exist_ok=True)

        # Create empty sessions index
        sessions = {
            "version": "1.0.0",
            "initialized_at": _now(),
            "department": dept,
            "sessions": []
        }
        (dept_path / "sessions.json").write_text(json.dumps(sessions, indent=2))


def main():
    """Run memory initialization."""
    memory_root = Path("memory")
    memory_root.mkdir(parents=True, exist_ok=True)

    print("Initializing VJSOS-AI Memory Engine...")

    print("✓ Creating 4-tier directory structure")
    create_directory_structure(memory_root)

    print("✓ Initializing Global tier (Tier 4)")
    initialize_global_memory(memory_root)

    print("✓ Initializing Department tier (Tier 3)")
    initialize_department_memory(memory_root)

    print("\nMemory tiers ready:")
    for tier in ["session", "agent", "department", "global"]:
        tier_path = memory_root / tier
        if tier_path.exists():
            print(f"  ✓ {tier}/ - exists")
        else:
            print(f"  ✗ {tier}/ - MISSING")

    print("\n✓ Memory Engine initialization complete")


if __name__ == "__main__":
    main()