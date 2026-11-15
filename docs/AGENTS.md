# VJSOS-AI Agent Directory

**Version:** 1.0.0
**Constitution Article:** V
**Governance:** Department Directors (Governor-approved)

---

## 1. Core Kernel Agents

### 1.1 System Governor

**Agent ID:** `governor@vjsos-ai`  
**Type:** singleton  
**Memory Tier:** global  
**Department:** N/A  

**Mission:** Enforce constitutional compliance, maintain architectural integrity, resolve conflicts, approve agent/skill lifecycle events, control memory growth, trigger refactoring.

**Prompt:** `kernel/governor/governor.md`

---

### 1.2 Orchestrator

**Agent ID:** `orchestrator@vjsos-ai`  
**Type:** singleton  
**Memory Tier:** global  
**Department:** N/A  

**Mission:** Coordinate all task execution. Decompose user requests, select departments and agents, build context packages, manage QA gates, assemble final output.

**Prompt:** `kernel/orchestrator/orchestrator.md`

---

### 1.3 Context Engine

**Agent ID:** `context-engine@vjsos-ai`  
**Type:** singleton  
**Memory Tier:** global  
**Department:** N/A  

**Mission:** Build minimal, relevant context packages for agents. Eliminate context bloat. Maximize signal-to-noise ratio.

**Prompt:** `kernel/context-engine/context-engine.md`

---

### 1.4 Memory Engine

**Agent ID:** `memory-engine@vjsos-ai`  
**Type:** singleton  
**Memory Tier:** global  
**Department:** N/A  

**Mission:** Manage the four-tier memory model. Enforce lifecycles. Deduplicate. Index. Serve retrieval requests from Context Engine and directly-authorized agents.

**Prompt:** `kernel/memory-engine/memory-engine.md`

---

### 1.5 QA Engine

**Agent ID:** `qa-engine@vjsos-ai`  
**Type:** singleton  
**Memory Tier:** global  
**Department:** N/A  

**Mission:** Independent quality verification. Every agent output must pass QA before reaching the user or persistent storage. Coordinate department-specific QA agents.

**Prompt:** `kernel/qa-engine/qa-engine.md`

---

## 2. Department Directory Structure

### 2.1 Engineering Department

#### Core Agents

**`android-agent@engineering@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** android, kotlin, compose, android-studio
- **Skills:** android_development, anr_analysis, performance_optimization, debugging, testing, architecture_design
- **Prompt:** `agents/engineering/android.md`
- **QA Agent:** `qa-engineering@vjsos-ai`

**`backend-agent@engineering@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** backend, apis, databases, microservices
- **Skills:** api_design, database_architecture, microservices, testing, documentation, observability
- **Prompt:** `agents/engineering/backend.md`
- **QA Agent:** `qa-engineering@vjsos-ai`

**`infrastructure-agent@engineering@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** ci-cd, automation, devops, monitoring
- **Skills:** ci-cd_pipeline, automation, monitoring, security, testing, documentation
- **Prompt:** `agents/engineering/infrastructure.md`
- **QA Agent:** `qa-engineering@vjsos-ai`

**`code-review-agent@engineering@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** code-review, architecture, standards
- **Skills:** code_review, architecture_validation, standards_enforcement, documentation, testing
- **Prompt:** `agents/engineering/code-review.md`
- **QA Agent:** `qa-engineering@vjsos-ai`

### 2.2 Media Department

#### Core Agents

**`research-agent@media@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** research, fact-checking, verification
- **Skills:** research, fact-checking, source_verification, citation_management, documentation
- **Prompt:** `agents/media/research.md`
- **QA Agent:** `qa-media@vjsos-ai`

**`script-agent@media@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** writing, editing, formatting
- **Skills:** script_writing, editing, formatting, documentation, qa_review
- **Prompt:** `agents/media/script.md`
- **QA Agent:** `qa-media@vjsos-ai`

**`publishing-agent@media@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** publishing, optimization, distribution
- **Skills:** content_formatting, seo_optimization, distribution, documentation, quality_check
- **Prompt:** `agents/media/publishing.md`
- **QA Agent:** `qa-media@vjsos-ai`

### 2.3 Business Department

#### Core Agents

**`strategy-agent@business@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** strategy, analysis, planning
- **Skills:** strategic_planning, market_analysis, financial_modeling, competitive_analysis, documentation
- **Prompt:** `agents/business/strategy.md`
- **QA Agent:** `qa-business@vjsos-ai`

