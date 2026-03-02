# Phase 5: Documentation Migration - Context

**Gathered:** 2026-02-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Migrate existing Sphinx/RST documentation to MkDocs with Material for MkDocs theme. All existing content is preserved, API docs are generated from docstrings, and the Kotti brand kit is applied. Sphinx artifacts are removed after verified migration.

</domain>

<decisions>
## Implementation Decisions

### Site structure & navigation
- Restructure nav to match brand template: 4 top-level tabs — Overview | Guides | API | Community
- `navigation.tabs` enabled in header for top-level sections
- 1:1 page conversion — every existing RST page becomes its own MD page (no merging)
- Include changelog in the docs site; exclude todo.txt (internal only)
- Map existing sections: first_steps/ → Getting Started (under Guides), developing/basic/ + developing/advanced/ → User Guide (under Guides), api/ → API tab

### Content conversion approach
- Automated conversion (pandoc/rst-to-myst) as starting point, then manual cleanup
- Standard markdown relative links for cross-references (no mkdocs-autorefs plugin)
- Code blocks get language-specific syntax highlighting + copy buttons (already enabled in brand config)
- Replace any Graphviz diagrams with Mermaid (native Material for MkDocs support via pymdownx.superfences)
- Delete old RST docs after verified migration — clean break

### API docs generation
- Per-module pages matching existing structure (one page per module)
- Source code links to GitHub enabled for each documented class/function
- API Reference tab includes an index/overview page listing all modules with one-line descriptions
- mkdocstrings for Python docstring extraction

### Content quality
- Fix obvious issues during conversion: broken links, typos, outdated references
- Update Python version references to reflect 3.10+ target; remove Python 2 references
- Verify code examples against current codebase during conversion

### Theme & branding
- Apply kotti-brand kit as-is: mkdocs.yml config, kotti.css, SVG assets, logo.html override
- Default color mode follows system preference (not hardcoded light or dark)
- Enable social cards plugin for branded Open Graph images on link sharing
- Set up mike for multi-version documentation

### Build & deployment
- Host on ReadTheDocs (keep existing kotti.readthedocs.io)
- Add MkDocs dependencies as optional `[docs]` group in pyproject.toml
- Create .readthedocs.yml configured for MkDocs build

### Sphinx cleanup
- Delete all Sphinx artifacts after migration: conf.py, Makefile, docs/_static/, Sphinx dependencies
- Remove Sphinx-related dependencies from pyproject.toml

### Claude's Discretion
- API docs detail level: include what has meaningful docstrings, skip undocumented internals
- Static assets from docs/_static/: review and migrate anything actually referenced in content, discard the rest

</decisions>

<specifics>
## Specific Ideas

- Use the full kotti-brand kit (BRAND.md, mkdocs-theme/, svg/) — it's purpose-built for this migration
- Brand palette: Amber Heritage (#D4920B primary, #F7F3ED light bg, #1A1714 dark bg)
- Typography: JetBrains Mono throughout (text + code)
- Mermaid replaces Graphviz for any existing diagrams

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 05-documentation-migration*
*Context gathered: 2026-02-28*
