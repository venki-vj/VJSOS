#!/usr/bin/env python3
"""
Kernel Entry Point

Run the VJSOS-AI kernel components from command line:
    python -m kernel          # Run health check
    python -m kernel serve    # Start orchestrator server
    python -m kernel dispatch --task "..." --department engineering
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kernel.health_check import main as health_check_main


def main():
    """Kernel entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ("health", "check"):
        # Default: run health check
        health_check_main()
    elif args[0] == "serve":
        print("Starting VJSOS-AI Kernel...")
        print("Orchestrator server not yet implemented in Phase 1")
        sys.exit(1)
    elif args[0] == "dispatch":
        print("Task dispatch requires orchestrator. Use: python -m kernel.orchestrator dispatch ...")
        sys.exit(1)
    else:
        print(f"Unknown command: {args[0]}")
        print("Usage: python -m kernel [health|check|serve]")
        sys.exit(1)


if __name__ == "__main__":
    main()