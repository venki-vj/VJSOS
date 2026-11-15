#!/usr/bin/env python3
"""
System Governor - Constitutional Authority

The System Governor is the singleton constitutional authority for the VJSOS-AI operating system.
It enforces the AI Constitution, makes final decisions, and coordinates the entire system.

Key Responsibilities:
- Constitutional compliance enforcement
- Architectural integrity monitoring
- Conflict resolution
- Agent lifecycle approval
- Skill and memory governance
- Refactoring authorization
- Human override coordination
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

class DecisionType(Enum):
    CONSTITUTIONAL_VIOLATION = "constitutional_violation"
    ARCHITECTURAL_CHANGE = "architectural_change"
    AGENT_LIFECYCLE = "agent_lifecycle"
    SKILL_APPROVAL = "skill_approval"
    MEMORY_GOVERNANCE = "memory_governance"
    HUMAN_OVERRIDE = "human_override"
    REFACTORING = "refactoring"

class DecisionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPEALED = "appealed"

@dataclass
class DecisionRecord:
    decision_id: str
    type: DecisionType
    title: str
    rationale: str
    impact: Dict[str, Any]
    proposed_by: str
    timestamp: str
    status: DecisionStatus
    appeal_deadline: str
    constitutional_reference: Optional[str] = None
    governor_override: bool = False
    human_approval_required: bool = False

class SystemGovernor:
    """System Governor - singleton constitutional authority."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.governor_id = "governor@vjsos-ai"
        self.constitution_path = "docs/AI_CONSTITUTION.md"
        self.decisions_log = "memory/global/decisions.md"
        self.appeal_log = "memory/global/human_overrides.md"
        self.approved_agents = []
        self.approved_skills = []
        self.aprovals_required = []
        self._initialized = True

    def validate_constitution(self, content: str) -> Dict[str, Any]:
        """Validate content against AI Constitution."""
        validation_result = {
            "valid": True,
            "violations": [],
            "warnings": [],
            "constitutional_reference": None
        }

        # Check for prohibited patterns (Rule 1: No Self-Modification)
        if self._contains_self_modification(content):
            validation_result["valid"] = False
            validation_result["violations"].append(
                "Contains self-modification (Constitution Article I, Rule 1)"
            )

        # Check for unauthorized delegation (Rule 2: Governor authority)
        if self._contains_unauthorized_delegation(content):
            validation_result["valid"] = False
            validation_result["violations"].append(
                "Contains unauthorized delegation of constitutional authority"
            )

        # Check for knowledge duplication (Rule 4: No Knowledge Duplication)
        if self._contains_knowledge_duplication(content):
            validation_result["warnings"].append(
                "Potential knowledge duplication - check against department memory"
            )

        # Check for memory governance (Rule 8: Memory governance)
        if not self._has_memory_governance(content):
            validation_result["warnings"].append(
                "Lacks memory governance provisions"
            )

        return validation_result

    def make_decision(self, decision_type: DecisionType, title: str,
                     rationale: str, impact: Dict[str, Any],
                     proposed_by: str, human_approval_required: bool = False,
                     constitutional_reference: Optional[str] = None) -> str:
        """Make a constitutional decision."""
        decision_id = f"decision_{int(time.time())}_{decision_type.value}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        appeal_deadline = datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%SZ")

        decision = DecisionRecord(
            decision_id=decision_id,
            type=decision_type,
            title=title,
            rationale=rationale,
            impact=impact,
            proposed_by=proposed_by,
            timestamp=timestamp,
            status=DecisionStatus.PENDING,
            appeal_deadline=appeal_deadline,
            constitutional_reference=constitutional_reference,
            governor_override=False,
            human_approval_required=human_approval_required
        )

        # Log decision
        self._log_decision(decision)

        # Auto-approve if governor override allowed
        if not human_approval_required:
            decision.status = DecisionStatus.APPROVED
            self._record_governor_approval(decision)

        return decision_id

    def approve_agent(self, agent_manifest: Dict[str, Any]) -> bool:
        """Approve an agent for operational status."""
        validation_result = self.validate_constitution(
            json.dumps(agent_manifest)
        )

        if not validation_result["valid"]:
            self._record_rejection(agent_manifest, validation_result["violations"])
            return False

        # Check constitution compliance
        agent_id = agent_manifest.get("agent_id")
        constitution_compliant = self._check_agent_constitution_compliance(agent_manifest)

        if constitution_compliant["valid"]:
            self.approved_agents.append(agent_manifest)
            self._log_agent_approval(agent_manifest)
            return True
        else:
            self._record_rejection(agent_manifest, constitution_compliant["violations"])
            return False

    def approve_skill(self, skill_manifest: Dict[str, Any]) -> bool:
        """Approve a skill for registry."""
        validation_result = self.validate_constitution(
            json.dumps(skill_manifest)
        )

        if not validation_result["valid"]:
            self._record_rejection(skill_manifest, validation_result["violations"])
            return False

        self.approved_skills.append(skill_manifest)
        self._log_skill_approval(skill_manifest)
        return True

    def enforce_memory_governance(self, memory_object: Dict[str, Any]) -> bool:
        """Enforce memory governance rules."""
        # Check for 0.95 deduplication compliance
        tier = memory_object.get("tier")
        owner = memory_object.get("owner")

        if tier in [3, 4]:  # Department or Global tier
            if not self._check_cross_tier_deduplication(memory_object):
                return False

        # Check memory lifecycle compliance
        if not self._check_memory_lifecycle(memory_object):
            return False

        return True

    def process_human_override_request(self, override_request: Dict[str, Any]) -> str:
        """Process human override request for Governor decisions."""
        override_id = f"override_{int(time.time())}"
        override_record = {
            "override_id": override_id,
            "request": override_request,
            "processed_at": datetime.utcnow().isoformat() + "Z",
            "governor_decision": None,
            "human_review": True,
            "status": "pending_human_review"
        }

        self._log_override_request(override_record)
        return override_id

    def get_constitution(self) -> str:
        """Get current Constitution text."""
        try:
            with open(self.constitution_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "Constitution file not found"

    def get_decision_log(self) -> List[Dict[str, Any]]:
        """Get log of all decisions."""
        try:
            with open(self.decisions_log, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_approved_agents(self) -> List[Dict[str, Any]]:
        """Get list of approved agents."""
        return self.approved_agents

    def get_approved_skills(self) -> List[Dict[str, Any]]:
        """Get list of approved skills."""
        return self.approved_skills

    # Internal helper methods

    def _contains_self_modification(self, content: str) -> bool:
        """Check for self-modification patterns."""
        modification_patterns = [
            "self.*modify",
            "autonomous.*change",
            "self.*update",
            "automatic.*refactor",
            "self.*config"
        ]
        content_lower = content.lower()
        for pattern in modification_patterns:
            if pattern in content_lower:
                return True
        return False

    def _contains_unauthorized_delegation(self, content: str) -> bool:
        """Check for unauthorized delegation of authority."""
        delegation_patterns = [
            "bypass.*governor",
            "override.*constitution",
            "delegat.*authority",
            "autonom.*decision"
        ]
        content_lower = content.lower()
        for pattern in delegation_patterns:
            if pattern in content_lower:
                return True
        return False

    def _contains_knowledge_duplication(self, content: str) -> bool:
        """Check for potential knowledge duplication."""
        return False  # Would need semantic comparison

    def _has_memory_governance(self, content: str) -> bool:
        """Check for memory governance provisions."""
        memory_keywords = ["memory", "lifecycle", "ttl", "tier", "deduplication"]
        return any(keyword in content.lower() for keyword in memory_keywords)

    def _check_agent_constitution_compliance(self, agent_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Check if agent complies with Constitution."""
        result = {"valid": True, "violations": []}

        # Check agent identity format
        agent_id = agent_manifest.get("agent_id", "")
        if "@" not in agent_id:
            result["valid"] = False
            result["violations"].append("Invalid agent ID format")

        # Check governance compliance
        governance = agent_manifest.get("governance", {})
        if governance.get("governor_approval_required", True) and \
           not agent_manifest.get("approved_by_governor", False):
            result["valid"] = False
            result["violations"].append("Missing Governor approval")

        return result

    def _check_cross_tier_deduplication(self, memory_object: Dict[str, Any]) -> bool:
        """Check deduplication compliance for cross-tier memories."""
        # This would integrate with Memory Engine for semantic comparison
        return True

    def _check_memory_lifecycle(self, memory_object: Dict[str, Any]) -> bool:
        """Check memory lifecycle compliance."""
        tier = memory_object.get("tier")
        expires_at = memory_object.get("expires_at")

        if tier in [1, 2]:  # Session or Agent tier - has TTL
            if not expires_at:
                return False

        return True

    def _log_decision(self, decision: DecisionRecord):
        """Log decision to file."""
        decisions = self.get_decision_log()
        decisions.append(decision.__dict__)

        Path("memory/global").mkdir(parents=True, exist_ok=True)
        with open(self.decisions_log, 'w') as f:
            json.dump(decisions, f, indent=2)

    def _record_governor_approval(self, decision: DecisionRecord):
        """Record governor approval."""
        decision.status = DecisionStatus.APPROVED
        self._log_decision(decision)

    def _record_rejection(self, item: Dict[str, Any], reasons: List[str]):
        """Record rejection with reasons."""
        rejection_record = {
            "rejected_item": item,
            "rejection_reasons": reasons,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "rejected"
        }

        rejections = self.get_rejection_log()
        rejections.append(rejection_record)

        Path("memory/global").mkdir(parents=True, exist_ok=True)
        with open("memory/global/rejections.md", 'w') as f:
            json.dump(rejections, f, indent=2)

    def _log_agent_approval(self, agent_manifest: Dict[str, Any]):
        """Log agent approval."""
        approval_record = {
            "agent_id": agent_manifest.get("agent_id"),
            "approved_at": datetime.utcnow().isoformat() + "Z",
            "approved_by": self.governor_id,
            "status": "approved"
        }

        approvals = self.get_agent_approval_log()
        approvals.append(approval_record)

        Path("memory/global").mkdir(parents=True, exist_ok=True)
        with open("memory/global/agent_approvals.md", 'w') as f:
            json.dump(approvals, f, indent=2)

    def _log_skill_approval(self, skill_manifest: Dict[str, Any]):
        """Log skill approval."""
        approval_record = {
            "skill_id": skill_manifest.get("skill_id"),
            "approved_at": datetime.utcnow().isoformat() + "Z",
            "approved_by": self.governor_id,
            "status": "approved"
        }

        approvals = self.get_skill_approval_log()
        approvals.append(approval_record)

        Path("memory/global").mkdir(parents=True, exist_ok=True)
        with open("memory/global/skill_approvals.md", 'w') as f:
            json.dump(approvals, f, indent=2)

    def _log_override_request(self, override_record: Dict[str, Any]):
        """Log human override request."""
        overrides = self.get_override_log()
        overrides.append(override_record)

        Path("memory/global").mkdir(parents=True, exist_ok=True)
        with open(self.appeal_log, 'w') as f:
            json.dump(overrides, f, indent=2)

    def get_rejection_log(self) -> List[Dict[str, Any]]:
        """Get rejection log."""
        try:
            with open("memory/global/rejections.md", 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_agent_approval_log(self) -> List[Dict[str, Any]]:
        """Get agent approval log."""
        try:
            with open("memory/global/agent_approvals.md", 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_skill_approval_log(self) -> List[Dict[str, Any]]:
        """Get skill approval log."""
        try:
            with open("memory/global/skill_approvals.md", 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_override_log(self) -> List[Dict[str, Any]]:
        """Get override log."""
        try:
            with open(self.appeal_log, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def __repr__(self):
        return f"<SystemGovernor id={self.governor_id} instance={self._instance}>"

# Global governor instance
governor = SystemGovernor()

if __name__ == "__main__":
    # Test governor functionality
    print("Testing System Governor...")
    print(f"Governor ID: {governor.governor_id}")

    # Test constitution validation
    constitution_text = """
    # VJSOS-AI Constitution
    Article I: Mission - AI-native organization that produces high-quality verifiable outputs.
    Article II: Values - Quality over Speed, Automation over Repetition, Knowledge over Guessing.
    Article III: Communication - All messages flow through Orchestrator, no direct agent-to-agent calls.
    """

    validation = governor.validate_constitution(constitution_text)
    print(f"Constitution validation: {validation}")

    # Test decision making
    decision_id = governor.make_decision(
        DecisionType.ARCHITECTURAL_CHANGE,
        "Test Architectural Change",
        "Testing governor decision making",
        {"impact": "test", "risk": "low"},
        "test_user",
        human_approval_required=False
    )
    print(f"Made decision: {decision_id}")

    print("Governor test completed successfully!")