#!/usr/bin/env python3
"""
Memory Entry Point

Run the memory engine from command line:
    python -m memory          # Show memory status
    python -m memory init     # Initialize tier structure
    python -m memory search "..."  # Search memory
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory.initialize import main as init_main


def show_status():
    """Show current memory tier status."""
    memory_root = Path("memory")

    tiers = ["session", "agent", "department", "global"]

    print("VJSOS-AI Memory Tier Status")
    print("=" * 40)

    for tier in tiers:
        tier_path = memory_root / tier
        if tier_path.exists():
            entry_count = len(list(tier_path.glob("**/*.json")))
            print(f"  {tier}: {entry_count} entries")
        else:
            print(f"  {tier}: not initialized")

    print("\nRun 'python -m memory init' to initialize tiers.")


def main():
    """Memory entry point."""
    args = sys.argv[1:]

    if not args:
        show_status()
    elif args[0] == "init":
        init_main()
    elif args[0] == "search":
        query = " ".join(args[1:])
        if not query:
            print("Usage: python -m memory search <query>")
            sys.exit(1)
        print(f"Searching memory for: {query}")
        # Placeholder for search functionality
        print("Search not yet implemented in Phase 1")
    else:
        print(f"Unknown command: {args[0]}")
        print("Usage: python -m memory [init|search]")
        sys.exit(1)


if __name__ == "__main__":
    main()