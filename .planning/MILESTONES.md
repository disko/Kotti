# Milestones

## v1.0 Kotti Modernization (Shipped: 2026-02-28)

**Phases completed:** 5 phases, 12 plans, 4 tasks

**Key accomplishments:**
- Migrated from setup.py to pyproject.toml with hatchling build backend and src layout
- Replaced bleach with nh3 for HTML sanitization, pkg_resources with importlib.metadata/resources
- Consolidated 3 CI workflows into 1 matrix (Python 3.10-3.13 x SQLite/PostgreSQL/MySQL)
- Applied ruff formatting + linting (441 violations fixed), added pre-commit hooks
- Migrated all documentation from Sphinx/RST to MkDocs Material with mkdocstrings API docs
- 381 files changed, +18,506/-7,077 lines across 12 plans in 2 days

---

