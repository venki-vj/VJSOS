#!/usr/bin/env python3
"""
Context Engine - Minimal Context Assembly

The Context Engine assembles minimal context packages using relevance scoring:
- Domain Match: 40%
- Recency: 20%
- Frequency: 20%
- Explicit Reference: 20%

Default token budget: 8000 tokens

Every agent receives only what it needs, when it needs it.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class MemoryTier(Enum):
    SESSION = 1
    AGENT = 2
    DEPARTMENT = 3
    GLOBAL = 4

@dataclass
class ContextItem:
    """A single context item from memory."""
    memory_id: str
    tier: int
    source: str  # agent_id or department
    content: str
    summary: str
    embedding: List[float]
    tags: List[str]
    created_at: str
    relevance_score: float = 0.0

@dataclass
class ContextPackage:
    """Minimal context package for an agent."""
    correlation_id: str
    intent: Dict[str, Any]
    items: List[ContextItem]
    total_tokens: int
    budget_tokens: int
    assembled_at: str
    query_embedding: List[float]

class ContextEngine:
    """Context Engine - minimal context assembly with relevance scoring."""

    def __init__(self, memory_engine=None, budget_tokens: int = 8000):
        self.engine_id = "context-engine@vjsos-ai"
        self.memory_engine = memory_engine
        self.budget_tokens = budget_tokens
        self.relevance_weights = {
            "domain_match": 0.4,
            "recency": 0.2,
            "frequency": 0.2,
            "explicit_reference": 0.2
        }

    def assemble(self, intent: Dict[str, Any], correlation_id: str) -> ContextPackage:
        """Assemble minimal context package for a task."""
        query_embedding = self._embed_query(intent)

        # Retrieve candidate memories from all tiers
        candidates = self._retrieve_candidates(query_embedding)

        # Score relevance for each candidate
        scored = self._score_relevance(candidates, intent, query_embedding)

        # Pack within token budget
        selected = self._pack_within_budget(scored, self.budget_tokens)

        return ContextPackage(
            correlation_id=correlation_id,
            intent=intent,
            items=selected,
            total_tokens=sum(self._estimate_tokens(item.content) for item in selected),
            budget_tokens=self.budget_tokens,
            assembled_at=datetime.utcnow().isoformat() + "Z",
            query_embedding=query_embedding
        )

    def _retrieve_candidates(self, query_embedding: List[float]) -> List[ContextItem]:
        """Retrieve candidate memories from all tiers."""
        candidates = []

        # In real implementation, this queries the Memory Engine
        # For now, return empty list - will be populated by integration
        return candidates

    def _score_relevance(self, candidates: List[ContextItem],
                        intent: Dict[str, Any],
                        query_embedding: List[float]) -> List[ContextItem]:
        """Score relevance of candidates using weighted algorithm."""
        domain = intent.get("domain", "").lower()

        for candidate in candidates:
            score = 0.0

            # 1. Domain Match (40%) - tag overlap with intent domain
            domain_match = self._calculate_domain_match(candidate.tags, domain)
            score += self.relevance_weights["domain_match"] * domain_match

            # 2. Recency (20%) - exponential decay
            recency = self._calculate_recency(candidate.created_at)
            score += self.relevance_weights["recency"] * recency

            # 3. Frequency (20%) - usage count (would come from memory engine)
            frequency = candidate.relevance_score  # placeholder for usage frequency
            score += self.relevance_weights["frequency"] * frequency

            # 4. Explicit Reference (20%) - direct mention in intent
            explicit = self._calculate_explicit_reference(candidate.content, intent)
            score += self.relevance_weights["explicit_reference"] * explicit

            candidate.relevance_score = min(1.0, score)

        # Sort by relevance descending
        return sorted(candidates, key=lambda c: c.relevance_score, reverse=True)

    def _pack_within_budget(self, scored_items: List[ContextItem],
                           budget: int) -> List[ContextItem]:
        """Pack context items within token budget."""
        selected = []
        current_tokens = 0

        for item in scored_items:
            item_tokens = self._estimate_tokens(item.content)
            if current_tokens + item_tokens <= budget:
                selected.append(item)
                current_tokens += item_tokens
            else:
                # Try to include summary only
                summary_tokens = self._estimate_tokens(item.summary)
                if current_tokens + summary_tokens <= budget:
                    # Create a summary-only variant
                    summary_item = ContextItem(
                        memory_id=item.memory_id,
                        tier=item.tier,
                        source=item.source,
                        content=item.summary,
                        summary=item.summary,
                        embedding=item.embedding,
                        tags=item.tags,
                        created_at=item.created_at,
                        relevance_score=item.relevance_score
                    )
                    selected.append(summary_item)
                    current_tokens += summary_tokens
                else:
                    break

        return selected

    def _calculate_domain_match(self, tags: List[str], domain: str) -> float:
        """Calculate domain match score (0.0 - 1.0)."""
        if not domain or not tags:
            return 0.0

        domain_keywords = {
            "engineering": ["code", "software", "build", "test", "api", "android", "backend"],
            "media": ["video", "script", "content", "youtube", "podcast"],
            "business": ["revenue", "pricing", "market", "strategy", "cost"],
            "research": ["data", "analysis", "statistics", "survey", "literature"],
            "animation": ["3d", "model", "rig", "character", "animation"],
            "operations": ["automate", "workflow", "process", "optimize"],
            "knowledge": ["documentation", "document", "wiki", "guide"],
            "infrastructure": ["infrastructure", "deploy", "ci", "cd", "kubernetes"],
            "improvement": ["improve", "optimize", "performance", "bottleneck"]
        }

        domain_tags = set(t.lower() for t in domain_keywords.get(domain, []))
        candidate_tags = set(t.lower() for t in tags)

        if not domain_tags or not candidate_tags:
            return 0.0

        intersection = domain_tags & candidate_tags
        return len(intersection) / len(domain_tags | candidate_tags)

    def _calculate_recency(self, created_at: str) -> float:
        """Calculate recency score with exponential decay (0.0 - 1.0)."""
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except ValueError:
            return 0.5  # default for unparseable dates

        now = datetime.utcnow()
        age_days = (now - created.replace(tzinfo=None)).total_seconds() / 86400

        # Exponential decay: score = e^(-age/30) where 30 days is half-life
        return math.exp(-age_days / 30)

    def _calculate_frequency(self, candidate: ContextItem) -> float:
        """Calculate frequency score (placeholder - would query Memory Engine)."""
        # In real implementation, this queries memory engine for access count
        return 0.5  # default

    def _calculate_explicit_reference(self, content: str, intent: Dict[str, Any]) -> float:
        """Calculate explicit reference score (0.0 - 1.0)."""
        content_lower = content.lower()
        explicit_refs = intent.get("explicit_references", [])

        if not explicit_refs:
            return 0.0

        matches = sum(1 for ref in explicit_refs if ref.lower() in content_lower)
        return min(1.0, matches / len(explicit_refs))

    def _embed_query(self, intent: Dict[str, Any]) -> List[float]:
        """Generate embedding for intent query."""
        # In real implementation, this uses an embedding model
        # For now, return a deterministic hash-based embedding
        import hashlib
        query_text = json.dumps(intent, sort_keys=True)
        hash_bytes = hashlib.sha256(query_text.encode()).digest()
        # Convert to 768-dim vector (normalized)
        vector = [b / 255.0 for b in hash_bytes] * 3  # 256 * 3 = 768
        return vector[:768]

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    def to_dict(self, package: ContextPackage) -> Dict[str, Any]:
        """Serialize context package to dictionary."""
        return {
            "correlation_id": package.correlation_id,
            "intent": package.intent,
            "items": [
                {
                    "memory_id": item.memory_id,
                    "tier": item.tier,
                    "source": item.source,
                    "content": item.content,
                    "summary": item.summary,
                    "tags": item.tags,
                    "relevance_score": item.relevance_score,
                    "created_at": item.created_at
                }
                for item in package.items
            ],
            "total_tokens": package.total_tokens,
            "budget_tokens": package.budget_tokens,
            "assembled_at": package.assembled_at
        }

def main():
    """Test the Context Engine."""
    engine = ContextEngine()
    print("Testing Context Engine...")

    # Test intent
    intent = {
        "domain": "engineering",
        "task": "Create a Python function to process JSON data",
        "explicit_references": ["python", "json", "parsing"]
    }

    package = engine.assemble(intent, "corr_test123")
    print(f"Assembled package: {engine.to_dict(package)}")
    print("Context Engine test completed!")

if __name__ == "__main__":
    main()