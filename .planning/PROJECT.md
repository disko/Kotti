# Kotti Modernization

## What This Is

Kotti is a Pyramid-based CMS framework published on PyPI, now modernized with pyproject.toml packaging, Python 3.10-3.13 support, nh3 sanitization, ruff linting/formatting, and MkDocs Material documentation. Backwards compatibility maintained through deprecation warnings.

## Core Value

Keep Kotti installable, functional, and maintainable on modern Python (3.10-3.13) without breaking existing users — every change must go through a deprecation path.

## Requirements

### Validated

- ✓ Hierarchical content tree with traversal-based routing — existing
- ✓ ACL-based security with local group assignments — existing
- ✓ SQLAlchemy ORM persistence (SQLite, PostgreSQL, MySQL) — existing
- ✓ Content type system with TypeInfo registry — existing
- ✓ Event-driven architecture (insert, update, delete lifecycle) — existing
- ✓ Form handling via colander/deform schemas — existing
- ✓ File upload/storage via filedepot — existing
- ✓ User/group management with role-based permissions — existing
- ✓ Internationalization (i18n) with Babel — existing
- ✓ Plugin architecture via includeme hooks — existing
- ✓ Alembic database migrations — existing
- ✓ Chameleon template rendering — existing
- ✓ PyPI package distribution — existing
- ✓ GitHub Actions CI with multi-DB testing — existing
- ✓ pyproject.toml with hatchling build backend and src layout — v1.0
- ✓ uv as package manager with committed lock file — v1.0
- ✓ ruff for linting and formatting (replaces flake8/isort/black) — v1.0
- ✓ Python 3.10-3.13 support, 3.6-3.9 dropped — v1.0
- ✓ nh3 sanitization (replaces deprecated bleach) — v1.0
- ✓ importlib.metadata/resources (replaces pkg_resources) — v1.0
- ✓ Consolidated CI matrix (Python x DB backend) — v1.0
- ✓ pre-commit hooks for code quality — v1.0
- ✓ MkDocs Material documentation with mkdocstrings API docs — v1.0
- ✓ Deprecation warnings for all changed public APIs — v1.0

### Active

(None — next milestone requirements TBD via `/gsd:new-milestone`)

### Out of Scope

- Replacing fanstatic/js.* asset pipeline — too complex, needs its own milestone
- Replacing Angular 1.x — frontend overhaul is a separate effort
- Upgrading to Pyramid 2.0 — major API changes, deserves dedicated milestone
- Replacing pyramid_beaker sessions — requires evaluating alternatives, separate effort
- Removing ZCML support — breaking change for plugins, needs deprecation planning
- Replacing FormEncode with colander — used in email validation, risk of subtle breakage
- Performance optimization — separate effort after modernization

## Context

Kotti is a mature Pyramid-based CMS framework (version 2.0.10dev0) published on PyPI. After v1.0 modernization:
- 17,000 LOC Python across src/kotti/
- Test suite using pytest with SQLite/PostgreSQL/MySQL backends
- MkDocs Material documentation with mkdocstrings API reference
- GitHub Actions CI: consolidated matrix (Python 3.10-3.13 x 3 DB backends)
- pyproject.toml + hatchling + src layout + uv.lock
- ruff linting/formatting + pre-commit hooks
- nh3 sanitization, importlib.metadata/resources
- All entry points working (paste.app_factory, console_scripts, fanstatic, pytest11)

Known tech debt:
- Pyramid pinned to <2 (pyramid.compat dependency)
- SQLAlchemy pinned to <2 (declarative_base, baked queries)
- 3 pre-existing test_file.py failures (depot/cgi FieldStorage issue)
- fanstatic/Angular 1.x frontend stack unchanged

## Constraints

- **Backwards compatibility**: Must use deprecation warnings before removing/changing public APIs
- **PyPI publication**: Package must remain installable via pip throughout
- **Entry points**: paste.app_factory, fanstatic.libraries, console_scripts, pytest11 must work
- **Plugin compatibility**: includeme hooks and configuration patterns must remain functional
- **Test suite**: All existing tests must pass after changes (or updated with clear rationale)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python 3.10-3.13 target | Drop EOL versions, use modern syntax | ✓ Good — all tests pass |
| pyproject.toml + src layout | Modern Python packaging standard | ✓ Good — clean build |
| uv as package manager | Fast, modern, replaces pip/pip-tools | ✓ Good — lock file committed |
| ruff for linting + formatting | Replaces flake8, isort, black — single tool | ✓ Good — 441 violations fixed |
| Deprecation cycle for breaking changes | Protect existing users | ✓ Good — shims in sanitizers |
| Replace bleach with nh3 | bleach deprecated, nh3 is maintained | ✓ Good — characterization tests pass |
| hatchling over setuptools | Modern, handles src layout natively | ✓ Good — all assets included |
| MkDocs Material over Sphinx update | Modern, better DX, mkdocstrings for API docs | ✓ Good — 52 pages, strict build passes |
| Isolated formatting commit | Preserves git blame via .git-blame-ignore-revs | ✓ Good — GitHub auto-skips |
| Keep pyramid<2 and sqlalchemy<2 pins | Too risky for this milestone | ⚠️ Revisit — future milestone |

---
*Last updated: 2026-02-28 after v1.0 milestone*
