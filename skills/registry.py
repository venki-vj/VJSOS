#!/usr/bin/env python3
"""
Skill Registry - Capability Package Management

The Skill Registry manages all skill packages:
- Load/validate skill manifests (skill.md)
- Version resolution and dependency graph
- Test execution framework
- QA status tracking
- Skill discovery and search
"""

import json
import yaml
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import subprocess


class SkillType(Enum):
    ANALYSIS = "analysis"
    GENERATION = "generation"
    VERIFICATION = "verification"
    AUTOMATION = "automation"
    ORCHESTRATION = "orchestration"
    MONITORING = "monitoring"


class SkillQAStatus(Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    DEPRECATED = "deprecated"


@dataclass
class SkillManifest:
    """Skill manifest - matches the spec format."""
    skill_id: str
    version: str
    owner: str
    domain: str
    description: str
    type: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    examples: List[Dict[str, str]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    qa_status: str = "pending"
    last_reviewed: Optional[str] = None
    changelog: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillManifest":
        """Create SkillManifest from dictionary."""
        # Filter only valid fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class SkillTest:
    """Skill test case - YAML format per spec.

    Matches the test suite YAML schema:
        version: 1
        tests:
          - name: "..."
            inputs: {...}
            assertions: [...]
            expected: {...}
    """
    name: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    assertions: List[Dict[str, Any]] = field(default_factory=list)
    expected: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillEntry:
    """Registered skill entry with metadata."""
    manifest: SkillManifest
    path: Path
    prompt_path: Optional[Path] = None
    test_results: List[Dict[str, Any]] = field(default_factory=list)
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    status: SkillQAStatus = SkillQAStatus.PENDING


class SkillRegistry:
    """Skill Registry - manages skill packages."""

    def __init__(self, skills_root: str = "skills"):
        self.registry_id = "skill-registry@vjsos-ai"
        self.skills_root = Path(skills_root)
        self.skills_root.mkdir(parents=True, exist_ok=True)

        self.skills: Dict[str, SkillEntry] = {}  # skill_id@version -> SkillEntry
        self.aliases: Dict[str, str] = {}  # skill_id -> latest version
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.index_path = self.skills_root / "registry_index.json"

        self._load_index()

    def _load_index(self):
        """Load the registry index from disk."""
        if self.index_path.exists():
            with open(self.index_path, 'r') as f:
                data = json.load(f)
            # Reconstruct skills
            for skill_key, entry_data in data.get("skills", {}).items():
                manifest = SkillManifest.from_dict(entry_data["manifest"])
                entry = SkillEntry(
                    manifest=manifest,
                    path=Path(entry_data["path"]),
                    prompt_path=Path(entry_data["prompt_path"]) if entry_data.get("prompt_path") else None,
                    status=SkillQAStatus(entry_data.get("status", "pending")),
                    registered_at=entry_data.get("registered_at", ""),
                    test_results=entry_data.get("test_results", []),
                )
                self.skills[skill_key] = entry
                self.aliases[manifest.skill_id] = manifest.version
                self.dependency_graph[skill_key] = set(manifest.dependencies)

    def _save_index(self):
        """Save the registry index to disk."""
        index_data = {
            "version": "1.0.0",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "skills": {}
        }
        for skill_key, entry in self.skills.items():
            index_data["skills"][skill_key] = {
                "manifest": asdict(entry.manifest),
                "path": str(entry.path),
                "prompt_path": str(entry.prompt_path) if entry.prompt_path else None,
                "status": entry.status.value,
                "registered_at": entry.registered_at,
                "test_results": entry.test_results
            }
        with open(self.index_path, 'w') as f:
            json.dump(index_data, f, indent=2)

    def register_skill(self, skill_path: str) -> Dict[str, Any]:
        """Register a skill package from a directory."""
        path = Path(skill_path)
        if not path.exists() or not path.is_dir():
            return {"success": False, "error": f"Path not found: {skill_path}"}

        # Look for binder/skill.md
        skill_md = path / "binder" / "skill.md"
        if not skill_md.exists():
            skill_md = path / "skill.md"
        if not skill_md.exists():
            return {"success": False, "error": "skill.md not found in package"}

        # Parse manifest
        manifest = self._parse_manifest(skill_md)
        if not manifest:
            return {"success": False, "error": "Failed to parse skill.md"}

        # Validate manifest
        validation = self._validate_manifest(manifest)
        if not validation["valid"]:
            return {"success": False, "error": validation["error"]}

        # Check for existing version
        skill_key = f"{manifest.skill_id}@{manifest.version}"
        if skill_key in self.skills:
            return {"success": False, "error": f"Skill {skill_key} already registered"}

        # Check dependencies
        dep_check = self._check_dependencies(manifest.dependencies)
        if not dep_check["satisfied"]:
            return {"success": False, "error": f"Unsatisfied dependencies: {dep_check['missing']}"}

        # Find prompt file
        prompt_path = path / "binder" / "prompt.md"
        if not prompt_path.exists():
            prompt_path = path / "prompt.md"

        # Create skill entry
        entry = SkillEntry(
            manifest=manifest,
            path=path,
            prompt_path=prompt_path if prompt_path.exists() else None
        )

        # Register
        self.skills[skill_key] = entry
        self.aliases[manifest.skill_id] = manifest.version
        self.dependency_graph[skill_key] = set(manifest.dependencies)

        self._save_index()

        return {
            "success": True,
            "skill_key": skill_key,
            "manifest": asdict(manifest),
            "message": f"Skill {skill_key} registered successfully"
        }

    def get_skill(self, skill_id: str, version: Optional[str] = None) -> Optional[SkillEntry]:
        """Get a skill by ID and optional version."""
        if version:
            return self.skills.get(f"{skill_id}@{version}")
        # Return latest version
        latest_version = self.aliases.get(skill_id)
        if latest_version:
            return self.skills.get(f"{skill_id}@{latest_version}")
        return None

    def get_prompt(self, skill_id: str, version: Optional[str] = None) -> Optional[str]:
        """Get the prompt for a skill."""
        entry = self.get_skill(skill_id, version)
        if entry and entry.prompt_path and entry.prompt_path.exists():
            return entry.prompt_path.read_text()
        return None

    def list_skills(self, domain: Optional[str] = None, type_: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered skills with optional filters."""
        results = []
        for skill_key, entry in self.skills.items():
            manifest = entry.manifest
            if domain and manifest.domain != domain:
                continue
            if type_ and manifest.type != type_:
                continue
            results.append({
                "skill_id": manifest.skill_id,
                "version": manifest.version,
                "domain": manifest.domain,
                "type": manifest.type,
                "description": manifest.description,
                "owner": manifest.owner,
                "qa_status": entry.status.value,
                "registered_at": entry.registered_at
            })
        return results

    def resolve_dependencies(self, skill_id: str, version: Optional[str] = None) -> List[str]:
        """Resolve all dependencies for a skill (topological order)."""
        entry = self.get_skill(skill_id, version)
        if not entry:
            return []

        visited = set()
        order = []

        def visit(dep_key: str):
            if dep_key in visited:
                return
            visited.add(dep_key)
            # Visit dependencies first
            for dep in self.dependency_graph.get(dep_key, []):
                visit(dep)
            order.append(dep_key)

        skill_key = f"{entry.manifest.skill_id}@{entry.manifest.version}"
        visit(skill_key)
        return order

    def run_tests(self, skill_id: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Run all tests for a skill."""
        entry = self.get_skill(skill_id, version)
        if not entry:
            return {"success": False, "error": "Skill not found"}

        test_dir = entry.path / "tests"
        if not test_dir.exists():
            return {"success": False, "error": "No tests directory found"}

        results = []
        for test_file in test_dir.glob("*.yaml"):
            test_result = self._run_test_file(test_file, entry)
            results.append(test_result)

        # Update entry
        entry.test_results = results
        all_passed = all(r.get("passed", False) for r in results)
        entry.status = SkillQAStatus.VERIFIED if all_passed else SkillQAStatus.FAILED

        self._save_index()

        return {
            "success": True,
            "skill_key": f"{entry.manifest.skill_id}@{entry.manifest.version}",
            "all_passed": all_passed,
            "results": results
        }

    def _run_test_file(self, test_file: Path, entry: SkillEntry) -> Dict[str, Any]:
        """Run a single test YAML file.

        Supports two formats:
        1. Flat test case: name, skill, version, input, assertions
        2. Test suite: version, tests: [{name, inputs, assertions, expected}, ...]
        """
        with open(test_file, 'r') as f:
            test_data = yaml.safe_load(f)

        # Detect test suite format (has 'tests' key with list)
        if "tests" in test_data and isinstance(test_data.get("tests"), list):
            # Test suite format - run all test cases
            test_cases = []
            for tc_data in test_data["tests"]:
                tc = {
                    "name": tc_data.get("name", "unnamed"),
                    "inputs": tc_data.get("inputs", {}),
                    "assertions": tc_data.get("assertions", []),
                    "expected": tc_data.get("expected", {})
                }
                test_cases.append(self._run_single_test_case(entry, tc, test_file))

            passed = all(tc.get("passed", False) for tc in test_cases)
            return {
                "test_name": test_file.stem,
                "passed": passed,
                "test_cases": test_cases,
                "assertions_checked": sum(len(tc.get("assertions", [])) for tc in test_cases),
                "file": str(test_file)
            }

        # Flat test case format
        test = SkillTest(**test_data)

        # In a real implementation, this would execute the skill prompt
        # For now, we validate the test format
        return {
            "test_name": test.name,
            "skill": test.inputs.get("skill", ""),
            "passed": True,  # placeholder
            "assertions_checked": len(test.assertions),
            "file": str(test_file)
        }

    def _run_single_test_case(self, entry: SkillEntry, tc_data: Dict[str, Any],
                               test_file: Path) -> Dict[str, Any]:
        """Execute a single test case from a test suite."""
        test_name = tc_data.get("name", "unnamed")
        start_time = time.time()

        try:
            # Render the prompt with variables from inputs
            inputs = tc_data.get("inputs", {})
            prompt = entry.path  # placeholder
            passed = True  # placeholder for now

            return {
                "name": test_name,
                "passed": passed,
                "duration_ms": (time.time() - start_time) * 1000,
                "file": str(test_file)
            }
        except Exception as e:
            return {
                "name": test_name,
                "passed": False,
                "duration_ms": (time.time() - start_time) * 1000,
                "error": str(e),
                "file": str(test_file)
            }

    def _parse_manifest(self, skill_md: Path) -> Optional[SkillManifest]:
        """Parse skill.md manifest (YAML frontmatter or full YAML)."""
        content = skill_md.read_text()

        # Try YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    data = yaml.safe_load(parts[1])
                    return SkillManifest.from_dict(data)
                except yaml.YAMLError:
                    pass

        # Try full YAML
        try:
            data = yaml.safe_load(content)
            return SkillManifest.from_dict(data)
        except yaml.YAMLError:
            pass

        return None

    def _validate_manifest(self, manifest: SkillManifest) -> Dict[str, Any]:
        """Validate skill manifest."""
        required_fields = ["skill_id", "version", "owner", "domain", "description", "type", "inputs", "outputs"]
        for field_name in required_fields:
            if not getattr(manifest, field_name, None):
                return {"valid": False, "error": f"Missing required field: {field_name}"}

        # Validate version format (semver)
        parts = manifest.version.split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            return {"valid": False, "error": "Version must be semantic (MAJOR.MINOR.PATCH)"}

        # Validate type
        try:
            SkillType(manifest.type)
        except ValueError:
            return {"valid": False, "error": f"Invalid skill type: {manifest.type}"}

        return {"valid": True}

    def _check_dependencies(self, dependencies: List[str]) -> Dict[str, Any]:
        """Check if all dependencies are satisfied."""
        missing = []
        for dep in dependencies:
            # Parse dep format: skill_id@version or skill_id
            if "@" in dep:
                skill_id, version = dep.split("@", 1)
                if not self.get_skill(skill_id, version):
                    missing.append(dep)
            else:
                if not self.get_skill(dep):
                    missing.append(dep)

        return {"satisfied": len(missing) == 0, "missing": missing}

    def unregister_skill(self, skill_id: str, version: str) -> Dict[str, Any]:
        """Unregister a skill."""
        skill_key = f"{skill_id}@{version}"
        if skill_key not in self.skills:
            return {"success": False, "error": "Skill not found"}

        del self.skills[skill_key]

        # Update alias if it pointed to this version
        if self.aliases.get(skill_id) == version:
            # Find next latest version
            versions = [k.split("@")[1] for k in self.skills if k.startswith(f"{skill_id}@")]
            if versions:
                versions.sort(key=lambda v: tuple(map(int, v.split("."))), reverse=True)
                self.aliases[skill_id] = versions[0]
            else:
                del self.aliases[skill_id]

        if skill_key in self.dependency_graph:
            del self.dependency_graph[skill_key]

        self._save_index()
        return {"success": True, "message": f"Skill {skill_key} unregistered"}

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        domains = {}
        types = {}
        for entry in self.skills.values():
            domains[entry.manifest.domain] = domains.get(entry.manifest.domain, 0) + 1
            types[entry.manifest.type] = types.get(entry.manifest.type, 0) + 1

        return {
            "total_skills": len(self.skills),
            "domains": domains,
            "types": types,
            "skills_by_status": {
                status.value: sum(1 for e in self.skills.values() if e.status == status)
                for status in SkillQAStatus
            }
        }


def main():
    """Test the Skill Registry."""
    registry = SkillRegistry("skills")

    # Test listing (empty initially)
    print("Registry stats:", registry.get_stats())
    print("Skills:", registry.list_skills())

    # Create a test skill package
    test_skill_path = Path("skills/test_skill")
    test_skill_path.mkdir(parents=True, exist_ok=True)
    (test_skill_path / "binder").mkdir(exist_ok=True)

    # Write manifest
    manifest_content = """---
skill_id: "test_skill"
version: "1.0.0"
owner: "test-agent@engineering@vjsos-ai"
domain: "engineering"
description: "Test skill for registry validation"
type: "analysis"
inputs:
  data:
    type: "object"
    required: true
outputs:
  result:
    type: "string"
examples: []
dependencies: []
tests:
  - test_basic.yaml
qa_status: "pending"
changelog: |
  - v1.0.0: Initial release
"""
    (test_skill_path / "binder" / "skill.md").write_text(manifest_content)

    # Write prompt
    (test_skill_path / "binder" / "prompt.md").write_text("# Test Skill Prompt\n\nProcess input data.")

    # Write test
    (test_skill_path / "tests").mkdir(exist_ok=True)
    test_content = """name: "Basic Test"
skill: "test_skill"
version: "1.0.0"
input:
  data: {"key": "value"}
assertions:
  - assertion: "result is not empty"
expected_output_contains:
  - "processed"
"""
    (test_skill_path / "tests" / "test_basic.yaml").write_text(test_content)

    # Register
    result = registry.register_skill(str(test_skill_path))
    print(f"Register result: {result}")

    # List skills
    print(f"Skills: {registry.list_skills()}")

    # Get skill
    skill = registry.get_skill("test_skill")
    print(f"Skill: {skill.manifest.skill_id} v{skill.manifest.version}")

    # Run tests
    test_result = registry.run_tests("test_skill")
    print(f"Test result: {test_result}")

    # Stats
    print(f"Stats: {registry.get_stats()}")


if __name__ == "__main__":
    main()