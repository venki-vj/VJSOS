"""
Learning Engine - Post-mortem analysis and continuous improvement.

Components:
- engine.py: Core learning engine with pattern detection and recommendations
- pattern_detector.py: Advanced pattern recognition (performance, failures, correlations)
- proposal_workflow.py: Improvement proposal lifecycle (draft → review → implement → verify)

Usage:
    from learning import LearningEngine, PatternDetector, ProposalWorkflow
    engine = LearningEngine()
    detector = PatternDetector()
    workflow = ProposalWorkflow()
"""

from .engine import LearningEngine, LearningType, PatternDetector as EnginePatternDetector, TrendAnalyzer
from .pattern_detector import PatternDetector, PatternType, Pattern
from .proposal_workflow import ProposalWorkflow, Proposal, ProposalStatus, ProposalPriority, ProposalType

__all__ = [
    # Core engine
    "LearningEngine",
    "LearningType",
    "TrendAnalyzer",

    # Pattern detection (standalone module)
    "PatternDetector",
    "PatternType",
    "Pattern",

    # Proposal workflow
    "ProposalWorkflow",
    "Proposal",
    "ProposalStatus",
    "ProposalPriority",
    "ProposalType",
]