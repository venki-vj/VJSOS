# VJSOS-AI Quick Start Guide

## Prerequisites
- Git
- Python 3.11+ (for kernel simulation)
- Node.js 20+ (for plugin SDK)
- Docker (for infrastructure components)

---

## Phase 0: Foundation (Current State)

### 1. Clone and Explore
```bash
git clone <repository-url> VJSOS-AI
cd VJSOS-AI
ls -la
```

Expected structure:
```
VJSOS-AI/
├── .git/
├── README.md
├── docs/
│   ├── QUICKSTART.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── AI_CONSTITUTION.md
│   ├── DEPARTMENTS.md
│   ├── AGENTS.md
│   ├── SKILLS.md
│   └── specs/
│       ├── KERNEL_SPEC.md
│       └── AI_OPERATING_SYSTEM_SPEC.md
├── kernel/
│   ├── governor/
│   ├── orchestrator/
│   ├── context-engine/
│   ├── memory-engine/
│   └── qa-engine/
├── agents/
│   ├── directors/
│   ├── qa/
│   └── engineering/
├── departments/
│   ├── engineering/
│   ├── media/
│   ├── business/
│   ├── research/
│   ├── animation/
│   ├── operations/
│   ├── knowledge/
│   ├── infrastructure/
│   └── improvement/
├── memory/
│   ├── session/
│   ├── agent/
│   ├── department/
│   └── global/
├── plugins/
│   ├── COMMON_INTERFACE.md
│   └── registry/
└── skills/
    └── skills-engine/
```

### 2. Verify Constitution Load
```bash
# The Governor validates constitution on startup
cat docs/AI_CONSTITUTION.md | head -50
```

### 3. Verify Kernel Components
```bash
ls kernel/
# Should show: governor/, orchestrator/, context-engine/, memory-engine/, qa-engine/
```

---

## Phase 1: Local Simulation Setup

### 1. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Kernel Health Check
```bash
python -m kernel.health_check
# Expected: All 5 components report "HEALTHY"
```

### 3. Initialize Memory Tiers
```bash
python -m memory.initialize
# Creates directory structure and loads Tier 4 (Global) + Tier 3 (Department)
```

### 4. Load Skill Registry
```bash
python -m skills.registry load
# Registers all skill packages from skills/
```

### 5. Load Plugins
```bash
python -m plugins.loader
# Validates and loads plugins from plugins/registry/
```

---

## Phase 2: Run First Orchestration

### 1. Start Orchestrator
```bash
python -m kernel.orchestrator serve
```

### 2. Submit a Test Task
```bash
python -m kernel.orchestrator dispatch \
  --task "Create a simple Python script that prints 'Hello VJSOS'" \
  --department engineering
```

### 3. Observe Flow
```
User Request
    ↓
Message Bus → Governor (constitutional check)
    ↓
Orchestrator (analyze → plan → context → dispatch)
    ↓
Engineering Director → Worker Agent (context package)
    ↓
Worker produces output
    ↓
QA Agent verifies (rubric)
    ↓
Pass → Return to user | Fail → Feedback loop (max 3)
```

---

## Phase 3: Local Development Workflow

### Adding a New Skill
```bash
# 1. Create skill structure
mkdir -p skills/android/new_skill/{binder,tests,examples}

# 2. Write skill.md manifest
cat > skills/android/new_skill/binder/skill.md << 'EOF'
skill_id: "new_skill"
version: "1.0.0"
owner: "android-agent@engineering@vjsos-ai"
domain: "android"
description: "..."
type: "analysis"
# ... (see AI_OPERATING_SYSTEM_SPEC.md §5.2)
EOF

# 3. Write prompt.md
cat > skills/android/new_skill/binder/prompt.md << 'EOF'
# Skill Prompt: new_skill
...
EOF

# 4. Add tests
cat > skills/android/new_skill/tests/test_basic.yaml << 'EOF'
name: "Basic Test"
skill: "new_skill"
version: "1.0.0"
# ... (see spec §5.4)
EOF

# 5. Register
python -m skills.registry register skills/android/new_skill

# 6. QA Verify
python -m qa.verify --skill new_skill
```

### Adding a New Agent
```bash
# 1. Create agent prompt in agents/{department}/
# 2. Add to department manifest (MANIFEST.md)
# 3. Register with Governor
python -m governor.register_agent --config agents/engineering/new-agent.md
```

### Adding a Plugin
```bash
# 1. Create plugin manifest
cat > plugins/mytool/manifest.json << 'EOF'
{
  "plugin_id": "mytool@v1.0.0",
  "type": "api_integration",
  "auth_method": "oauth",
  "capabilities": ["read_data", "write_data"],
  "governor_approval": true
}
EOF

# 2. Implement plugin SDK handlers
# 3. Governor review
python -m governor.review_plugin --manifest plugins/mytool/manifest.json
```

---

## Directory Structure Reference

| Directory | Purpose |
|-----------|---------|
| `kernel/` | Core system components |
| `agents/` | Individual agent prompts |
| `departments/` | Department manifests + agents |
| `memory/` | 4-tier memory storage |
| `plugins/` | External integrations |
| `skills/` | Capability packages |
| `docs/` | Specifications and guides |

---

## Configuration Files

### `config/kernel.yaml`
```yaml
governor:
  constitution_path: "docs/AI_CONSTITUTION.md"
  
orchestrator:
  max_qa_cycles: 3
  default_context_budget: 8000
  
context_engine:
  relevance_weights:
    domain_match: 0.4
    recency: 0.2
    frequency: 0.2
    explicit_reference: 0.2
  
memory_engine:
  tiers:
    session:
      ttl_hours: 24
      max_entries: 1000
    agent:
      ttl_days: 180
      dedup_threshold: 0.95
    department:
      ttl: null  # infinite
      dedup_threshold: 0.95
    global:
      ttl: null
      dedup_threshold: 0.95
      
qa_engine:
  rubric_weights:
    accuracy: 0.30
    completeness: 0.20
    documentation: 0.15
    tests: 0.20
    constitution_compliance: 0.15
  max_feedback_cycles: 3
```

---

## Testing the Framework

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### End-to-End Test
```bash
python -m tests.e2e.test_full_orchestration
```

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Governor rejects task | Check Constitution compliance |
| QA fails repeatedly | Review rubric in `departments/{dept}/qa-*.md` |
| Context budget exceeded | Narrow task scope or increase budget |
| Plugin auth fails | Verify vault credentials, Governor approval |
| Memory tier not loading | Check `memory/` permissions and structure |

---

## Next Steps

See `docs/IMPLEMENTATION_PLAN.md` for:
- Phase 1: Kernel implementation details
- Phase 2: Infrastructure and services
- Phase 3: Department rollout
- Phase 4: Expansion and optimization

---

## Support

- Architecture questions → `docs/specs/AI_OPERATING_SYSTEM_SPEC.md`
- Agent development → `docs/AGENTS.md`
- Skill creation → `docs/SKILLS.md`
- Plugin development → `plugins/COMMON_INTERFACE.md`

---
**Version:** 1.0.0 | **Last Updated:** 2026-08-07