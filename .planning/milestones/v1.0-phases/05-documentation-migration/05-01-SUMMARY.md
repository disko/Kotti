---
phase: 05-documentation-migration
plan: 01
subsystem: docs
tags: [mkdocs, mkdocs-material, mkdocstrings, mike, readthedocs, sphinx-removal]

# Dependency graph
requires:
  - phase: 04-code-quality-and-formatting
    provides: Clean codebase ready for documentation; ruff-formatted source for mkdocstrings introspection
provides:
  - MkDocs site scaffold with Kotti Amber Heritage brand theme
  - Full navigation structure with 52 stub markdown pages
  - mkdocstrings plugin configured for Sphinx docstring style
  - Social cards plugin (CI-only), mike version selector, Mermaid fences
  - .readthedocs.yaml v2 config pointing to mkdocs.yml
  - MkDocs optional-deps replacing Sphinx in pyproject.toml
affects:
  - 05-02 (content migration — stub pages ready for pandoc replacement)
  - 05-03 (mkdocstrings API docs — plugin already configured)

# Tech tracking
tech-stack:
  added:
    - mkdocs-material[imaging]>=9.5
    - mkdocstrings[python]>=0.24
    - mike>=2.0
  patterns:
    - Brand kit applied as skin over Material for MkDocs base
    - Social plugin disabled locally via !ENV [CI, false] to avoid cairosvg deps
    - navigation.indexes enables section index pages (api/index.md, kotti.views/index.md)
    - Stub pages (# Title + *Content pending migration.*) prevent nav build failures

key-files:
  created:
    - mkdocs.yml
    - .readthedocs.yaml
    - docs/overrides/partials/logo.html
    - docs/stylesheets/kotti.css
    - docs/assets/ (7 SVG files)
    - docs/index.md
    - docs/guides/ (23 stub pages)
    - docs/api/ (18 + 10 + 4 stub pages across nested structure)
    - docs/community/ (3 stub pages)
  modified:
    - pyproject.toml (docs group: Sphinx → MkDocs deps)
    - uv.lock (new docs deps)
  deleted:
    - rtd.txt (legacy Sphinx-era RTD requirements)

key-decisions:
  - "mkdocs build --strict exits 0 in 0.21s — build gate confirmed green"
  - "MkDocs 2.0 / Material incompatibility warning is advisory only; does not fail build"
  - "navigation.indexes added to features (not in brand kit default) for section index page support"
  - "mike version provider configured in extra.version (not .method — deprecated in Material 7.x)"
  - "Social plugin enabled only in CI via !ENV [CI, false] to avoid local cairosvg system deps"
  - "Stub API pages have no ::: directives — mkdocstrings not invoked until plan 03"

patterns-established:
  - "Stub page pattern: # Title + *Content pending migration.* — safe nav placeholder"
  - "Brand kit application: copy mkdocs.yml from kotti-brand/, then extend rather than start fresh"

requirements-completed: [DOC-01, DOC-02]

# Metrics
duration: 3min
completed: 2026-02-28
---

# Phase 5 Plan 01: MkDocs Scaffold Summary

**MkDocs site scaffolded with Kotti Amber Heritage brand skin, full nav (52 stub pages), mkdocstrings plugin, and ReadTheDocs v2 config — `mkdocs build --strict` exits 0**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-02-28T09:26:02Z
- **Completed:** 2026-02-28T09:28:47Z
- **Tasks:** 2
- **Files modified:** 73

## Accomplishments

- Brand kit (mkdocs.yml, kotti.css, logo.html, 7 SVG assets) copied from kotti-brand/ to docs/
- All 52 stub markdown pages created covering full nav tree (guides, api, community)
- mkdocstrings plugin configured; Sphinx/docutils/repoze.sphinx.autointerface removed from pyproject.toml
- .readthedocs.yaml v2 created; legacy rtd.txt removed; uv.lock updated
- `mkdocs build --strict` verified: exit code 0, 0.21s build time

## Task Commits

Each task was committed atomically:

1. **Task 1: Copy brand kit and create docs directory structure** - `1378fdd2` (feat)
2. **Task 2: Update pyproject.toml docs group and create .readthedocs.yaml** - `84641baf` (feat)

**Plan metadata:** (docs commit pending)

## Files Created/Modified

- `mkdocs.yml` - Full MkDocs config: brand theme, plugins (mkdocstrings, social, search), complete nav, Mermaid fences, mike version selector
- `.readthedocs.yaml` - ReadTheDocs v2 config pointing to mkdocs.yml, pip install of docs extras
- `pyproject.toml` - docs group updated in both [project.optional-dependencies] and [dependency-groups]
- `uv.lock` - Updated with mkdocs-material, mkdocstrings, mike, and all transitive deps
- `docs/overrides/partials/logo.html` - Inline SVG logo partial for nav
- `docs/stylesheets/kotti.css` - Amber Heritage brand skin (CSS custom properties overriding Material)
- `docs/assets/*.svg` - 7 brand SVG assets (mark-dark, mark-light, mark-mono-white, favicon, wordmark variants)
- `docs/index.md` - Homepage placeholder
- `docs/guides/**/*.md` - 23 stub pages (getting-started: 6, user-guide: 17)
- `docs/api/**/*.md` - 32 stub pages (18 top-level, 10 kotti.views, 4 kotti.views.edit)
- `docs/community/*.md` - 3 stub pages (help, contributing, changelog)

## Decisions Made

- Added `navigation.indexes` feature (not in brand kit default) — required for section index pages (api/index.md, kotti.views/index.md) to function as section landing pages
- Social plugin: `enabled: !ENV [CI, false]` — avoids cairosvg system dependency on local macOS builds
- mike `extra.version.provider` (not `.method`) — brand kit used correct modern key already
- Stub API pages contain no `::: module` directives — mkdocstrings invocation deferred to plan 03 to allow build without kotti importable

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

- MkDocs 2.0 / Material for MkDocs incompatibility advisory warning appears in build output. This is a Material theme banner about MkDocs 2.x incompatibility, not a build error. Exit code is 0 and `--strict` does not treat it as a warning that fails the build.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `mkdocs build --strict` is green — content migration (plan 02) can begin immediately
- All 52 stub pages are nav-registered and build successfully — pandoc-converted content can replace stubs one page at a time
- mkdocstrings plugin is configured — adding `::: module` directives in plan 03 is a drop-in addition
- Sphinx deps fully removed from pyproject.toml — no conflicts

---
*Phase: 05-documentation-migration*
*Completed: 2026-02-28*
