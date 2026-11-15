# VJSOS-AI Skill Framework

**Version:** 1.0.0 | **Last Updated:** 2026-08-07

---

## Overview

Skills are the atomic units of capability in VJSOS-AI. Each skill is a self-contained package that defines a specific task, its inputs, outputs, and validation tests.

## Skill Structure

```
skills/{domain}/{skill_id}/
├── binder/
│   ├── skill.md        # Manifest: skill_id, version, owner, inputs, outputs, tests
│   └── prompt.md       # Prompt template with variable substitution
├── tests/
│   └── test_{skill}_basic.yaml
├── examples/
│   └── {example}.md
└── .vjsos/
    └── metadata.json
```

## Skill Manifest Schema

A skill manifest (`binder/skill.md`) contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_id` | string | ✅ | Unique identifier for the skill |
| `version` | string | ✅ | Semantic version (e.g., "1.0.0") |
| `owner` | string | ✅ | Agent ID responsible for this skill |
| `domain` | string | ✅ | Department domain (engineering, media, etc.) |
| `description` | string | ✅ | Human-readable description |
| `type` | string | ✅ | analysis, generation, verification, automation, orchestration, monitoring |
| `inputs` | object | ✅ | Input schema with type, required, description |
| `outputs` | object | ✅ | Output schema with type, description |
| `tests` | array | ⚠️ | List of test YAML files |
| `qa_status` | string | ✅ | pending, verified, failed |

## Skill Types

### Analysis
Skills that analyze data, inspect code, or evaluate quality.

**Example:** `code_review`, `performance_analysis`, `architecture_validation`

### Generation
Skills that create new content, code, or assets.

**Example:** `script_writing`, `shot_list_generation`, `api_design`

### Verification
Skills that validate, test, or check outputs.

**Example:** `qa_review`, `standards_enforcement`, `fact_checking`

### Automation
Skills that execute workflows, run tools, or perform repetitive tasks.

**Example:** `ci_cd_pipeline`, `process_automation`, `deploy`

### Orchestration
Skills that coordinate other skills or manage workflows.

**Example:** `video_orchestrator`, `pipeline_coordinator`, `release_manager`

### Monitoring
Skills that observe, report, and alert on system state.

**Example:** `metrics_collection`, `health_check`, `alert_generator`

## Test Format

Tests are written in YAML format:

```yaml
version: 1
tests:
  - name: "happy_path"
    inputs:
      sample: "input data"
    assertions:
      - field: "output.valid"
        operator: "equals"
        value: true
    expected:
      contains: ["expected phrase"]
```

### Assertion Operators

| Operator | Description |
|----------|-------------|
| `exists` | Field exists and is not None |
| `contains` | String contains substring, or list contains element |
| `not_contains` | String does not contain substring |
| `equals` | Value equals expected |
| `not_equals` | Value does not equal expected |
| `greater_than` | Numeric value is greater |
| `less_than` | Numeric value is less |

## QA Rubric

Skills must pass the 5-check QA rubric (Constitution Article V):

| Check | Weight | Description |
|-------|--------|-------------|
| Accuracy | 30% | Outputs are correct and verifiable |
| Completeness | 20% | All requirements met, no missing elements |
| Documentation | 15% | Skill manifest, prompt, and examples complete |
| Tests | 20% | Test suite passes with good coverage |
| Constitution | 15% | Follows Article II-IV rules |

## Skill Registration Flow

```
1. Skill created in skills/{domain}/
2. Manifest validated against schema
3. Tests run via Skill Tester
4. QA Engine evaluates using rubric
5. Governor approves final QA status
6. Skill registered in registry (skills/registry_index.json)
```

## Domain Structure

Each department has its own skill directory with domain-specific skill types:

| Department | Skill Domains |
|------------|---------------|
| Engineering | `android_development`, `backend_development`, `system_architecture`, `ci_cd_pipeline` |
| Media | `research`, `scriptwriting`, `publishing_optimization`, `video_production` |
| Business | `strategic_planning`, `financial_modeling`, `market_analysis`, `revenue_strategy` |
| Research | `data_analysis`, `statistical_modeling`, `knowledge_discovery`, `experiment_design` |
| Animation | `character_rigging`, `3d_modeling`, `texturing`, `asset_creation` |
| Operations | `process_automation`, `workflow_optimization`, `monitoring`, `workflow_definition` |
| Knowledge | `documentation_creation`, `taxonomy_management`, `knowledge_dist`, `versioning` |
| Infrastructure | `infrastructure_management`, `ci_cd_pipeline`, `deployment`, `security` |
| Improvement | `performance_analysis`, `metrics_visualization`, `optimization_recommendation` |

## Example Skill: video_production

```markdown
skill_id: "video_production"
version: "1.0.0"
owner: "video-agent@media@vjsos-ai"
domain: "media"
type: "generation"
description: "Transform a script + style guide into a timed shot list"
inputs:
  script:
    type: string
    required: true
    description: "Full script text with scenes, dialogue, and timing cues"
outputs:
  shot_list:
    type: object
    required: true
    description: "JSON shot list with all render instructions"
tests:
  - "test_shot_list_generation.yaml"
qa_status: "verified"
```

## CLI Usage

```bash
# List skills
python scripts/skills_cli.py list

# Register a new skill
python scripts/skills_cli.py register skills/media/new_skill

# Run skill tests
python scripts/skills_cli.py test new_skill

# Get skill details
python scripts/skills_cli.py get new_skill
```

---

## Governance

Skills follow Constitution Articles:

- **Article I**: Mission alignment required
- **Article IV**: Department ownership
- **Article V**: QA verification before deployment
- **Article VI**: Governor final approval