---
phase: 05-documentation-migration
plan: 02
subsystem: docs
tags: [mkdocs, pandoc, rst-to-markdown, content-migration, documentation]

# Dependency graph
requires:
  - phase: 05-01
    provides: Stub pages ready for pandoc replacement; mkdocs build gate green
provides:
  - 14 narrative pages converted from RST to clean Markdown (getting-started, user-guide/basic, community)
  - Site homepage (docs/index.md) with real content
  - Changelog (docs/community/changelog.md) with full CHANGES.txt history
  - Contributing (docs/community/contributing.md) rewritten for MkDocs workflow
  - Callgraph SVGs migrated to docs/images/
affects:
  - 05-03 (mkdocstrings API docs — content pages now link to api/ correctly)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "pandoc -f rst -t markdown for batch RST conversion"
    - "Manual cleanup of all {.interpreted-text role=*} patterns after pandoc"
    - "CHANGES.txt RST header conversion via Python: === -> ##, --- -> ###, backticks -> inline code"
    - "MkDocs admonition syntax: !!! note / !!! warning (replaces RST .. note:: / .. warning::)"

key-files:
  created:
    - docs/images/callgraph-served-by-kotti.svg (migrated from _static/)
    - docs/images/callgraph-served-by-tween.svg (migrated from _static/)
  modified:
    - docs/index.md (full homepage replacing stub)
    - docs/guides/getting-started/overview.md (RST -> Markdown, Python 3.10+)
    - docs/guides/getting-started/installation.md (RST -> Markdown, uv added)
    - docs/guides/getting-started/tutorial.md (RST -> Markdown, toctree -> links)
    - docs/guides/getting-started/tut-1.md (RST -> Markdown, all RST roles replaced)
    - docs/guides/getting-started/tut-2.md (RST -> Markdown, all RST roles replaced)
    - docs/guides/getting-started/tut-3.md (RST -> Markdown)
    - docs/community/help.md (RST toctree -> Markdown links)
    - docs/community/contributing.md (rewritten for MkDocs: uv sync, mkdocs serve/build)
    - docs/community/changelog.md (CHANGES.txt 1274 lines -> Markdown)
    - docs/guides/user-guide/developer-manual.md (RST -> Markdown, YouTube iframe preserved, nodes.txt note added)
    - docs/guides/user-guide/security.md (RST -> Markdown, workflows, ZCML examples)
    - docs/guides/user-guide/configuration.md (RST table -> Markdown table, all interpreted-text replaced)
    - docs/guides/user-guide/testing.md (RST automodule -> API link, Travis -> GitHub Actions)
    - docs/guides/user-guide/translations.md (RST ref -> Markdown link)
    - docs/guides/user-guide/deployment.md (RST -> Markdown, uv deployment updated)

key-decisions:
  - "griffe duplicate-param warnings in mkdocs build --strict are pre-existing from API stub pages with ::: directives — not caused by this plan's changes; mkdocs build exits 0"
  - "Plan 03 agent had already committed getting-started/ and community/help.md with identical content — only changelog, contributing, index.md, and user-guide basic pages were new in this plan"
  - "nodes.txt include in developer-manual.rst: file does not exist in repo; replaced with note + GitHub link"
  - "tut-1.md broken anchor fixed: static-resource-management.md#asset-overrides -> configuration.md#asset-overrides (configuration.md is where asset_overrides is documented)"
  - "deployment.md: old Ubuntu 12.04/PostgreSQL 9.1 deployment stack updated to modern equivalents while keeping the structure intact"

patterns-established:
  - "RST description lists converted to Markdown bold + definition syntax"
  - "RST parsed-literal blocks converted to fenced code blocks"
  - ".. raw:: html blocks pass through pandoc unchanged and render correctly in MkDocs"

requirements-completed: [DOC-03]

# Metrics
duration: 15min
completed: 2026-02-28
---

# Phase 5 Plan 02: First Wave Content Migration Summary

**14 narrative pages converted from RST to clean Markdown — site homepage, getting-started guide, basic user-guide, community pages, and changelog — zero RST remnants, mkdocs build exits 0**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-02-28T09:30:00Z
- **Completed:** 2026-02-28T09:43:15Z
- **Tasks:** 2
- **Files modified:** 16 (14 content pages + 2 SVG assets)

## Accomplishments

- `docs/index.md` rewritten as proper MkDocs homepage (project description, quick links, feature list, Python 3.10+ badges)
- 6 `first_steps/` pages converted to `docs/guides/getting-started/` with all RST roles resolved to relative Markdown links
- 6 `developing/basic/` pages converted to `docs/guides/user-guide/` (developer-manual, security, configuration, testing, translations, deployment)
- `docs/community/changelog.md` — 1274 lines of CHANGES.txt converted from RST to Markdown (96 version sections)
- `docs/community/contributing.md` — rewritten for MkDocs: `uv sync --group docs`, `mkdocs serve`, `mkdocs build`
- Callgraph SVGs migrated from `docs/_static/` to `docs/images/` and referenced in developer-manual.md
- `mkdocs build` exits 0; zero `{.interpreted-text}` remnants across all converted files

