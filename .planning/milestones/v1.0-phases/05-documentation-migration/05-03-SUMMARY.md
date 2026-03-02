---
phase: 05-documentation-migration
plan: 03
subsystem: docs
tags: [mkdocs, mkdocstrings, pandoc, griffe, sphinx-docstrings, api-reference]

# Dependency graph
requires:
  - phase: 05-01
    provides: MkDocs scaffold with 52 stub pages and mkdocstrings plugin configured

provides:
  - 11 developing/advanced/ RST pages converted to clean Markdown in docs/guides/user-guide/
  - 32 API reference pages with ::: module directives for mkdocstrings introspection
  - API index page with module table (18 modules + kotti.views subpackages)
  - callgraph SVGs copied to docs/images/ for new MkDocs path structure
  - Pre-existing getting-started/ and community/help.md content also committed

affects:
  - 05-04 (final documentation migration — community/changelog pages)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - mkdocstrings API page pattern: "# module.name\n::: module.name\n    options:"
    - Sphinx docstring param pattern: ":param type name: desc" (merged from separate :param/:type)
    - HTML grid for side-by-side images: <div class="grid" markdown>
    - API index page: table with [module](module.md) links and one-line descriptions

key-files:
  created:
    - docs/guides/user-guide/as-a-library.md
    - docs/guides/user-guide/close-to-anonymous.md
    - docs/guides/user-guide/default-views.md
    - docs/guides/user-guide/add-to-edit-interface.md
    - docs/guides/user-guide/events.md
    - docs/guides/user-guide/frontpage-different-template.md
    - docs/guides/user-guide/images.md
    - docs/guides/user-guide/blobs.md
    - docs/guides/user-guide/static-resource-management.md
    - docs/guides/user-guide/understanding-kotti-startup.md
    - docs/guides/user-guide/sanitizers.md
    - docs/images/callgraph-served-by-kotti.svg
    - docs/images/callgraph-served-by-tween.svg
  modified:
    - docs/api/index.md (module table with descriptions)
    - docs/api/kotti.md (and 17 other top-level API pages)
    - docs/api/kotti.views/index.md (and submodule pages)
    - docs/api/kotti.views/kotti.views.edit/index.md (and submodule pages)
    - mkdocs.yml (global members_order: source option)
    - src/kotti/filedepot.py (docstring fix)
    - src/kotti/message.py (docstring fix)
    - src/kotti/request.py (docstring fix)
    - src/kotti/resources.py (docstring fix)
    - src/kotti/sanitizers.py (docstring fix)
    - src/kotti/security.py (docstring fix)

key-decisions:
  - "griffe 2.0 warns on Sphinx :param x: + :type x: (duplicate param info) — fixed by merging into :param type x: pattern in 6 source files"
  - "mkdocstrings-python 2.0.3 has bug: SphinxStyleOptions includes warn_missing_types but griffe parse_sphinx() doesn't accept it — docstring_options config workaround avoided; source fixed instead"
  - "blobs.md side-by-side callgraph images rewritten as HTML grid with docs/images/ path"
  - "members_order: source added to mkdocs.yml global handler options"
  - "API index uses table format with one-line descriptions; no ::: directive (pure navigation)"

patterns-established:
  - "All advanced guide pages: clean Markdown with API links pointing to ../../api/module.md"
  - "Sphinx docstring merging: :param type name: desc (not separate :param + :type entries)"
  - "mkdocstrings page: # title + ::: module + options block (8 lines total)"

requirements-completed: [DOC-03, DOC-04]

# Metrics
duration: 25min
completed: 2026-02-28
---

# Phase 5 Plan 03: Advanced Guides + API Reference Pages Summary

**11 developing/advanced/ RST pages converted to clean Markdown and 32 API reference pages with mkdocstrings ::: directives — `mkdocs build --strict` passes in 2s with real kotti module introspection**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-02-28T09:29:00Z
- **Completed:** 2026-02-28T09:45:45Z
- **Tasks:** 2
- **Files modified:** 57

## Accomplishments

