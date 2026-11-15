#!/usr/bin/env python3
"""
Memory Engine - 4-Tier Memory Architecture

Four-Tier Memory Model:
- Tier 1: Session (24h TTL, per-conversation)
- Tier 2: Agent (180d TTL, per-agent expertise)
- Tier 3: Department (∞ TTL, department knowledge)
- Tier 4: Global (∞ TTL, organizational constitution/vision)

Features:
- Deduplication (content + semantic, threshold 0.95)
- Embedding-based search
- Lifecycle enforcement
- Cross-linking and traceability
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import math

class MemoryTier(Enum):
    SESSION = 1
    AGENT = 2
    DEPARTMENT = 3
    GLOBAL = 4

@dataclass
class MemoryObject:
    """Memory object schema - matches spec."""
    memory_id: str
    tier: int
    owner: str
    type: str  # context, expertise, decision, pattern, lesson, sop
    correlation_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    expires_at: Optional[str] = None
    content: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    governance: Dict[str, Any] = field(default_factory=dict)
    lifecycle: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Set default TTL based on tier
        if self.tier == MemoryTier.SESSION.value and not self.expires_at:
            self.expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
        elif self.tier == MemoryTier.AGENT.value and not self.expires_at:
            self.expires_at = (datetime.utcnow() + timedelta(days=180)).isoformat() + "Z"
        # Tier 3 and 4 have no expiration (∞)

        # Set default lifecycle
        if not self.lifecycle:
            self.lifecycle = {
                "version": "1.0.0",
                "status": "active",
                "last_reviewed": self.created_at,
                "review_interval_days": 180 if self.tier >= MemoryTier.AGENT.value else 30
            }

        # Set default governance
        if not self.governance:
            self.governance = {
                "access_level": "read_write",
                "audit_trail": [],
                "tags": []
            }

class MemoryEngine:
    """Memory Engine - 4-tier memory management with deduplication."""

    def __init__(self, dedup_threshold: float = 0.95):
        self.engine_id = "memory-engine@vjsos-ai"
        self.dedup_threshold = dedup_threshold
        self.storage_paths = {
            MemoryTier.SESSION: Path("memory/session"),
            MemoryTier.AGENT: Path("memory/agent"),
            MemoryTier.DEPARTMENT: Path("memory/department"),
            MemoryTier.GLOBAL: Path("memory/global")
        }
        self._initialize_storage()

        # In-memory indices for fast lookup
        self._indices = {tier: {} for tier in MemoryTier}

    def _initialize_storage(self):
        """Initialize memory tier directories."""
        for path in self.storage_paths.values():
            path.mkdir(parents=True, exist_ok=True)

    # === Core Operations ===

    def store(self, memory: MemoryObject) -> Dict[str, Any]:
        """Store a memory object with deduplication check."""
        # Check deduplication
        dup_result = self._check_deduplication(memory)
        if dup_result["is_duplicate"]:
            return {
                "stored": False,
                "duplicate_of": dup_result["duplicate_id"],
                "similarity": dup_result["similarity"]
            }

        # Assign memory ID if not set
        if not memory.memory_id:
            memory.memory_id = self._generate_memory_id(memory)

        # Set tier-specific path
        tier = MemoryTier(memory.tier)
        tier_path = self.storage_paths[tier]

        # For tier 3 (department), organize by department
        if tier == MemoryTier.DEPARTMENT:
            dept = memory.owner.split("@")[-1] if "@" in memory.owner else "general"
            tier_path = tier_path / dept
            tier_path.mkdir(parents=True, exist_ok=True)

        # For tier 2 (agent), organize by agent
        elif tier == MemoryTier.AGENT:
            agent_id = memory.owner
            tier_path = tier_path / agent_id.replace("@", "_")
            tier_path.mkdir(parents=True, exist_ok=True)

        # For tier 1 (session), organize by correlation_id
        elif tier == MemoryTier.SESSION:
            corr_id = memory.correlation_id or "unknown"
            tier_path = tier_path / corr_id
            tier_path.mkdir(parents=True, exist_ok=True)

        # Write memory file
        filename = f"{memory.memory_id}.json"
        filepath = tier_path / filename

        with open(filepath, 'w') as f:
            json.dump(asdict(memory), f, indent=2)

        # Update index
        self._update_index(memory)

        return {
            "stored": True,
            "memory_id": memory.memory_id,
            "path": str(filepath)
        }

    def retrieve(self, memory_id: str, tier: int) -> Optional[MemoryObject]:
        """Retrieve a specific memory by ID."""
        tier_enum = MemoryTier(tier)
        tier_path = self.storage_paths[tier_enum]

        # Handle subdirectories
        if tier == MemoryTier.DEPARTMENT.value:
            for dept_dir in tier_path.iterdir():
                if dept_dir.is_dir():
                    filepath = dept_dir / f"{memory_id}.json"
                    if filepath.exists():
                        return self._load_memory(filepath)
        elif tier == MemoryTier.AGENT.value:
            for agent_dir in tier_path.iterdir():
                if agent_dir.is_dir():
                    filepath = agent_dir / f"{memory_id}.json"
                    if filepath.exists():
                        return self._load_memory(filepath)
        elif tier == MemoryTier.SESSION.value:
            for corr_dir in tier_path.iterdir():
                if corr_dir.is_dir():
                    filepath = corr_dir / f"{memory_id}.json"
                    if filepath.exists():
                        return self._load_memory(filepath)
        else:
            filepath = tier_path / f"{memory_id}.json"
            if filepath.exists():
                return self._load_memory(filepath)

        return None

    def search(self, query_embedding: List[float],
               tier: Optional[int] = None,
               owner: Optional[str] = None,
               top_k: int = 10,
               min_similarity: float = 0.5) -> List[Tuple[MemoryObject, float]]:
        """Semantic search across memory tiers."""
        results = []

        tiers_to_search = [MemoryTier(tier)] if tier else list(MemoryTier)

        for t in tiers_to_search:
            tier_path = self.storage_paths[t]

            if t == MemoryTier.DEPARTMENT:
                for dept_dir in tier_path.iterdir():
                    if dept_dir.is_dir():
                        results.extend(self._search_directory(
                            dept_dir, query_embedding, owner, min_similarity))
            elif t == MemoryTier.AGENT:
                for agent_dir in tier_path.iterdir():
                    if agent_dir.is_dir():
                        results.extend(self._search_directory(
                            agent_dir, query_embedding, owner, min_similarity))
            elif t == MemoryTier.SESSION:
                for corr_dir in tier_path.iterdir():
                    if corr_dir.is_dir():
                        results.extend(self._search_directory(
                            corr_dir, query_embedding, owner, min_similarity))
            else:
                results.extend(self._search_directory(
                    tier_path, query_embedding, owner, min_similarity))

        # Sort by similarity descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _search_directory(self, directory: Path,
                         query_embedding: List[float],
                         owner: Optional[str],
                         min_similarity: float) -> List[Tuple[MemoryObject, float]]:
        """Search all JSON files in a directory."""
        results = []
        for filepath in directory.glob("*.json"):
            try:
                memory = self._load_memory(filepath)
                if owner and memory.owner != owner:
                    continue

                similarity = self._cosine_similarity(
                    query_embedding, memory.content.get("embedding", []))
                if similarity >= min_similarity:
                    results.append((memory, similarity))
            except (json.JSONDecodeError, KeyError):
                continue
        return results

    def _check_deduplication(self, memory: MemoryObject) -> Dict[str, Any]:
        """Check for duplicates using content hash and semantic similarity."""
        # Content hash deduplication (exact)
        content_hash = self._hash_content(memory.content)
        for existing_id, existing_hash in self._indices[MemoryTier(memory.tier)].get("hashes", {}).items():
            if existing_hash == content_hash:
                return {
                    "is_duplicate": True,
                    "duplicate_id": existing_id,
                    "similarity": 1.0,
                    "type": "content"
                }

        # Semantic deduplication
        memory_embedding = memory.content.get("embedding", [])
        if memory_embedding:
            similar = self.search(
                memory_embedding,
                tier=memory.tier,
                owner=memory.owner,
                top_k=5,
                min_similarity=self.dedup_threshold
            )
            if similar:
                return {
                    "is_duplicate": True,
                    "duplicate_id": similar[0][0].memory_id,
                    "similarity": similar[0][1],
                    "type": "semantic"
                }

        return {"is_duplicate": False}

    def _update_index(self, memory: MemoryObject):
        """Update in-memory indices."""
        tier = MemoryTier(memory.tier)
        if "hashes" not in self._indices[tier]:
            self._indices[tier]["hashes"] = {}
        content_hash = self._hash_content(memory.content)
        self._indices[tier]["hashes"][memory.memory_id] = content_hash

    def _load_memory(self, filepath: Path) -> MemoryObject:
        """Load memory from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return MemoryObject(**data)

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not a or not b or len(a) != len(b):
            return 0.0

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)

    def _hash_content(self, content: Dict[str, Any]) -> str:
        """Generate content hash for exact deduplication."""
        # Normalize and hash
        normalized = json.dumps(content, sort_keys=True)
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

    def _generate_memory_id(self, memory: MemoryObject) -> str:
        """Generate unique memory ID."""
        timestamp = int(time.time())
        content_hash = self._hash_content(memory.content)
        tier_char = {1: "s", 2: "a", 3: "d", 4: "g"}.get(memory.tier, "x")
        return f"mem_{tier_char}{timestamp}_{content_hash[:8]}"

    # === Lifecycle Management ===

    def enforce_ttl(self) -> Dict[str, int]:
        """Enforce TTL - archive expired memories."""
        stats = {"checked": 0, "archived": 0, "errors": 0}
        now = datetime.utcnow()

        for tier in [MemoryTier.SESSION, MemoryTier.AGENT]:
            tier_path = self.storage_paths[tier]

            if tier == MemoryTier.DEPARTMENT:
                for dept_dir in tier_path.iterdir():
                    if dept_dir.is_dir():
                        s = self._check_directory_ttl(dept_dir, now)
                        stats["checked"] += s["checked"]
                        stats["archived"] += s["archived"]
            elif tier == MemoryTier.AGENT:
                for agent_dir in tier_path.iterdir():
                    if agent_dir.is_dir():
                        s = self._check_directory_ttl(agent_dir, now)
                        stats["checked"] += s["checked"]
                        stats["archived"] += s["archived"]
            elif tier == MemoryTier.SESSION:
                for corr_dir in tier_path.iterdir():
                    if corr_dir.is_dir():
                        s = self._check_directory_ttl(corr_dir, now)
                        stats["checked"] += s["checked"]
                        stats["archived"] += s["archived"]

        return stats

    def _check_directory_ttl(self, directory: Path, now: datetime) -> Dict[str, int]:
        """Check TTL for all memories in a directory."""
        stats = {"checked": 0, "archived": 0}
        for filepath in directory.glob("*.json"):
            try:
                memory = self._load_memory(filepath)
                stats["checked"] += 1

                if memory.expires_at:
                    expires = datetime.fromisoformat(memory.expires_at.replace('Z', '+00:00'))
                    if now > expires:
                        self._archive_memory(filepath, memory)
                        stats["archived"] += 1
            except (json.JSONDecodeError, ValueError):
                continue
        return stats

    def _archive_memory(self, filepath: Path, memory: MemoryObject):
        """Archive an expired memory."""
        archive_dir = filepath.parent / "archived"
        archive_dir.mkdir(exist_ok=True)

        archive_path = archive_dir / filepath.name
        filepath.rename(archive_path)

        # Update index
        tier = MemoryTier(memory.tier)
        if "hashes" in self._indices[tier]:
            self._indices[tier]["hashes"].pop(memory.memory_id, None)

    # === Utilities ===

    def get_stats(self) -> Dict[str, Any]:
        """Get memory engine statistics."""
        stats = {}
        for tier in MemoryTier:
            tier_path = self.storage_paths[tier]
            count = 0
            if tier == MemoryTier.DEPARTMENT:
                for dept_dir in tier_path.iterdir():
                    if dept_dir.is_dir():
                        count += len(list(dept_dir.glob("*.json")))
            elif tier == MemoryTier.AGENT:
                for agent_dir in tier_path.iterdir():
                    if agent_dir.is_dir():
                        count += len(list(agent_dir.glob("*.json")))
            elif tier == MemoryTier.SESSION:
                for corr_dir in tier_path.iterdir():
                    if corr_dir.is_dir():
                        count += len(list(corr_dir.glob("*.json")))
            else:
                count = len(list(tier_path.glob("*.json")))

            stats[tier.name.lower()] = {
                "count": count,
                "ttl": "24h" if tier == MemoryTier.SESSION else
                       "180d" if tier == MemoryTier.AGENT else "∞"
            }
        return stats

    def export_tier(self, tier: int, output_path: Path) -> int:
        """Export all memories from a tier."""
        tier_enum = MemoryTier(tier)
        tier_path = self.storage_paths[tier_enum]
        exported = 0

        all_memories = []
        if tier == MemoryTier.DEPARTMENT.value:
            for dept_dir in tier_path.iterdir():
                if dept_dir.is_dir():
                    for filepath in dept_dir.glob("*.json"):
                        all_memories.append(self._load_memory(filepath))
        elif tier == MemoryTier.AGENT.value:
            for agent_dir in tier_path.iterdir():
                if agent_dir.is_dir():
                    for filepath in agent_dir.glob("*.json"):
                        all_memories.append(self._load_memory(filepath))
        elif tier == MemoryTier.SESSION.value:
            for corr_dir in tier_path.iterdir():
                if corr_dir.is_dir():
                    for filepath in corr_dir.glob("*.json"):
                        all_memories.append(self._load_memory(filepath))
        else:
            for filepath in tier_path.glob("*.json"):
                all_memories.append(self._load_memory(filepath))

        with open(output_path, 'w') as f:
            json.dump([asdict(m) for m in all_memories], f, indent=2)

        return len(all_memories)

def main():
    """Test the Memory Engine."""
    engine = MemoryEngine()
    print("Testing Memory Engine...")

    # Create a test memory
    memory = MemoryObject(
        tier=MemoryTier.AGENT.value,
        owner="android-agent@engineering@vjsos-ai",
        type="expertise",
        content={
            "summary": "Android ANR analysis patterns",
            "body": "Key patterns for detecting ANRs in Android apps...",
            "embedding": [0.1] * 768  # placeholder
        },
        tags=["android", "anr", "performance"]
    )

    # Store
    result = engine.store(memory)
    print(f"Store result: {result}")

    # Retrieve
    if result["stored"]:
        retrieved = engine.retrieve(result["memory_id"], MemoryTier.AGENT.value)
        print(f"Retrieved: {retrieved.memory_id if retrieved else 'NOT FOUND'}")

    # Stats
    print(f"Stats: {engine.get_stats()}")
    print("Memory Engine test completed!")

if __name__ == "__main__":
    main()