# Phase 4: Code Quality and Formatting - Context

**Gathered:** 2026-02-28
**Status:** Ready for planning

<domain>
## Phase Boundary

The codebase passes ruff with zero violations, type annotation anti-patterns are corrected, and developer tooling (pre-commit) is configured for ongoing hygiene. Covers requirements LNT-01 through LNT-06 and CQ-01 through CQ-04.

</domain>

<decisions>
## Implementation Decisions

### Ruff rule selection
- Comprehensive rule set: pyflakes (F), pycodestyle (E/W), isort (I), bugbear (B), pyupgrade (UP), SIM, RUF
- Auto-fix all safe fixes; review unsafe fixes manually
- Adopt ruff defaults over existing codebase conventions
- Line length: 88 (ruff/Black default)

### Formatting commit strategy
- First commit in the phase is pure formatting: ruff format + isort applied to entire codebase
- Single commit covering all code (not split by package)
- Set up .git-blame-ignore-revs with .gitattributes config so git blame skips the formatting commit automatically
- Config first approach not needed — formatting commit comes first

### Pre-commit hook scope
- Hooks: ruff (lint + format), trailing-whitespace, end-of-file-fixer, check-yaml, check-merge-conflict, check-added-large-files, check-toml, debug-statements
- Hooks block the commit on failure (standard enforcement)
- Pre-commit also runs in CI (`pre-commit run --all-files`) as a check
- Pin hook versions to specific tags/SHAs for reproducibility

### Code cleanup boundaries
- Code duplication removal (CQ-04): conservative — only exact or near-exact repeated blocks, no refactoring for DRY-ness
- pyupgrade modernizations (LNT-05): all safe modernizations — super() without args, X | None union syntax, f-strings, etc. (Python 3.10+ target makes all safe)
- Type annotations (CQ-02): modernize to X | None syntax, replace Union[X, None] and Optional[X], add `from __future__ import annotations` where needed
- Deprecation warnings (CQ-03): add DeprecationWarning for any public API changes made during this phase

### Claude's Discretion
- Bare except handler replacements (CQ-01): Claude reads each handler in alembic/env.py and views/cache.py and picks the most appropriate specific exception type
- Exact ruff rule configuration details beyond the selected rule sets
- Order of linting fix commits after the initial formatting commit

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches. User consistently chose recommended/standard practices throughout discussion.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-code-quality-and-formatting*
*Context gathered: 2026-02-28*
