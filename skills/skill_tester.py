#!/usr/bin/env python3
"""
Skill Tester - Automated Test Runner for Skills

Executes skill tests defined in YAML format:
    version: 1
    tests:
      - name: "happy_path"
        inputs:
          prompt: "..."
        expected:
          contains: ["key phrase"]
          not_contains: ["forbidden"]
        assertions:
          - field: "outputs.text"
            operator: "contains"
            value: "expected output"

Usage:
    tester = SkillTester(skill_registry, skill_loader)
    results = tester.run_tests("skill_id")
"""

import yaml
import time
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List

from skills.registry import SkillRegistry, SkillQAStatus
from skills.skill_loader import SkillLoader


class TestResult(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class Assertion:
    """A single test assertion."""
    field: str
    operator: str  # contains, not_contains, equals, greater_than, less_than, exists
    value: Any
    expected: Optional[Any] = None

    def evaluate(self, actual_value: Any) -> bool:
        """Evaluate this assertion against an actual value."""
        try:
            if self.operator == "exists":
                return actual_value is not None
            if self.operator == "contains":
                if isinstance(actual_value, str) and isinstance(self.value, str):
                    return self.value in actual_value
                if isinstance(actual_value, list):
                    return self.value in actual_value
                return False
            if self.operator == "not_contains":
                if isinstance(actual_value, str) and isinstance(self.value, str):
                    return self.value not in actual_value
                return True
            if self.operator == "equals":
                return actual_value == self.value
            if self.operator == "not_equals":
                return actual_value != self.value
            if self.operator == "greater_than":
                return float(actual_value) > float(self.value)
            if self.operator == "less_than":
                return float(actual_value) < float(self.value)
            return False
        except (TypeError, ValueError):
            return False


@dataclass
class TestCaseResult:
    """Result of a single test case execution."""
    name: str
    result: TestResult
    duration_ms: float
    error: Optional[str] = None
    assertion_results: List[Dict[str, Any]] = field(default_factory=list)
    actual_output: Optional[Any] = None


@dataclass
class TestSuiteResult:
    """Result of running a test suite for a skill."""
    skill_id: str
    test_suite_path: str
    total: int
    passed: int
    failed: int
    errors: int
    skipped: int
    duration_ms: float
    test_cases: List[TestCaseResult]
    qa_status: SkillQAStatus
    executed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class SkillTester:
    """Runs automated tests for skills defined in YAML."""

    def __init__(self, registry: SkillRegistry, loader: SkillLoader):
        self.tester_id = "skill-tester@vjsos-ai"
        self.registry = registry
        self.loader = loader

    def run_tests(self, skill_id: str) -> TestSuiteResult:
        """Run the test suite for a skill."""
        skill = self.loader.get_loaded_skill(skill_id)
        if not skill:
            return TestSuiteResult(
                skill_id=skill_id,
                test_suite_path="",
                total=0, passed=0, failed=0, errors=1, skipped=0,
                duration_ms=0, test_cases=[],
                qa_status=SkillQAStatus.FAILED,
            )

        # Locate test files: manifest's `tests` list → tests/*.yaml → test.yaml
        test_files = []
        manifest_tests = skill.manifest.tests or []
        for t in manifest_tests:
            p = skill.skill_path / "tests" / t
            if p.exists():
                test_files.append(p)
        if not test_files:
            tests_dir = skill.skill_path / "tests"
            if tests_dir.exists():
                test_files = sorted(tests_dir.glob("*.yaml"))
        if not test_files:
            p = skill.skill_path / "test.yaml"
            if p.exists():
                test_files = [p]
        if not test_files:
            return TestSuiteResult(
                skill_id=skill_id,
                test_suite_path="",
                total=0, passed=0, failed=0, errors=0, skipped=1,
                duration_ms=0, test_cases=[
                    TestCaseResult(
                        name="test_suites",
                        result=TestResult.SKIPPED,
                        duration_ms=0,
                        error="No test.yaml found"
                    )
                ],
                qa_status=SkillQAStatus.PENDING
            )

        # Load and run each test suite
        test_cases = []
        start_time = time.time()

        for test_path in test_files:
            test_config = self._load_test_suite(test_path)
            if not test_config:
                test_cases.append(TestCaseResult(
                    name=f"load:{test_path.name}",
                    result=TestResult.ERROR,
                    duration_ms=0,
                    error="Failed to parse YAML"
                ))
                continue
            for test_def in test_config.get("tests", []):
                case_result = self._run_test_case(skill, test_def)
                test_cases.append(case_result)

        duration_ms = (time.time() - start_time) * 1000
        passed = sum(1 for tc in test_cases if tc.result == TestResult.PASSED)
        failed = sum(1 for tc in test_cases if tc.result == TestResult.FAILED)
        errors = sum(1 for tc in test_cases if tc.result == TestResult.ERROR)
        skipped = sum(1 for tc in test_cases if tc.result == TestResult.SKIPPED)

        # Determine QA status
        qa_status = SkillQAStatus.VERIFIED if failed == 0 and errors == 0 else SkillQAStatus.FAILED

        return TestSuiteResult(
            skill_id=skill_id,
            test_suite_path="; ".join(str(p) for p in test_files),
            total=len(test_cases),
            passed=passed, failed=failed, errors=errors, skipped=skipped,
            duration_ms=duration_ms,
            test_cases=test_cases,
            qa_status=qa_status
        )

    def _load_test_suite(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load and parse a YAML test suite."""
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def _run_test_case(self, skill, test_def: Dict[str, Any]) -> TestCaseResult:
        """Execute a single test case definition."""
        test_name = test_def.get("name", "unnamed")
        start_time = time.time()
        assertions_passed = []
        error_msg = None
        result = TestResult.PASSED
        actual_output = None

        try:
            # Render the prompt with variables from test inputs
            inputs = test_def.get("inputs", {})
            prompt = skill.render_prompt(inputs) if hasattr(skill, "render_prompt") else ""
            actual_output = {"prompt_rendered": len(prompt) > 0}

            # Evaluate assertions
            assertions = test_def.get("assertions", [])
            for assertion in assertions:
                field_path = assertion.get("field", "")
                operator = assertion.get("operator", "exists")
                expected = assertion.get("value")

                actual_value = self._extract_field(actual_output, field_path)
                passed = Assertion(
                    field=field_path,
                    operator=operator,
                    value=expected
                ).evaluate(actual_value)

                assertions_passed.append({
                    "field": field_path,
                    "operator": operator,
                    "expected": expected,
                    "actual": actual_value,
                    "passed": passed
                })

                if not passed:
                    result = TestResult.FAILED

            # Evaluate expected output checks
            expected = test_def.get("expected", {})
            if "contains" in expected:
                for phrase in expected["contains"]:
                    if phrase not in prompt:
                        result = TestResult.FAILED
                        assertions_passed.append({
                            "field": "prompt",
                            "operator": "contains",
                            "expected": phrase,
                            "actual": prompt[:200],
                            "passed": False
                        })

            if "not_contains" in expected:
                for phrase in expected["not_contains"]:
                    if phrase in prompt:
                        result = TestResult.FAILED
                        assertions_passed.append({
                            "field": "prompt",
                            "operator": "not_contains",
                            "expected": phrase,
                            "actual": "...",
                            "passed": False
                        })

        except Exception as e:
            result = TestResult.ERROR
            error_msg = str(e)

        duration_ms = (time.time() - start_time) * 1000

        return TestCaseResult(
            name=test_name,
            result=result,
            duration_ms=duration_ms,
            error=error_msg,
            assertion_results=assertions_passed,
            actual_output=actual_output
        )

    def _extract_field(self, data: Any, field_path: str) -> Any:
        """Extract a value from a nested structure by dot-path."""
        current = data
        for part in field_path.split("."):
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, object) and hasattr(current, part):
                current = getattr(current, part)
            else:
                return None
        return current

    def get_test_summary(self, result: TestSuiteResult) -> str:
        """Format a human-readable test summary."""
        lines = [
            f"Skill: {result.skill_id}",
            f"Total: {result.total} | Passed: {result.passed} | Failed: {result.failed} | Errors: {result.errors} | Skipped: {result.skipped}",
            f"Duration: {result.duration_ms:.1f}ms",
            f"QA Status: {result.qa_status.value}"
        ]
        for tc in result.test_cases:
            status_mark = "✓" if tc.result == TestResult.PASSED else "✗" if tc.result == TestResult.FAILED else "!" if tc.result == TestResult.ERROR else "⊘"
            lines.append(f"  {status_mark} {tc.name} ({tc.duration_ms:.1f}ms)")
            if tc.error:
                lines.append(f"    Error: {tc.error}")
        return "\n".join(lines)


def main():
    """Test the Skill Tester."""
    registry = SkillRegistry()
    loader = SkillLoader(registry)
    tester = SkillTester(registry, loader)

    # Test with a non-existent skill
    result = tester.run_tests("nonexistent_skill")
    print(f"Test suite result: {tester.get_test_summary(result)}")


if __name__ == "__main__":
    main()