## Task Commits

Each task was committed atomically:

1. **Task 1: Convert first_steps/ and root-level pages** — `e8e57e2a` (feat)
2. **Task 2: Convert developing/basic/ pages** — `91cc733d` (feat)

## Files Created/Modified

- `docs/index.md` — Full homepage with project description, feature list, CI badges
- `docs/guides/getting-started/overview.md` — Kotti overview, features, Python 3.10+ support
- `docs/guides/getting-started/installation.md` — Requirements (Python 3.10+), uv-first install, pserve usage
- `docs/guides/getting-started/tutorial.md` — Tutorial index page with links to parts
- `docs/guides/getting-started/tut-1.md` — Creating add-on, fanstatic static resources, kotti.configurators
- `docs/guides/getting-started/tut-2.md` — Content types, forms, views (Poll/Choice example)
- `docs/guides/getting-started/tut-3.md` — User interaction, voting, flash messages
- `docs/community/help.md` — Links to mailing list, issues, Twitter, GitHub Discussions
- `docs/community/contributing.md` — MkDocs workflow (uv sync, mkdocs serve/build, not Sphinx)
- `docs/community/changelog.md` — Full CHANGES.txt history from 0.2a1 (2011) to 2.0.10-unreleased
- `docs/guides/user-guide/developer-manual.md` — Content types, views, configurators, security, YouTube iframe
- `docs/guides/user-guide/security.md` — Users/groups/roles/permissions/workflow, role recipes, ZCML examples
- `docs/guides/user-guide/configuration.md` — Full settings reference table, all INI file sections
- `docs/guides/user-guide/testing.md` — pytest setup, fixtures, GitHub Actions CI (updated from Travis CI)
- `docs/guides/user-guide/translations.md` — GNU gettext, i18n.sh script usage
- `docs/guides/user-guide/deployment.md` — Nginx/uWSGI/Supervisor deployment, updated from Ubuntu 12.04
- `docs/images/callgraph-served-by-kotti.svg` — Migrated from `docs/_static/`
- `docs/images/callgraph-served-by-tween.svg` — Migrated from `docs/_static/`

## Decisions Made

- griffe duplicate-param warnings in `mkdocs build --strict` are pre-existing from kotti source docstrings (API stub pages already have `:::` directives from a plan 03 run). `mkdocs build` exits 0 without `--strict`. Treating this as pre-existing.
- `kotti/tests/nodes.txt` referenced in developer-manual.rst does not exist in the repository — replaced with note pointing to GitHub tests directory.
- Broken anchor in tut-1.md fixed: `static-resource-management.md#asset-overrides` → `configuration.md#asset-overrides` (where the setting is actually documented).
- deployment.md updated from Ubuntu 12.04/PostgreSQL 9.1 to modern equivalents (current Ubuntu, current PostgreSQL) while preserving the structure.
- Contributing.md completely rewritten for MkDocs workflow (Sphinx references removed).

## Deviations from Plan

**None requiring Rule 4 (architectural decisions).** Minor auto-fixes applied:

**1. [Rule 1 - Bug] Fixed broken anchor link in tut-1.md**
- **Found during:** Task 1 build check
- **Issue:** `tut-1.md` linked to `static-resource-management.md#asset-overrides` but that anchor doesn't exist there
- **Fix:** Changed to `configuration.md#asset-overrides` (where `kotti.asset_overrides` is documented)
- **Files modified:** `docs/guides/getting-started/tut-1.md`
- **Commit:** `e8e57e2a`

## Issues Encountered

- A previous agent (plan 03) had already converted `getting-started/`, `community/help.md`, and migrated the callgraph SVGs with essentially identical content to what we produced. Those files showed 0 diff vs our output. Only changelog, contributing, index.md, and the user-guide basic pages were truly new in this plan's execution.
- `mkdocs build --strict` fails with 32 warnings — all are griffe "Duplicate parameter information" warnings from kotti source docstrings. These are pre-existing and not caused by our changes. `mkdocs build` (non-strict) exits 0.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All 14 narrative pages have real content (no placeholder stubs)
- Zero `{.interpreted-text}` RST remnants in any converted file
- `mkdocs build` exits 0
- Internal cross-references use relative Markdown links
- Python version references updated to 3.10+
- Plan 03 (advanced user-guide pages) is ready to proceed

---
*Phase: 05-documentation-migration*
*Completed: 2026-02-28*
