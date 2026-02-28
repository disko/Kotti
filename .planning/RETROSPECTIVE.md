# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — Kotti Modernization

**Shipped:** 2026-02-28
**Phases:** 5 | **Plans:** 12 | **Sessions:** ~5

### What Was Built
- pyproject.toml + hatchling + src layout + uv.lock (replacing setup.py/setup.cfg/tox.ini)
- nh3 sanitization with deprecation shims for bleach API compatibility
- Consolidated CI matrix: Python 3.10-3.13 x SQLite/PostgreSQL/MySQL
- ruff linting/formatting (441 violations fixed) + pre-commit hooks
- MkDocs Material docs with mkdocstrings API reference (52 pages, 32 API modules)
- importlib.metadata/resources replacing pkg_resources throughout

### What Worked
- Strict phase ordering (packaging → deps → CI → quality → docs) prevented cascading issues
- Characterization tests before bleach→nh3 switch caught CSS normalization differences early
- Isolated formatting commit with .git-blame-ignore-revs preserved git history usability
- Wave-based parallel execution for docs migration (plans 02+03 in parallel) saved time
- yolo mode kept flow uninterrupted across all phases

### What Was Inefficient
- Phase 2 plan 01 was overly broad (characterization tests + importlib + mock + pins in one plan)
- Some stub-then-fill pattern in docs (plan 01 created 52 stubs, plans 02-03 replaced them) — could have been 2 plans instead of 4
- VERIFICATION.md griffe warnings required source docstring fixes that should have been in phase 4

### Patterns Established
- `# noqa: RUF012` for SQLAlchemy/Pyramid class-level mutables (framework-managed, not bugs)
- `# noqa: E711` for SQLAlchemy ORM `== None` filters (required by SQL generation)
- B018 per-file-ignored in tests (intentional property-access side effects are valid test patterns)
- Social cards plugin gated with `!ENV [CI, false]` to avoid cairosvg system deps locally

### Key Lessons
1. Always run characterization tests before replacing a sanitization library — behavioral differences are subtle (CSS semicolons, tag normalization)
2. Formatting changes should always be isolated commits with .git-blame-ignore-revs — mixing with functional changes makes review impossible
3. mkdocstrings requires Sphinx-compatible docstring format (`:param type name:`) — griffe 2.0 rejects split `:param:` + `:type:` pairs
4. Pre-existing test failures should be documented in STATE.md blockers immediately — they cause confusion in every subsequent phase

### Cost Observations
- Model mix: ~10% opus (orchestration), ~90% sonnet (execution/verification)
- Sessions: ~5 sessions across 2 days
- Notable: Phase 3 (CI modernization) completed in 1m 26s — simplest phase by far

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | ~5 | 5 | Initial modernization — established packaging/CI/quality baselines |

### Cumulative Quality

| Milestone | Plans | Files Changed | LOC Delta |
|-----------|-------|---------------|-----------|
| v1.0 | 12 | 381 | +18,506/-7,077 |

### Top Lessons (Verified Across Milestones)

1. Strict phase ordering prevents cascading failures in modernization projects
2. Characterization tests before library replacements catch subtle behavioral changes
