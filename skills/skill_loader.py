#!/usr/bin/env python3
"""
Skill Loader - Dynamic Prompt Loading and Skill Instantiation

Loads skill manifests from disk, resolves the prompt templates and
associated files, and instantiates callable skill objects that the
Orchestrator can dispatch.

Supports:
- Loading skill.md manifests from a directory tree
- Dynamic prompt loading with Jinja-style substitution
- Dependency resolution via the SkillRegistry
- Skill object instantiation with capability checks
"""

import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

from skills.registry import SkillRegistry, SkillManifest, SkillType


@dataclass
class LoadedSkill:
    """A skill loaded into memory and ready for dispatch."""
    manifest: SkillManifest
    prompt_template: str
    prompt_variables: List[str]
    resolved_dependencies: List[str]
    skill_path: Path

    @property
    def skill_id(self) -> str:
        return self.manifest.skill_id

    def render_prompt(self, variables: Dict[str, str]) -> str:
        """Render the prompt template with provided variables.

        Supports both Jinja-style `{{var}}` (used by skill prompt.md files)
        and format-style `{var}` markers. Missing variables are left as-is.
        """
        import re

        def _sub(m):
            return variables.get(m.group(1) or m.group(2), m.group(0))

        return re.sub(r"\{\{(\w+)\}\}|\{(\w+)\}", _sub, self.prompt_template)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifest": asdict(self.manifest),
            "prompt_variables": self.prompt_variables,
            "resolved_dependencies": self.resolved_dependencies,
            "skill_path": str(self.skill_path)
        }


class SkillLoader:
    """Loads and caches skill definitions from disk."""

    def __init__(self, registry: SkillRegistry):
        self.loader_id = "skill-loader@vjsos-ai"
        self.registry = registry
        self._loaded_skills: Dict[str, LoadedSkill] = {}
        self._cache_ttl = 300  # 5 minutes
        self._last_loaded: Dict[str, float] = {}

    def load_skill(self, skill_id: str) -> Optional[LoadedSkill]:
        """Load a single skill by ID, using cache if available."""
        skill = self.registry.get_skill(skill_id)
        if not skill:
            return None

        # Check cache
        cached = self._loaded_skills.get(skill_id)
        cache_age = time.time() - self._last_loaded.get(skill_id, 0)
        if cached and cache_age < self._cache_ttl:
            return cached

        skill_path = Path(self.registry.skills_root) / skill_id
        loaded = self._load_skill_from_path(skill.manifest, skill_path)
        if loaded:
            self._loaded_skills[skill_id] = loaded
            self._last_loaded[skill_id] = time.time()
        return loaded

    def _load_skill_from_path(self, manifest: SkillManifest,
                               skill_path: Path) -> Optional[LoadedSkill]:
        """Load skill files from a directory."""
        if not skill_path.exists():
            return None

        # Load the prompt template (skill packages use binder/prompt.md)
        prompt_path = skill_path / "binder" / "prompt.md"
        if not prompt_path.exists():
            prompt_path = skill_path / "prompt.md"
        if prompt_path.exists():
            prompt_template = prompt_path.read_text(encoding="utf-8")
        else:
            # Fallback to manifest description
            prompt_template = manifest.description or ""

        # Extract prompt variables ({{var}} style markers)
        import re
        prompt_variables = list(set(re.findall(r"\{\{(\w+)\}\}", prompt_template)))

        # Resolve dependencies
        resolved_deps = list(manifest.dependencies or [])

        return LoadedSkill(
            manifest=manifest,
            prompt_template=prompt_template,
            prompt_variables=prompt_variables,
            resolved_dependencies=resolved_deps,
            skill_path=skill_path
        )

    def load_all(self, force: bool = False) -> List[LoadedSkill]:
        """Load all registered skills."""
        if force:
            self._loaded_skills.clear()
            self._last_loaded.clear()

        loaded = []
        for skill_key in self.registry.skills:
            skill_id = skill_key.split("@")[0]
            skill = self.load_skill(skill_id)
            if skill:
                loaded.append(skill)
        return loaded

    def get_loaded_skill(self, skill_id: str) -> Optional[LoadedSkill]:
        """Get a cached loaded skill without re-reading from disk."""
        cached = self._loaded_skills.get(skill_id)
        if not cached:
            return self.load_skill(skill_id)
        return cached

    def render_skill_prompt(self, skill_id: str,
                            variables: Dict[str, str]) -> Optional[str]:
        """Render a skill's prompt with given variables."""
        loaded = self.get_loaded_skill(skill_id)
        if not loaded:
            return None
        return loaded.render_prompt(variables)

    def get_skill_requirements(self, skill_id: str) -> Dict[str, Any]:
        """Get input/output/schema requirements for a skill."""
        loaded = self.get_loaded_skill(skill_id)
        if not loaded:
            return {}

        manifest = loaded.manifest
        return {
            "skill_id": manifest.skill_id,
            "type": manifest.type,
            "inputs": asdict(manifest.inputs) if hasattr(manifest.inputs, '__dict__') else manifest.inputs,
            "outputs": asdict(manifest.outputs) if hasattr(manifest.outputs, '__dict__') else manifest.outputs,
            "prompt_variables": loaded.prompt_variables,
            "dependencies": loaded.resolved_dependencies
        }


def main():
    """Test the Skill Loader."""
    registry = SkillRegistry()
    # Register a test skill
    from skills.registry import SkillManifest
    test_manifest = SkillManifest(
        skill_id="test_skill",
        version="1.0.0",
        owner="engineering",
        domain="test",
        description="Test skill for validation",
        type=SkillType.ANALYSIS.value,
        inputs={},
        outputs={},
        dependencies=[]
    )
    registry.register_skill(test_manifest)

    loader = SkillLoader(registry)
    loaded = loader.load_skill("test_skill")
    print(f"Loaded: {loaded is not None}")
    if loaded:
        print(f"  Prompt vars: {loaded.prompt_variables}")


if __name__ == "__main__":
    main()