#!/usr/bin/env python3
"""
QA Engine - Multi-Check Verification Framework

QA Engine enforces a 5-check rubric for all work:
- Accuracy: 30% - factual correctness and validity
- Completeness: 20% - all requirements met
- Documentation: 15% - clear explanations, inline docs
- Tests: 20% - test coverage and validation
- Constitution Compliance: 15% - Constitution rules adherence

Maximum of 3 feedback cycles per task.
Central QA Engine coordinates department-specific QA agents.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

class VerdictStatus(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NEEDS_REVISION = "NEEDS_REVISION"

@dataclass
class CheckResult:
    """Result of a single rubric check."""
    name: str
    weight: float
    score: float  # 0.0 - 1.0
    verdict: str  # PASS / FAIL / PARTIAL
    feedback: str
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}

@dataclass
class QAResult:
    """Complete QA verification result."""
    verification_id: str
    task_id: str
    department: str
    timestamp: str
    status: VerdictStatus
    overall_score: float  # weighted average
    checks: List[CheckResult]
    summary: str
    feedback: List[Dict[str, str]]  # file:line + expected fix
    appeal_path: Optional[str] = None
    max_feedback_cycles: int = 3
    feedback_cycles_used: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verification_id": self.verification_id,
            "task_id": self.task_id,
            "department": self.department,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "overall_score": round(self.overall_score, 3),
            "checks": [asdict(c) for c in self.checks],
            "summary": self.summary,
            "feedback": self.feedback,
            "appeal_path": self.appeal_path,
            "max_feedback_cycles": self.max_feedback_cycles,
            "feedback_cycles_used": self.feedback_cycles_used
        }

class QAEngine:
    """QA Engine - central verification coordinator."""

    def __init__(self):
        self.engine_id = "qa-engine@vjsos-ai"
        self.rubric_weights = {
            "accuracy": 0.30,
            "completeness": 0.20,
            "documentation": 0.15,
            "tests": 0.20,
            "constitution_compliance": 0.15
        }
        self.max_feedback_cycles = 3
        self.department_rubrics_path = Path("departments")
        self.qa_logs_path = Path("logs/qa")
        self.qa_logs_path.mkdir(parents=True, exist_ok=True)

    def verify(self, artifact: Dict[str, Any], department: str) -> Dict[str, Any]:
        """Run full QA verification against department rubric."""
        verification_id = f"qa_{int(time.time())}_{department}"

        # Run all 5 checks
        checks = []

        # 1. Accuracy (30%)
        accuracy = self._check_accuracy(artifact)
        checks.append(accuracy)

        # 2. Completeness (20%)
        completeness = self._check_completeness(artifact, department)
        checks.append(completeness)

        # 3. Documentation (15%)
        documentation = self._check_documentation(artifact)
        checks.append(documentation)

        # 4. Tests (20%)
        tests = self._check_tests(artifact)
        checks.append(tests)

        # 5. Constitution Compliance (15%)
        constitution = self._check_constitution_compliance(artifact)
        checks.append(constitution)

        # Calculate weighted overall score
        overall_score = self._calculate_weighted_score(checks)

        # Determine verdict
        if overall_score >= 0.85:
            status = VerdictStatus.APPROVED
        elif overall_score >= 0.60:
            status = VerdictStatus.NEEDS_REVISION
        else:
            status = VerdictStatus.REJECTED

        # Generate feedback
        feedback = self._generate_feedback(checks)

        # Get department rubric path
        appeal_path = f"departments/{department}/MANIFEST.md"

        result = QAResult(
            verification_id=verification_id,
            task_id=artifact.get("task_id", "unknown"),
            department=department,
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=status,
            overall_score=overall_score,
            checks=checks,
            summary=self._generate_summary(checks, status),
            feedback=feedback,
            appeal_path=appeal_path,
            max_feedback_cycles=self.max_feedback_cycles,
            feedback_cycles_used=artifact.get("metadata", {}).get("qa_cycles", 0)
        )

        # Log result
        self._log_verification(result)

        return result.to_dict()

    # === Individual Checks ===

    def _check_accuracy(self, artifact: Dict[str, Any]) -> CheckResult:
        """Check 1: Accuracy (30%) - factual correctness and validity."""
        details = {"checks": []}
        score = 0.0
        verdict = "FAIL"
        feedback = ""

        # Check for factual claims verification
        content = artifact.get("content", "")
        if isinstance(content, str):
            content_str = content
        else:
            content_str = json.dumps(content)

        # Basic accuracy heuristics
        has_citations = "citation" in content_str.lower() or "source" in content_str.lower() or "reference" in content_str.lower()
        has_confidence_levels = "confidence" in content_str.lower()
        is_code_valid = self._validate_code(artifact.get("content", ""))

        # Score based on heuristics
        if has_citations and has_confidence_levels:
            score = 1.0
            verdict = "PASS"
            feedback = "Content includes citations and confidence levels"
        elif has_citations:
            score = 0.8
            verdict = "PARTIAL"
            feedback = "Content includes citations but lacks confidence levels"
        elif is_code_valid:
            score = 0.7
            verdict = "PARTIAL"
            feedback = "Code appears syntactically valid"
        else:
            score = 0.3
            verdict = "FAIL"
            feedback = "No citations, confidence levels, or validated code found"

        details["checks"] = [
            {"name": "citations", "passed": has_citations},
            {"name": "confidence_levels", "passed": has_confidence_levels},
            {"name": "code_validation", "passed": is_code_valid}
        ]

        return CheckResult(
            name="accuracy",
            weight=self.rubric_weights["accuracy"],
            score=score,
            verdict=verdict,
            feedback=feedback,
            details=details
        )

    def _check_completeness(self, artifact: Dict[str, Any], department: str) -> CheckResult:
        """Check 2: Completeness (20%) - all requirements met."""
        details = {"checks": []}
        score = 0.0
        verdict = "FAIL"
        feedback = ""

        # Load department requirements from manifest
        dept_manifest_path = self.department_rubrics_path / department / "MANIFEST.md"
        has_manifest = dept_manifest_path.exists()

        required_fields = ["agent_id", "type", "department", "output"]
        present_fields = [field for field in required_fields
                        if artifact.get(field) or artifact.get("metadata", {}).get(field)]

        score = len(present_fields) / len(required_fields)

        if score >= 0.8:
            verdict = "PASS"
            feedback = f"All {len(present_fields)}/{len(required_fields)} required fields present"
        elif score >= 0.5:
            verdict = "PARTIAL"
            feedback = f"Missing fields: {[f for f in required_fields if f not in present_fields]}"
        else:
            verdict = "FAIL"
            feedback = f"Incomplete: {len(present_fields)}/{len(required_fields)} required fields present"

        details["checks"] = [
            {"name": "has_manifest", "passed": has_manifest},
            {"name": f"required_fields_present_{len(present_fields)}/{len(required_fields)}", "passed": score >= 0.8}
        ]

        return CheckResult(
            name="completeness",
            weight=self.rubric_weights["completeness"],
            score=score,
            verdict=verdict,
            feedback=feedback,
            details=details
        )

    def _check_documentation(self, artifact: Dict[str, Any]) -> CheckResult:
        """Check 3: Documentation (15%) - clear explanations and docs."""
        details = {"checks": []}
        score = 0.0
        verdict = "FAIL"
        feedback = ""

        content = artifact.get("content", "")
        if isinstance(content, str):
            content_str = content
        else:
            content_str = json.dumps(content)

        has_explanations = len(content_str.split("\n")) >= 3  # basic heuristic
        has_comments = "comment" in content_str.lower() or "#" in content_str or "/*" in content_str
        has_structure = any(tag in content_str for tag in ["#", "##", "###", "def ", "class ", "import ", "function "])

        score = (int(has_explanations) + int(has_comments) + int(has_structure)) / 3.0
        verdict = "PASS" if score >= 0.7 else ("PARTIAL" if score >= 0.4 else "FAIL")

        if score >= 0.8:
            feedback = "Good documentation with explanations, comments, and structure"
        elif score >= 0.5:
            feedback = "Some documentation needs improvement"
        else:
            feedback = "Insufficient documentation - add explanations and comments"

        details["checks"] = [
            {"name": "has_explanations", "passed": has_explanations},
            {"name": "has_comments", "passed": has_comments},
            {"name": "has_structure", "passed": has_structure}
        ]

        return CheckResult(
            name="documentation",
            weight=self.rubric_weights["documentation"],
            score=score,
            verdict=verdict,
            feedback=feedback,
            details=details
        )

    def _check_tests(self, artifact: Dict[str, Any]) -> CheckResult:
        """Check 4: Tests (20%) - test coverage and validation."""
        details = {"checks": []}
        score = 0.0
        verdict = "FAIL"
        feedback = ""

        # Check if tests are present in artifact
        tests = artifact.get("tests", artifact.get("test_cases", []))
        has_tests = len(tests) > 0
        has_coverage = artifact.get("coverage", 0) >= 0.8
        has_validation = artifact.get("validation_passed", False)

        if has_tests and has_coverage:
            score = 1.0
            verdict = "PASS"
            feedback = f"Tests present with {artifact.get('coverage', 0)*100:.0f}% coverage"
        elif has_tests:
            score = 0.4
            verdict = "PARTIAL"
            feedback = "Tests present but coverage insufficient"
        else:
            score = 0.0
            verdict = "FAIL"
            feedback = "No tests found - add test coverage"

        details = {
            "checks": [
                {"name": "has_tests", "passed": has_tests},
                {"name": f"coverage_{artifact.get('coverage', 0)*100:.0f}%", "passed": has_coverage},
                {"name": "validation_passed", "passed": has_validation}
            ]
        }

        return CheckResult(
            name="tests",
            weight=self.rubric_weights["tests"],
            score=score,
            verdict=verdict,
            feedback=feedback,
            details=details
        )

    def _check_constitution_compliance(self, artifact: Dict[str, Any]) -> CheckResult:
        """Check 5: Constitution Compliance (15%) - Constitution rules adherence."""
        details = {"checks": []}
        score = 0.0
        verdict = "FAIL"
        feedback = ""

        content = artifact.get("content", "")
        if isinstance(content, str):
            content_str = content
        else:
            content_str = json.dumps(content)

        # Constitution Rule checks
        rule_checks = [
            ("no_self_modification",
             not any(term in content_str.lower() for term in ["self-modify", "autonomous change", "bypass governor"])),
            ("no_knowledge_duplication",
             "duplicate" not in content_str.lower() or "deduplication checked" in content_str.lower()),
            ("governor_authority",
             "governor" in content_str.lower() or "constitution" in content_str.lower()),
            ("no_undocumented_delegation",
             "governor approval" in content_str.lower() or "constitutional" in content_str.lower()),
            ("observability",
             "log" in content_str.lower() or "audit" in content_str.lower() or "trace" in content_str.lower())
        ]

        passed_checks = sum(1 for _, passed in rule_checks if passed)
        score = passed_checks / len(rule_checks)

        violation_names = [name for name, passed in rule_checks if not passed]

        if score == 1.0:
            verdict = "PASS"
            feedback = "Full Constitution compliance"
        elif score >= 0.6:
            verdict = "PARTIAL"
            feedback = f"Constitution violations: {violation_names}"
        else:
            verdict = "FAIL"
            feedback = f"Multiple Constitution violations: {violation_names}"

        details = {"checks": [{"name": name, "passed": passed} for name, passed in rule_checks]}

        return CheckResult(
            name="constitution_compliance",
            weight=self.rubric_weights["constitution_compliance"],
            score=score,
            verdict=verdict,
            feedback=feedback,
            details=details
        )

    # === Helper Methods ===

    def _calculate_weighted_score(self, checks: List[CheckResult]) -> float:
        """Calculate weighted overall score."""
        total = sum(check.weight * check.score for check in checks)
        total_weight = sum(check.weight for check in checks)
        return total / total_weight if total_weight > 0 else 0.0

    def _generate_feedback(self, checks: List[CheckResult]) -> List[Dict[str, str]]:
        """Generate structured feedback with file:line + expected fix."""
        feedback = []
        for check in checks:
            if check.verdict in ("FAIL", "PARTIAL"):
                feedback.append({
                    "file": "artifact_content",
                    "line": "N/A",
                    "check": check.name,
                    "verdict": check.verdict,
                    "expected_fix": check.feedback,
                    "severity": "blocker" if check.verdict == "FAIL" else "major"
                })
        return feedback

    def _generate_summary(self, checks: List[CheckResult], status: VerdictStatus) -> str:
        """Generate human-readable summary."""
        scores = {check.name: check.score for check in checks}
        avg_score = sum(scores.values()) / len(scores) if scores else 0

        return (
            f"QA Verification: {status.value} "
            f"(Score: {avg_score*100:.1f}%) — "
            f"Accuracy: {scores.get('accuracy', 0):.1f}, "
            f"Completeness: {scores.get('completeness', 0):.1f}, "
            f"Documentation: {scores.get('documentation', 0):.1f}, "
            f"Tests: {scores.get('tests', 0):.1f}, "
            f"Constitution: {scores.get('constitution_compliance', 0):.1f}"
        )

    def _log_verification(self, result: QAResult):
        """Log QA verification result."""
        log_entry = result.to_dict()
        log_file = self.qa_logs_path / f"{result.verification_id}.json"
        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=2)

    def _validate_code(self, content: Any) -> bool:
        """Basic code validation."""
        if not isinstance(content, str):
            return True

        # Simple checks
        has_syntax_indicators = any(
            keyword in content for keyword in
            ["def ", "class ", "import ", "function ", "fn ", "# "]
        )

        return has_syntax_indicators

    def get_rubric(self) -> Dict[str, Any]:
        """Get the QA rubric definition."""
        return {
            "version": "2.0",
            "weights": self.rubric_weights,
            "max_feedback_cycles": self.max_feedback_cycles,
            "verdict_thresholds": {
                "approved": ">= 0.85",
                "needs_revision": ">= 0.60 and < 0.85",
                "rejected": "< 0.60"
            },
            "appeal_path": "qa → department_director → governor"
        }

    def get_department_rubric(self, department: str) -> Optional[Dict[str, Any]]:
        """Get department-specific QA rubric."""
        rubric_path = self.department_rubrics_path / department / "MANIFEST.md"
        if rubric_path.exists():
            return {"department": department, "source": str(rubric_path)}
        return None

def main():
    """Test the QA Engine."""
    engine = QAEngine()
    print("Testing QA Engine...")

    # Test artifact
    artifact = {
        "task_id": "test_task_001",
        "agent_id": "android-agent@engineering@vjsos-ai",
        "department": "engineering",
        "content": """
        # Android ANR Analysis

        ## Summary
        This analysis examines ANR patterns in Android applications.

        ## Methodology
        - Analyzed 100 stack traces
        - Identified common deadlock patterns

        ## References
        - Android Developers docs: https://developer.android.com/topic/performance/vitals/anr
        - Confidence: High
        """,
        "tests": [{"test": "anr detection", "passed": True}],
        "coverage": 0.95,
        "validation_passed": True
    }

    result = engine.verify(artifact, "engineering")
    print(f"QA Result: {json.dumps(result, indent=2)}")
    print("\nRubric:")
    print(json.dumps(engine.get_rubric(), indent=2))
    print("\nQA Engine test completed!")

if __name__ == "__main__":
    main()