- 11 developing/advanced/*.rst pages batch-converted via pandoc then hand-cleaned (all {.interpreted-text} remnants removed)
- 32 API reference pages created with `::: kotti.module` directives for mkdocstrings
- API index page updated with descriptive module table linking all 18 modules
- blobs.md callgraph SVGs copied from docs/_static/ to docs/images/ and rewritten as HTML grid
- mkdocstrings `members_order: source` configured in global mkdocs.yml handler options
- `mkdocs build --strict` passes 0 warnings in 2.08s (up from 0.21s — real module introspection is working)

## Task Commits

Each task was committed atomically:

1. **Task 1: Convert developing/advanced/ pages via pandoc + cleanup** - `745c69fb` (feat)
2. **Task 2: Create mkdocstrings API reference pages** - `d37497d2` (feat)

**Plan metadata:** (docs commit pending)

## Files Created/Modified

- `docs/guides/user-guide/as-a-library.md` - Pandoc + manual cleanup of as-a-library.rst
- `docs/guides/user-guide/blobs.md` - Pandoc + manual cleanup; callgraph images as HTML grid
- `docs/guides/user-guide/events.md` - Pandoc + RST link cleanup; code blocks fixed to Python
- `docs/guides/user-guide/sanitizers.md` - Pandoc + links to kotti.sanitizers API page
- `docs/guides/user-guide/understanding-kotti-startup.md` - Pandoc + Pyramid API links
- (7 more user-guide/*.md files — all cleaned of {.interpreted-text} remnants)
- `docs/images/callgraph-served-by-kotti.svg` - Copied from docs/_static/ for MkDocs path
- `docs/images/callgraph-served-by-tween.svg` - Copied from docs/_static/ for MkDocs path
- `docs/api/kotti.resources.md` - `::: kotti.resources` with mkdocstrings options
- `docs/api/kotti.events.md` - `::: kotti.events` with mkdocstrings options
- (30 more API *.md files — all with ::: module directives)
- `mkdocs.yml` - Global `members_order: source` added to python handler options
- `src/kotti/filedepot.py` - Docstring fix (see deviations)
- `src/kotti/request.py` - Docstring fix (see deviations)
- `src/kotti/resources.py` - Docstring fix (see deviations)
- `src/kotti/sanitizers.py` - Docstring fix (see deviations)
- `src/kotti/message.py` - Docstring fix (see deviations)
- `src/kotti/security.py` - Docstring fix (see deviations)

## Decisions Made

- blobs.md callgraph images: used `<div class="grid" markdown>` HTML grid layout (md_in_html extension enabled)
- Broken links: `../configuration.md` → `configuration.md` (files are in same directory)
- Python code in blobs.md: `StringIO` → `BytesIO` (Python 3.10+ update)
- mkdocstrings options: `members: true` + `members_order: source` + `filters: ["!^_"]` as standard
- getting-started/ and community/help.md uncommitted content from Plan 02 included in Task 1 commit

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed griffe 2.0 duplicate Sphinx param warnings breaking --strict build**
- **Found during:** Task 2 (Create mkdocstrings API reference pages)
- **Issue:** griffe 2.0 emits "Duplicate parameter information" warnings when Sphinx docstrings use both `:param name: desc` and `:type name: type` entries for the same parameter. `mkdocs build --strict` treats all warnings as failures. 32 warnings across 6 source files.
- **Fix:** Merged separate `:param x:` + `:type x:` entries into combined `:param type x: desc` syntax in 6 source files: `request.py`, `message.py`, `filedepot.py`, `resources.py`, `sanitizers.py`, `security.py`
- **Files modified:** `src/kotti/request.py`, `src/kotti/message.py`, `src/kotti/filedepot.py`, `src/kotti/resources.py`, `src/kotti/sanitizers.py`, `src/kotti/security.py`
- **Verification:** `mkdocs build --strict` passes with 0 warnings
- **Committed in:** `d37497d2` (Task 2 commit)

**2. [Rule 3 - Blocking] Fixed mkdocstrings `member_order` → `members_order` option name**
- **Found during:** Task 2 (first mkdocs build attempt with API pages)
- **Issue:** Plan specified `member_order: source` but mkdocstrings-python 2.0.3's `PythonOptions` uses `members_order` (plural). Build errored: "PythonOptions.__init__() got an unexpected keyword argument 'member_order'"
- **Fix:** sed batch-replaced `member_order` with `members_order` across all 32 API files
- **Files modified:** All 32 docs/api/**/*.md files
- **Verification:** Build error resolved
- **Committed in:** `d37497d2` (Task 2 commit)

**3. [Rule 3 - Blocking] Fixed broken links in converted user-guide pages**
- **Found during:** Task 1 (mkdocs build --strict check after conversion)
- **Issue:** `../configuration.md` links in close-to-anonymous.md and frontpage-different-template.md resolved to `guides/configuration.md` which doesn't exist; correct path is `configuration.md` (same directory)
- **Fix:** Updated relative links to `configuration.md` (same directory relative)
- **Files modified:** `close-to-anonymous.md`, `frontpage-different-template.md`
- **Committed in:** `745c69fb` (Task 1 commit)

---

**Total deviations:** 3 auto-fixed (1 source docstring quality bug, 1 wrong option name, 1 broken link)
**Impact on plan:** All auto-fixes necessary for mkdocs build --strict to pass. Source docstring fixes are correct improvements to kotti codebase.

## Issues Encountered

- mkdocstrings-python 2.0.3 has a bug: `SphinxStyleOptions` defines `warn_missing_types` but griffe's `parse_sphinx()` doesn't accept it. Setting `docstring_options` in mkdocs.yml triggers this bug. Workaround: fix source docstrings to not emit warnings, rather than suppressing warnings in config.
- griffe 2.0 treats Sphinx `:param x:` + `:type x:` pattern as "Duplicate parameter information" — this is a known breaking change from griffe 1.x behavior. Fixed in source.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `mkdocs build --strict` is green with real mkdocstrings module introspection (2.08s build)
- All 11 advanced guide pages are real content (not stubs)
- All 32 API pages have ::: directives and render actual kotti API docs
- Plan 04 (community pages, changelog) can proceed immediately
- Pre-existing griffe docstring quality issues in kotti source are now fixed

---
*Phase: 05-documentation-migration*
*Completed: 2026-02-28*