**`revenue-agent@business@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** revenue, finance, pricing
- **Skills:** revenue_strategy, financial_planning, pricing_models, market_analysis, documentation
- **Prompt:** `agents/business/revenue.md`
- **QA Agent:** `qa-business@vjsos-ai`

### 2.4 Research Department

#### Core Agents

**`data-analyst-agent@research@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** data-analysis, statistics, visualization
- **Skills:** data_analysis, statistical_modeling, visualization, reporting, documentation
- **Prompt:** `agents/research/data-analyst.md`
- **QA Agent:** `qa-research@vjsos-ai`

**`knowledge-agent@research@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** knowledge-management, organization, discovery
- **Skills:** knowledge_organization, categorization, information_discovery, documentation, quality_assurance
- **Prompt:** `agents/research/knowledge.md`
- **QA Agent:** `qa-knowledge@vjsos-ai`

### 2.5 Animation Department

#### Core Agents

**`rigging-agent@animation@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** rigging, animation, character_control
- **Skills:** character_rigging, animation_controls, skinning, testing, documentation
- **Prompt:** `agents/animation/rigging.md`
- **QA Agent:** `qa-animation@vjsos-ai`

**`modeling-agent@animation@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** modeling, texturing, asset_creation
- **Skills:** 3d_modeling, texturing, asset_creation, quality_check, documentation
- **Prompt:** `agents/animation/modeling.md`
- **QA Agent:** `qa-animation@vjsos-ai`

### 2.6 Operations Department

#### Core Agents

**`automation-agent@operations@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** automation, workflows, process_optimization
- **Skills:** process_automation, workflow_optimization, monitoring, testing, documentation
- **Prompt:** `agents/operations/automation.md`
- **QA Agent:** `qa-automation@vjsos-ai`

### 2.7 Knowledge Department

#### Core Agents

**`documentation-agent@knowledge@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** documentation, organization, accessibility
- **Skills:** documentation_creation, organization, knowledge_dist, quality_check, versioning
- **Prompt:** `agents/knowledge/documentation.md`
- **QA Agent:** `qa-knowledge@vjsos-ai`

### 2.8 Infrastructure Department

#### Core Agents

**`devops-agent@infrastructure@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** infrastructure, ci-cd, deployment
- **Skills:** infrastructure_management, ci-cd_pipeline, deployment, monitoring, security
- **Prompt:** `agents/infrastructure/devops.md`
- **QA Agent:** `qa-infrastructure@vjsos-ai`

### 2.9 Improvement Department

#### Core Agents

**`performance-agent@improvement@vjsos-ai`**
- **Type:** Worker
- **Memory Tier:** agent
- **Domains:** performance-analysis, metrics, analysis
- **Skills:** performance_analysis, metrics_visualization, improvement_identification, reporting, documentation
- **Prompt:** `agents/improvement/performance.md`
- **QA Agent:** `qa-improvement@vjsos-ai`

---

## 3. Department Director Agents

### 3.1 Engineering Director

**Agent ID:** `director-engineering@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** engineering
- **Authority:** Agent approval, skill validation, QA standards
- **Prompt:** `agents/directors/engineering.md`

### 3.2 Media Director

**Agent ID:** `director-media@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** media
- **Authority:** Content approval, script validation, publishing standards
- **Prompt:** `agents/directors/media.md`

### 3.3 Business Director

**Agent ID:** `director-business@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** business
- **Authority:** Revenue model approval, market strategy, budget allocation
- **Prompt:** `agents/directors/business.md`

### 3.4 Research Director

**Agent ID:** `director-research@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** research
- **Authority:** Research standards, data validation, publication
- **Prompt:** `agents/directors/research.md`

### 3.5 Animation Director

**Agent ID:** `director-animation@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** animation
- **Authority:** Animation standards, pipeline compliance, quality control
- **Prompt:** `agents/directors/animation.md`

### 3.6 Operations Director

**Agent ID:** `director-operations@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** operations
- **Authority:** Process standards, automation approval, efficiency metrics
- **Prompt:** `agents/directors/operations.md`

### 3.7 Knowledge Director

**Agent ID:** `director-knowledge@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** knowledge
- **Authority:** Knowledge standards, taxonomy, documentation
- **Prompt:** `agents/directors/knowledge.md`

### 3.8 Infrastructure Director

**Agent ID:** `director-infrastructure@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** infrastructure
- **Authority:** Infrastructure standards, tool approval, platform management
- **Prompt:** `agents/directors/infrastructure.md`

