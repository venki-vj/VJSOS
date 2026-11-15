#!/usr/bin/env python3
"""
Orchestrator - Task Coordination Engine

The Orchestrator never solves tasks directly; it coordinates specialists. It decomposes
requests, selects departments/agents, assembles minimal context, dispatches tasks,
enforces QA gates, aggregates outputs, and logs execution traces.

10-Step Orchestration Loop:
1. Receive      - Accept request from user/message bus
2. Analyze      - Understand intent, decompose task
3. Select       - Choose departments and agents
4. Context      - Request minimal context package
5. Dispatch     - Dispatch tasks with correlation_id
6. Collect      - Collect task results
7. QA           - Verify against department rubric
8. Feedback     - Route QA failures back to agent (max 3 cycles)
9. Finalize     - Aggregate verified outputs
10. Log          - Log execution trace and metrics
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import asyncio


class TaskStatus(Enum):
    RECEIVED = "received"
    ANALYZING = "analyzing"
    ASSEMBLING_CONTEXT = "assembling_context"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    QA_PENDING = "qa_pending"
    QA_FEEDBACK_LOOP = "qa_feedback_loop"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class OrchestrationTask:
    """Represents an orchestrated task."""
    task_id: str
    correlation_id: str
    original_request: str
    intent: Optional[Dict[str, Any]] = None
    decomposition: List[Dict[str, Any]] = field(default_factory=list)
    selected_departments: List[str] = field(default_factory=list)
    selected_agents: List[str] = field(default_factory=list)
    context_package: Optional[Dict[str, Any]] = None
    status: TaskStatus = TaskStatus.RECEIVED
    results: List[Dict[str, Any]] = field(default_factory=list)
    qa_reports: List[Dict[str, Any]] = field(default_factory=list)
    feedback_cycles: int = 0
    max_feedback_cycles: int = 3
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    timestamps: Dict[str, str] = field(default_factory=dict)


class Orchestrator:
    """Orchestrator - task routing, coordination, and QA gate enforcement."""

    def __init__(self, governor=None, context_engine=None, memory_engine=None, qa_engine=None, bootstrap=True):
        self.orchestrator_id = "orchestrator@vjsos-ai"
        self.governor = governor
        self.context_engine = context_engine
        self.memory_engine = memory_engine
        self.qa_engine = qa_engine
        self.tasks = {}
        self.department_registry = {}
        self.agent_registry = {}
        self.max_feedback_cycles = 3
        self.task_timeout = 60  # seconds

        # Auto-bootstrap department/agent registry from MANIFEST.md files
        if bootstrap:
            self.bootstrap_from_manifests()

    # === Main Orchestration Loop ===

    async def orchestrate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the 10-step orchestration loop for an incoming task."""
        task_id = self._generate_task_id()
        correlation_id = self._generate_correlation_id()
        original_request = message.get("content", "")

        task = OrchestrationTask(
            task_id=task_id,
            correlation_id=correlation_id,
            original_request=original_request
        )
        task.timestamps["received_ts"] = time.time()
        task.timestamps["received"] = datetime.utcnow().isoformat() + "Z"
        self.tasks[task_id] = task

        # Step 1: Receive - Log the task
        await self._log_step(task, "RECEIVED", message)
        # Keep the local variable referenced for convention (content source)
        _ = task.original_request

        # Step 2: Analyze - Parse intent
        task.status = TaskStatus.ANALYZING
        intent = self._analyze_intent(original_request)
        task.intent = intent
        await self._log_step(task, "ANALYZED", intent)

        # Step 3: Select - Choose department/agent
        task.status = TaskStatus.DISPATCHED
        selected = self._select_agents(intent)
        if not selected:
            task.status = TaskStatus.FAILED
            task.errors.append("No suitable department/agent found")
            await self._log_step(task, "SELECT_FAILED", {"error": "no_agent_found"})
            return self._format_failure_response(task)

        task.selected_departments = selected["departments"]
        task.selected_agents = selected["agents"]
        await self._log_step(task, "SELECTED", selected)

        # Step 4: Context - Assemble minimal context
        task.status = TaskStatus.ASSEMBLING_CONTEXT
        task.context_package = self._build_context_package(task)
        await self._log_step(task, "CONTEXT_ASSEMBLED", task.context_package)

        # Step 5: Dispatch - Submit to agent
        task.status = TaskStatus.DISPATCHED
        dispatch_result = await self._dispatch(task)
        if not dispatch_result.get("success"):
            task.status = TaskStatus.FAILED
            task.errors.append(dispatch_result.get("error", "dispatch_failed"))
            await self._log_step(task, "DISPATCH_FAILED", dispatch_result)
            return self._format_failure_response(task)

        # Step 6: Collect - Wait for result
        task.status = TaskStatus.IN_PROGRESS
        result = await self._collect_result(task)
        task.results.append(result)
        await self._log_step(task, "RESULT_COLLECTED", result)

        # Step 7: QA Gate - Verify against rubric
        task.status = TaskStatus.QA_PENDING
        qa_report = await self._run_qa_gate(task)
        task.qa_reports.append(qa_report)
        await self._log_step(task, "QA_EXECUTED", qa_report)

        # Step 8: Feedback Loop (max 3 cycles)
        feedback_cycle = 0
        while qa_report.get("status") != "APPROVED" and feedback_cycle < self.max_feedback_cycles:
            task.status = TaskStatus.QA_FEEDBACK_LOOP
            feedback_cycle += 1
            task.feedback_cycles = feedback_cycle
            await self._send_feedback(task, qa_report)

            # Re-run the agent
            result = await self._collect_result(task, reprocess=True)
            task.results.append(result)

            # Re-run QA
            qa_report = await self._run_qa_gate(task)
            task.qa_reports.append(qa_report)
            await self._log_step(task, f"QA_REPORTS_{feedback_cycle}", qa_report)

        # Step 9: Finalize - Aggregate verified outputs
        if qa_report.get("status") == "APPROVED":
            task.status = TaskStatus.COMPLETED
            response = self._format_success_response(task)
            await self._log_step(task, "COMPLETED", response)
        else:
            task.status = TaskStatus.FAILED
            response = self._format_failure_response(
                task, "QA not approved after max feedback cycles")
            await self._log_step(task, "QA_CYCLE_EXHAUSTED", response)

        # Step 10: Log - Metrics
        await self._log_task_metrics(task)
        await self._log_step(task, "LOGGED", task.metrics)

        return response

    # === Step Implementations ===

    def _analyze_intent(self, content: str) -> Dict[str, Any]:
        """Step 2: Analyze request intent (capability mapping)."""
        content_lower = content.lower()
        domain_keywords = {
            "engineering": ["code", "android", "backend", "api", "software", "build",
                            "test", "fix", "refactor"],
            "media": ["video", "script", "content", "youtube", "podcast", "thumbnail", "seo"],
            "business": ["revenue", "pricing", "cost", "market", "strategy", "forecast", "profit"],
            "research": ["data", "analysis", "statistics", "survey", "literature", "research"],
            "animation": ["3d", "model", "rig", "character", "animation", "render"],
            "operations": ["automate", "workflow", "process", "optimize", "manual"],
            "knowledge": ["documentation", "document", "wiki", "guide", "knowledge"],
            "infrastructure": ["infrastructure", "deploy", "ci", "cd", "server", "kubernetes"],
            "improvement": ["improve", "optimize", "performance", "bottleneck", "kpi"]
        }

        best_domain = None
        best_score = 0
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            if score > best_score:
                best_score = score
                best_domain = domain

        if best_score == 0:
            best_domain = "research"  # default to research for analysis tasks

        return {
            "domain": best_domain,
            "confidence": best_score,
            "keywords_found": [
                kw for group in domain_keywords.values() for kw in group if kw in content_lower
            ]
        }

    def _select_agents(self, intent: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Step 3: Select departments and agents based on intent."""
        domain = intent.get("domain")
        department = domain if domain in self.department_registry else None
        if not department:
            return None

        department_agents = self.agent_registry.get(department, [])
        return {
            "departments": [department],
            "agents": department_agents,
            "primary_agent": department_agents[0] if department_agents else None
        }

    def _build_context_package(self, task: OrchestrationTask) -> Dict[str, Any]:
        """Step 4: Build minimal context package (via Context Engine)."""
        if self.context_engine is not None:
            return self.context_engine.assemble(task.intent, task.correlation_id)

        # Default fallback - minimal context
        return {
            "correlation_id": task.correlation_id,
            "intent": task.intent,
            "budget_tokens": 8000,
            "content": []
        }

    async def _dispatch(self, task: OrchestrationTask) -> Dict[str, Any]:
        """Step 5: Dispatch task to selected agent."""
        if not task.selected_agents:
            return {"success": False, "error": "No agents selected"}

        # In a real implementation, this would send to the message bus
        # and await the agent's on_task handler.
        dispatch_record = {
            "task_id": task.task_id,
            "agent": task.selected_agents[0],
            "context_package": task.context_package,
            "correlation_id": task.correlation_id,
            "status": "dispatched"
        }
        return {"success": True, "dispatch": dispatch_record}

    async def _collect_result(self, task: OrchestrationTask, reprocess=False) -> Dict[str, Any]:
        """Step 6: Collect result from agent."""
        # In a real implementation, this waits for agent completion on the bus.
        await asyncio.sleep(0.05)  # simulate async delay
        agent = task.selected_agents[0] if task.selected_agents else "unknown"
        return {
            "result": "Agent result placeholder",
            "produced_by": agent,
            "reprocessed": reprocess
        }

    async def _run_qa_gate(self, task: OrchestrationTask) -> Dict[str, Any]:
        """Step 7: Run the QA gate against the department rubric."""
        if self.qa_engine is not None and task.results and task.selected_departments:
            return self.qa_engine.verify(task.results[-1], task.selected_departments[0])

        # Default fallback - basic QA
        return {
            "status": "APPROVED" if task.results else "REJECTED",
            "score": 0.9 if task.results else 0.0,
            "feedback": [] if task.results else ["No result produced"]
        }

    async def _send_feedback(self, task: OrchestrationTask, qa_report: Dict[str, Any]):
        """Step 8: Send QA feedback to the agent."""
        feedback_message = {
            "type": "qa_feedback",
            "correlation_id": task.correlation_id,
            "task_id": task.task_id,
            "feedback": qa_report.get("feedback", []),
            "cycle": task.feedback_cycles
        }
        # In a real implementation, this sends via the message bus to the agent.
        return feedback_message

    async def _log_task_metrics(self, task: OrchestrationTask):
        """Step 10: Record execution metrics."""
        received_ts = task.timestamps.get("received_ts", time.time())
        task.metrics = {
            "feedback_cycles": task.feedback_cycles,
            "task_duration_s": round(time.time() - received_ts, 3)
        }

    # === Response Formatting ===

    def _format_success_response(self, task: OrchestrationTask) -> Dict[str, Any]:
        return {
            "status": "success",
            "task_id": task.task_id,
            "correlation_id": task.correlation_id,
            "output": task.results[-1] if task.results else None,
            "qa_reports": task.qa_reports
        }

    def _format_failure_response(self, task: OrchestrationTask, error: Optional[str] = None) -> Dict[str, Any]:
        return {
            "status": "failure",
            "task_id": task.task_id,
            "correlation_id": task.correlation_id,
            "error": error or "Unknown orchestration error",
            "errors": task.errors
        }

    # === Utility Methods ===

    async def _log_step(self, task: OrchestrationTask, step: str, data: Dict[str, Any]):
        """Log orchestration step to the audit trail."""
        entry = {
            "task_id": task.task_id,
            "correlation_id": task.correlation_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "step": step,
            "status": task.status.value if isinstance(task.status, TaskStatus) else str(task.status),
            "data": data
        }
        Path("logs").mkdir(parents=True, exist_ok=True)
        with open("logs/orchestration_audit.md", "a") as f:
            f.write(json.dumps(entry) + "\n")

    def bootstrap_from_manifests(self):
        """Automatically bootstrap departments and agents from MANIFEST.md files.

        This enables the Orchestrator to work out of the box without manual registration.
        """
        import re

        departments_path = Path("departments")
        if not departments_path.exists():
            return

        # Load each department
        for dept_dir in departments_path.iterdir():
            if not dept_dir.is_dir():
                continue

            manifest_path = dept_dir / "MANIFEST.md"
            if not manifest_path.exists():
                continue

            dept_id = dept_dir.name

            # Parse MANIFEST.md for worker agents
            content = manifest_path.read_text()
            worker_pattern = r"`([^`]+)`\s*\|?\s*Worker"
            agents = re.findall(worker_pattern, content)

            # Register department
            self.register_department(dept_id, {
                "manifest_path": str(manifest_path),
                "agent_count": len(agents)
            })

            # Register each worker agent
            for agent_id in agents:
                # Extract skill IDs from agent name or use defaults
                skills = self._infer_skills_from_agent(agent_id, dept_id)
                self.register_agent(dept_id, agent_id, skills)

    def _infer_skills_from_agent(self, agent_id: str, dept_id: str) -> List[str]:
        """Infer skill IDs from agent ID based on naming convention."""
        # Agent ID format: type-agent@dept@vjsos-ai
        # E.g., android-agent@engineering@vjsos-ai -> android_development
        defaults = {
            "engineering": ["debugging", "testing"],
            "media": ["research", "script_writing"],
            "business": ["strategic_planning", "market_analysis"],
            "research": ["data_analysis", "knowledge_discovery"],
            "animation": ["3d_modeling", "texturing"],
            "operations": ["process_automation"],
            "knowledge": ["documentation_creation"],
            "infrastructure": ["ci_cd_pipeline"],
            "improvement": ["performance_analysis"]
        }
        return defaults.get(dept_id, ["documentation"])

    def register_department(self, department_id: str, config: Dict[str, Any]):
        """Register a department with the Orchestrator."""
        self.department_registry[department_id] = config

    def register_agent(self, department_id: str, agent_id: str, skills: List[str]):
        """Register an agent under a department."""
        if department_id not in self.agent_registry:
            self.agent_registry[department_id] = []
        self.agent_registry[department_id].append(agent_id)

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the status of a task."""
        task = self.tasks.get(task_id)
        return task.status if task else None

    def _generate_task_id(self) -> str:
        """Generate a unique task ID."""
        return f"task_{int(time.time())}_{uuid.uuid4().hex[:8]}"

    def _generate_correlation_id(self) -> str:
        """Generate a correlation ID for the task."""
        return f"corr_{uuid.uuid4().hex[:12]}"


async def main():
    """Test the Orchestrator."""
    orchestrator = Orchestrator()
    print("Testing Orchestrator...")

    # Register a department
    orchestrator.register_department("engineering", {"mission": "Build software"})
    orchestrator.register_agent("engineering", "android-agent@vjsos-ai", ["android"])

    # Test orchestration
    request = {
        "content": "Create a simple Python function to print hello world",
    }
    result = await orchestrator.orchestrate(request)
    print(f"Orchestration result: {result}")


if __name__ == "__main__":
    asyncio.run(main())