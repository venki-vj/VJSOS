# RFC 0001: Orchestrator Registry Bootstrap

**Status:** DRAFT
**Category:** Infrastructure
**Created:** 2026-08-07
**Governor Approval:** Required

## Summary

This RFC proposes a standardized registry bootstrap mechanism for the Orchestrator to automatically discover and register departments and agents at startup.

## Motivation

Currently, the `Orchestrator.__init__` initializes empty registries:
```python
self.department_registry = {}
self.agent_registry = {}
```

This requires manual registration via `main()` test function, making the orchestrator unusable out of the box.

## Proposed Solution

Add a `RegistryBootstrap` class that:

1. **Discovers** department manifests from `departments/*/` MANIFEST.md
2. **Parses** agent definitions from `docs/AGENTS.md` and department manifests
3. **Registers** departments and agents with the Orchestrator on initialization

### Implementation Sketch

```python
class RegistryBootstrap:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        
    def bootstrap(self):
        self._load_departments()
        self._load_agents()
        
    def _load_departments(self):
        for dept_dir in Path("departments").iterdir():
            if dept_dir.is_dir() and (dept_dir / "MANIFEST.md").exists():
                dept = self._parse_department_manifest(dept_dir)
                self.orchestrator.register_department(dept)
                
    def _load_agents(self):
        # Parse from AGENTS.md and department MANIFESTs
        pass
```

## Alternatives

- **Option A:** Manual registration only (current state)
- **Option B:** Environment variable with JSON config
- **Option C:** REST API registration endpoint

## Impact

- **Positive:** Orchestrator works out of the box
- **Positive:** Reduces startup boilerplate
- **Risk:** May load unregistered agents/departments

## Security Considerations

- Only manifests with valid Governor hashes can be registered
- Cross-department agents require Governor approval
- All registrations logged for audit

## Timeline

- Week 1: Implement `RegistryBootstrap` class
- Week 1: Integration with Orchestrator `__init__`
- Week 2: Tests for registration flow
- Week 2: Documentation in `docs/AGENTS.md`