### 3.9 Improvement Director

**Agent ID:** `director-improvement@vjsos-ai`
- **Type:** Director
- **Memory Tier:** department
- **Department:** improvement
- **Authority:** Improvement standards, process changes, optimization
- **Prompt:** `agents/directors/improvement.md`

---

## 4. QA Agents

### 4.1 Engineering QA

**Agent ID:** `qa-engineering@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** engineering
- **Authority:** Code quality standards, testing requirements
- **Prompt:** `agents/qa/engineering.md`

### 4.2 Media QA

**Agent ID:** `qa-media@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** media
- **Authority:** Content standards, story quality
- **Prompt:** `agents/qa/media.md`

### 4.3 Business QA

**Agent ID:** `qa-business@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** business
- **Authority:** Business standards, strategy quality
- **Prompt:** `agents/qa/business.md`

### 4.4 Animation QA

**Agent ID:** `qa-animation@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** animation
- **Authority:** Animation quality standards
- **Prompt:** `agents/qa/animation.md`

### 4.5 Research QA

**Agent ID:** `qa-research@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** research
- **Authority:** Research standards, data quality
- **Prompt:** `agents/qa/research.md`

### 4.6 Infrastructure QA

**Agent ID:** `qa-infrastructure@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** infrastructure
- **Authority:** Infrastructure standards, reliability
- **Prompt:** `agents/qa/infrastructure.md`

### 4.7 Knowledge QA

**Agent ID:** `qa-knowledge@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** knowledge
- **Authority:** Knowledge standards, documentation quality
- **Prompt:** `agents/qa/knowledge.md`

### 4.8 Operations QA

**Agent ID:** `qa-operations@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** operations
- **Authority:** Operations standards, process compliance
- **Prompt:** `agents/qa/operations.md`

### 4.9 Improvement QA

**Agent ID:** `qa-improvement@vjsos-ai`
- **Type:** QA
- **Memory Tier:** global
- **Department:** improvement
- **Authority:** Improvement standards, performance metrics
- **Prompt:** `agents/qa/improvement.md`

---

## 5. Example Agent Implementation

### Example: `android-agent@engineering@vjsos-ai`

**Directory Structure:**
```
agents/
├── engineering/
│   ├── android-agent@vjsos-ai.md  # Manifest
│   ├── android.md                 # Prompt (implementation)
│   ├── skills/
│   │   └── android-development/   # Skill package
│   └── tests/                     # Automated tests
```

**Manifest (`android-agent@vjsos-ai.md`):**
```yaml
agent_id: "android-agent@engineering@vjsos-ai"
type: "worker"
department: "engineering"
director: "director-engineering@vjsos-ai"
mission: "Build and maintain Android applications following VJSOS quality standards"
domains: ["android", "kotlin", "compose"]
skills: ["android_development", "anr_analysis", "performance_optimization", "debugging", "testing", "architecture_design"]
memory_scope: "agent"
qa_rubric: "engineering_qa_rubric_v2.0"
status: "operational"
version: "2.3.1"
```

---

## 6. Agent Communication Protocol

### 6.1 Message Formats

```json
{
  "message_id": "uuid",
  "timestamp": "ISO8601",
  "source": "agent_id",
  "target": "orchestrator | director | agent_id | qa_engine",
  "type": "request | response | event | escalation",
  "payload": {},
  "correlation_id": "uuid",
  "priority": "low | normal | high | critical",
  "ttl": "duration"
}
```

### 6.2 Communication Rules (Constitution Article VII)

- **All messages** flow through the Orchestrator (or via department director for intra-department)
- **No direct agent-to-agent calls** (except QA → worker for feedback)
- **Escalations** go to Governor
- **System events** broadcast on kernel bus

---

## 7. Agent Lifecycle

```
PROPOSAL (RFC submitted)
    ↓
GOVERNOR APPROVAL
    ↓
MANIFEST CREATION (agent.md + prompt.md)
    ↓
SKILL REGISTRATION
    ↓
MEMORY INITIALIZATION
    ↓
ONBOARDING (learning package)
    ↓
QA VERIFICATION
    ↓
OPERATIONAL
    ↓
PERFORMANCE MONITORING
    ↓
(OPERATIONAL | DEPRECATED | SUSPENDED | EVOLVED)
```

---

**End of Agent Directory Specification**