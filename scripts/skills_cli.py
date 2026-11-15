#!/usr/bin/env python3
"""
Skill CLI - Command Line Interface for Skill Registry

Commands:
    skills register <skill_path>   - Register a skill from a skill.md manifest
    skills list [--domain DOMAIN]  - List registered skills
    skills test <skill_id>         - Run tests for a skill
    skills get <skill_id>          - Get skill details
    skills prompt <skill_id>       - Render skill prompt with variables
    skills unregister <skill_id>   - Unregister a skill
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Unicode glyphs (✓/✗/⚠) crash on Windows cp1252 consoles unless stdout is UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:  # Python < 3.7
    pass

from skills.registry import SkillRegistry
from skills.skill_loader import SkillLoader
from skills.skill_tester import SkillTester


def cmd_register(args):
    """Register a skill from a skill.md manifest."""
    registry = SkillRegistry(skills_root=args.skills_root)
    result = registry.register_skill(args.skill_path)
    if result.get("success"):
        # register_skill returns {success, skill_key, manifest, message}, not skill_id/version
        manifest = result.get("manifest", {})
        print(f"✓ Registered: {manifest.get('skill_id', result.get('skill_key', '?'))} "
              f"v{manifest.get('version', '?')}")
        if result.get("warnings"):
            for w in result["warnings"]:
                print(f"  ⚠ {w}")
    else:
        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


def cmd_list(args):
    """List registered skills."""
    registry = SkillRegistry(skills_root=args.skills_root)
    skills = registry.list_skills(domain=args.domain, type_=args.type)

    if args.json:
        print(json.dumps(skills, indent=2))
        return

    if not skills:
        print("No skills found")
        return

    for skill in skills:
        status = skill.get("qa_status", "unknown")
        status_icon = "✓" if status == "verified" else "✗" if status == "failed" else "?"
        print(f"{status_icon} {skill['skill_id']} v{skill['version']} ({skill['type']}) - {skill['domain']}")
        print(f"    {skill.get('description', '')[:80]}")


def cmd_test(args):
    """Run tests for a skill."""
    registry = SkillRegistry(skills_root=args.skills_root)
    loader = SkillLoader(registry)
    tester = SkillTester(registry, loader)

    # Ensure skill is loaded
    loader.load_skill(args.skill_id)

    result = tester.run_tests(args.skill_id)
    print(tester.get_test_summary(result))

    if args.json:
        from skills.skill_tester import TestSuiteResult
        print(json.dumps({
            "skill_id": result.skill_id,
            "total": result.total,
            "passed": result.passed,
            "failed": result.failed,
            "errors": result.errors,
            "skipped": result.skipped,
            "duration_ms": result.duration_ms,
            "qa_status": result.qa_status.value,
            "test_cases": [tc.__dict__ for tc in result.test_cases]
        }, indent=2, default=str))

    if result.qa_status.value != "verified":
        sys.exit(1)


def cmd_get(args):
    """Get skill details."""
    registry = SkillRegistry(skills_root=args.skills_root)
    entry = registry.get_skill(args.skill_id, args.version)
    if not entry:
        print(f"Skill not found: {args.skill_id}")
        sys.exit(1)

    data = {
        "skill_id": entry.skill_id,
        "version": entry.version,
        "manifest": entry.manifest.__dict__,
        "qa_status": entry.qa_status.value,
        "path": entry.path
    }
    print(json.dumps(data, indent=2, default=str))


def cmd_prompt(args):
    """Render a skill's prompt with variables."""
    registry = SkillRegistry(skills_root=args.skills_root)
    loader = SkillLoader(registry)

    skill = loader.load_skill(args.skill_id)
    if not skill:
        print(f"Skill not found: {args.skill_id}")
        sys.exit(1)

    variables = {}
    if args.variables:
        for var in args.variables:
            if "=" in var:
                k, v = var.split("=", 1)
                variables[k] = v

    prompt = skill.render_prompt(variables)
    if args.variables:
        print(f"Variables: {variables}")
    print(prompt)


def cmd_unregister(args):
    """Unregister a skill."""
    registry = SkillRegistry(skills_root=args.skills_root)
    result = registry.unregister_skill(args.skill_id, args.version)
    if result.get("success"):
        print(f"✓ Unregistered: {args.skill_id} v{args.version}")
    else:
        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="skills",
        description="VJSOS Skill Registry CLI"
    )
    parser.add_argument("--skills-root", default="skills", help="Skills root directory")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # register
    p_register = subparsers.add_parser("register", help="Register a skill")
    p_register.add_argument("skill_path", help="Path to skill.md or skill directory")
    p_register.set_defaults(func=cmd_register)

    # list
    p_list = subparsers.add_parser("list", help="List registered skills")
    p_list.add_argument("--domain", help="Filter by domain")
    p_list.add_argument("--type", help="Filter by type")
    p_list.set_defaults(func=cmd_list)

    # test
    p_test = subparsers.add_parser("test", help="Run tests for a skill")
    p_test.add_argument("skill_id", help="Skill ID to test")
    p_test.set_defaults(func=cmd_test)

    # get
    p_get = subparsers.add_parser("get", help="Get skill details")
    p_get.add_argument("skill_id", help="Skill ID")
    p_get.add_argument("--version", help="Specific version")
    p_get.set_defaults(func=cmd_get)

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="Render skill prompt")
    p_prompt.add_argument("skill_id", help="Skill ID")
    p_prompt.add_argument("variables", nargs="*", help="Prompt variables (KEY=VALUE)")
    p_prompt.set_defaults(func=cmd_prompt)

    # unregister
    p_unregister = subparsers.add_parser("unregister", help="Unregister a skill")
    p_unregister.add_argument("skill_id", help="Skill ID")
    p_unregister.add_argument("version", help="Version to unregister")
    p_unregister.set_defaults(func=cmd_unregister)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()