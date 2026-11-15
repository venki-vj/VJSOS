#!/usr/bin/env python3
"""
Kernel Health Check

Verifies that all 5 kernel components are operational.
Returns HEALTHY status for each component or specific error details.
"""
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from typing import Dict, Any


def check_governor() -> Dict[str, Any]:
    """Check System Governor health."""
    try:
        from kernel.governor import SystemGovernor
        gov = SystemGovernor()
        return {"status": "HEALTHY", "component": "Governor", "details": "Governor initialized successfully"}
    except Exception as e:
        return {"status": "UNHEALTHY", "component": "Governor", "error": str(e)}


def check_orchestrator() -> Dict[str, Any]:
    """Check Orchestrator health."""
    try:
        from kernel.orchestrator import Orchestrator
        orch = Orchestrator()
        # Check that department/agent registries are initialized
        dept_count = len(orch.department_registry)
        agent_count = sum(len(agents) for agents in orch.agent_registry.values())
        details = f"{dept_count} departments, {agent_count} agents registered"
        status = "HEALTHY" if dept_count > 0 else "DEGRADED"
        return {"status": status, "component": "Orchestrator", "details": details}
    except Exception as e:
        return {"status": "UNHEALTHY", "component": "Orchestrator", "error": str(e)}


def check_context_engine() -> Dict[str, Any]:
    """Check Context Engine health."""
    try:
        from kernel.context_engine import ContextEngine
        ctx = ContextEngine(budget_tokens=8000)
        return {"status": "HEALTHY", "component": "Context Engine", "details": "Budget tokens initialized"}
    except Exception as e:
        return {"status": "UNHEALTHY", "component": "Context Engine", "error": str(e)}


def check_memory_engine() -> Dict[str, Any]:
    """Check Memory Engine health."""
    try:
        from kernel.memory_engine import MemoryEngine, MemoryTier
        mem = MemoryEngine()
        tier_names = [t.name for t in mem.storage_paths.keys()]
        return {"status": "HEALTHY", "component": "Memory Engine", "details": f"Tiers: {', '.join(tier_names)}"}
    except Exception as e:
        return {"status": "UNHEALTHY", "component": "Memory Engine", "error": str(e)}


def check_qa_engine() -> Dict[str, Any]:
    """Check QA Engine health."""
    try:
        from kernel.qa_engine import QAEngine
        qa = QAEngine()
        return {"status": "HEALTHY", "component": "QA Engine", "details": "QA rubric loaded"}
    except Exception as e:
        return {"status": "UNHEALTHY", "component": "QA Engine", "error": str(e)}


def run_health_check() -> Dict[str, Any]:
    """Run health check on all kernel components."""
    results = {
        "governor": check_governor(),
        "orchestrator": check_orchestrator(),
        "context_engine": check_context_engine(),
        "memory_engine": check_memory_engine(),
        "qa_engine": check_qa_engine()
    }

    all_healthy = all(r["status"] == "HEALTHY" for r in results.values())

    return {
        "overall_status": "HEALTHY" if all_healthy else "UNHEALTHY",
        "components": results,
        "healthy_count": sum(1 for r in results.values() if r["status"] == "HEALTHY"),
        "total_count": len(results)
    }


def main():
    """Run health check and print results."""
    result = run_health_check()

    if result["overall_status"] == "HEALTHY":
        print("✓ All 5 components report HEALTHY")
        for name, check in result["components"].items():
            print(f"  ✓ {check['component']}: {check['status']}")
    else:
        print("✗ Health check FAILED")
        for name, check in result["components"].items():
            status = "✓" if check["status"] == "HEALTHY" else "✗"
            print(f"  {status} {check['component']}: {check['status']}")
            if "error" in check:
                print(f"      Error: {check['error']}")

    print(f"\nHealthy: {result['healthy_count']}/{result['total_count']} components")

    # Return non-zero exit code if unhealthy
    sys.exit(0 if result["overall_status"] == "HEALTHY" else 1)


if __name__ == "__main__":
    main()