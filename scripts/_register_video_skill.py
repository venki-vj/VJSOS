#!/usr/bin/env python3
"""One-shot registration + test runner for the video_production skill.

Bypasses CLI indirection so we can validate the skill end-to-end:
1. Register skills/video_production/binder/skill.md
2. List skills in media domain
3. Run the skill's test suite

Usage: python scripts/_register_video_skill.py [register|test|list]
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from skills.registry import SkillRegistry  # noqa: E402


def main() -> int:
    # register_skill() expects the package DIRECTORY (it looks for binder/skill.md inside)
    skill_dir = Path(__file__).resolve().parent.parent / "skills" / "video_production"

    if "test" in sys.argv:
        registry = SkillRegistry(skills_root="skills")
        entry = registry.get_skill("video_production")
        print("Loaded:", None if entry is None else entry.manifest.skill_id)
        if entry is None:
            print("Skill not registered yet — run: python scripts/_register_video_skill.py register")
            return 1
        result = registry.run_tests("video_production")
        print(json.dumps(result, indent=2, default=str))
        return 0

    # default: register + list
    registry = SkillRegistry(skills_root="skills")
    result = registry.register_skill(str(skill_dir))
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())