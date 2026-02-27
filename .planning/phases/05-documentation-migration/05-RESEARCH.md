# Phase 5: Documentation Migration - Research

**Researched:** 2026-02-28
**Domain:** MkDocs + Material for MkDocs, mkdocstrings, RST-to-Markdown conversion, ReadTheDocs deployment
**Confidence:** HIGH (stack verified against Context7 and live official docs)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Site structure & navigation**
- Restructure nav to match brand template: 4 top-level tabs — Overview | Guides | API | Community
- `navigation.tabs` enabled in header for top-level sections
- 1:1 page conversion — every existing RST page becomes its own MD page (no merging)
- Include changelog in the docs site; exclude todo.txt (internal only)
- Map existing sections: first_steps/ → Getting Started (under Guides), developing/basic/ + developing/advanced/ → User Guide (under Guides), api/ → API tab

**Content conversion approach**
- Automated conversion (pandoc/rst-to-myst) as starting point, then manual cleanup
- Standard markdown relative links for cross-references (no mkdocs-autorefs plugin)
- Code blocks get language-specific syntax highlighting + copy buttons (already enabled in brand config)
- Replace any Graphviz diagrams with Mermaid (native Material for MkDocs support via pymdownx.superfences)
- Delete old RST docs after verified migration — clean break

**API docs generation**
- Per-module pages matching existing structure (one page per module)
- Source code links to GitHub enabled for each documented class/function
- API Reference tab includes an index/overview page listing all modules with one-line descriptions
- mkdocstrings for Python docstring extraction

**Content quality**
- Fix obvious issues during conversion: broken links, typos, outdated references
- Update Python version references to reflect 3.10+ target; remove Python 2 references
- Verify code examples against current codebase during conversion

**Theme & branding**
- Apply kotti-brand kit as-is: mkdocs.yml config, kotti.css, SVG assets, logo.html override
- Default color mode follows system preference (not hardcoded light or dark)
- Enable social cards plugin for branded Open Graph images on link sharing
- Set up mike for multi-version documentation

**Build & deployment**
- Host on ReadTheDocs (keep existing kotti.readthedocs.io)
- Add MkDocs dependencies as optional `[docs]` group in pyproject.toml
- Create .readthedocs.yml configured for MkDocs build

**Sphinx cleanup**
- Delete all Sphinx artifacts after migration: conf.py, Makefile, docs/_static/, Sphinx dependencies
- Remove Sphinx-related dependencies from pyproject.toml

### Claude's Discretion
- API docs detail level: include what has meaningful docstrings, skip undocumented internals
- Static assets from docs/_static/: review and migrate anything actually referenced in content, discard the rest

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOC-01 | Documentation migrated from Sphinx/RST to MkDocs with Material for MkDocs theme | Brand kit is fully built; mkdocs.yml template exists at kotti-brand/mkdocs-theme/mkdocs.yml. 61 RST files to convert; pandoc is the conversion tool of choice. |
| DOC-02 | Documentation builds successfully with MkDocs | `mkdocs build` is the verification gate; brand config is complete and tested patterns exist. Dependencies go in `[docs]` group in pyproject.toml. |
| DOC-03 | All existing documentation content preserved during migration | 61 RST source files across api/ (32), developing/ (19), first_steps/ (6), and root-level pages. 1:1 conversion strategy, no merging. |
| DOC-04 | API documentation generated (mkdocstrings or equivalent) | mkdocstrings[python] with Sphinx-style docstring parsing. 20% docstring coverage in codebase — generate API pages for all modules that have any meaningful docstrings, skip undocumented internals. |
</phase_requirements>

---

## Summary

This phase converts 61 RST files from Sphinx to MkDocs with Material for MkDocs theme. The heavy lifting is already done: the `kotti-brand/` directory contains a complete, ready-to-use mkdocs.yml, kotti.css, logo.html override, and all SVG assets. The migration has three distinct work streams: (1) scaffolding — copy brand kit, set up directory structure, update pyproject.toml docs group, create .readthedocs.yaml; (2) content conversion — pandoc to automate RST→MD for 29 narrative pages, manual work for RST-specific constructs (cross-references, image tables, `.. raw::` blocks, intersphinx references), then rewrite contributing.rst for MkDocs workflow; (3) API docs — create mkdocstrings pages for 16 top-level modules + kotti.views subtree, configure mkdocstrings plugin with Sphinx docstring style.

The RST conversion will require significant manual cleanup because Sphinx-specific constructs do not translate automatically. The main conversion challenges are: (a) 75 RST cross-reference roles (`:ref:`, `:mod:`, `:func:`, `:class:` etc.) must become plain markdown links; (b) one file (`changes.rst`) is a pure `.. include::` directive that must become a symlink or direct copy of CHANGES.txt; (c) `developer-manual.rst` embeds a `.. raw:: html` iframe and an `.. include::` for a code file; (d) `blobs.rst` uses an RST figure table for two side-by-side SVG images.

The callgraph SVGs (`callgraph-served-by-kotti.svg`, `callgraph-served-by-tween.svg`) are the only `_static/` assets actually referenced in content — they should be migrated. The other `_static/` files (README, .graffle file) can be discarded. The existing SVGs are already rendered Graphviz output so they migrate as-is without needing Mermaid conversion — only inline graphviz code blocks would need Mermaid. No RST files contain inline `.. graphviz::` directives; the two SVGs are pre-rendered references. The user decision to "replace Graphviz with Mermaid" applies only if inline graphviz code blocks exist — they don't in this codebase.

**Primary recommendation:** Work in waves: Wave 0 (scaffolding + build verification), Wave 1 (narrative content conversion), Wave 2 (API docs + mkdocstrings), Wave 3 (cleanup, social cards, mike, RTD config, Sphinx removal).

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| mkdocs-material | >=9.5 | Theme + build system | The brand kit is built for Material; all CONTEXT.md features (tabs, dark mode, social cards) are Material-native |
| mkdocstrings[python] | >=0.24 | Python API doc generation from docstrings | Official plugin for mkdocstrings Python handler; griffe-based (replaces legacy python-legacy handler) |
| mike | >=2.0 | Multi-version documentation | Required for `extra.version.provider: mike` in mkdocs.yml |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| mkdocs-material[imaging] | >=9.5 | Social card image generation | Required for social plugin with cairosvg dependency; the `[imaging]` extra installs cairosvg + pillow |
| pandoc | 3.x (system) | RST→MD automated first pass | Already installed at system level (3.8.3 confirmed). Use for batch conversion of narrative docs. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pandoc | rst-to-myst | rst-to-myst not installed, pandoc already available and produces clean Markdown |
| mkdocstrings[python] | sphinx-autodoc | sphinx-autodoc requires Sphinx; mkdocstrings is the MkDocs-native equivalent |
| mike | GitLab CI versioning | mike is the standard for Material for MkDocs; already referenced in brand kit |

**Installation (docs group in pyproject.toml):**
```toml
[project.optional-dependencies]
docs = [
    "mkdocs-material[imaging]>=9.5",
    "mkdocstrings[python]>=0.24",
    "mike>=2.0",
]
```

---

## Architecture Patterns

### Recommended Project Structure
```
/                               # project root
├── mkdocs.yml                  # copied from kotti-brand/mkdocs-theme/mkdocs.yml (with nav filled in)
├── .readthedocs.yaml           # ReadTheDocs v2 config
└── docs/
    ├── overrides/              # copied from kotti-brand/mkdocs-theme/overrides/
    │   └── partials/
    │       └── logo.html
    ├── stylesheets/            # from kotti-brand/mkdocs-theme/stylesheets/
    │   └── kotti.css
    ├── assets/                 # SVG files from kotti-brand/svg/
    │   ├── kotti-mark-dark.svg
    │   ├── kotti-mark-light.svg
    │   └── kotti-favicon.svg   # etc.
    ├── index.md                # Overview tab — site home
    ├── guides/                 # Guides tab
    │   ├── getting-started/    # first_steps/ → here
    │   │   ├── overview.md
    │   │   ├── installation.md
    │   │   ├── tutorial.md
    │   │   ├── tut-1.md
    │   │   ├── tut-2.md
    │   │   └── tut-3.md
    │   └── user-guide/         # developing/ → here
    │       ├── developer-manual.md
    │       ├── security.md
    │       ├── configuration.md
    │       ├── testing.md
    │       ├── translations.md
    │       ├── deployment.md
    │       ├── as-a-library.md
    │       ├── close-to-anonymous.md
    │       ├── default-views.md
    │       ├── add-to-edit-interface.md
    │       ├── events.md
    │       ├── frontpage-different-template.md
    │       ├── images.md
    │       ├── blobs.md         # has callgraph SVGs
    │       ├── static-resource-management.md
    │       ├── understanding-kotti-startup.md
    │       └── sanitizers.md
    ├── api/                    # API tab
    │   ├── index.md            # module listing with one-line descriptions
    │   ├── kotti.md
    │   ├── kotti.events.md
    │   ├── kotti.fanstatic.md
    │   ├── kotti.filedepot.md
    │   ├── kotti.interfaces.md
    │   ├── kotti.message.md
    │   ├── kotti.migrate.md
    │   ├── kotti.populate.md
    │   ├── kotti.request.md
    │   ├── kotti.resources.md
    │   ├── kotti.sanitizers.md
    │   ├── kotti.security.md
    │   ├── kotti.sqla.md
    │   ├── kotti.testing.md
    │   ├── kotti.traversal.md
    │   ├── kotti.util.md
    │   ├── kotti.workflow.md
    │   └── kotti.views/
    │       ├── index.md
    │       ├── kotti.views.cache.md
    │       ├── kotti.views.file.md
    │       ├── kotti.views.form.md
    │       ├── kotti.views.login.md
    │       ├── kotti.views.site_setup.md
    │       ├── kotti.views.slots.md
    │       ├── kotti.views.users.md
    │       ├── kotti.views.util.md
    │       ├── kotti.views.view.md
    │       └── kotti.views.edit/
    │           ├── index.md
    │           ├── kotti.views.edit.actions.md
    │           ├── kotti.views.edit.content.md
    │           └── kotti.views.edit.default_views.md
    ├── community/              # Community tab
    │   ├── help.md
    │   ├── contributing.md
    │   └── changelog.md        # CHANGES.txt content
    └── images/                 # Migrated static assets (referenced images only)
        ├── callgraph-served-by-kotti.svg
        └── callgraph-served-by-tween.svg
```

### Pattern 1: Brand Kit Application
**What:** Copy kotti-brand/ files into docs/ structure
**When to use:** First task of the phase — must be done before any build verification
**Example:**
```bash
# From project root
cp kotti-brand/mkdocs-theme/mkdocs.yml mkdocs.yml
mkdir -p docs/overrides/partials docs/stylesheets docs/assets
cp kotti-brand/mkdocs-theme/overrides/partials/logo.html docs/overrides/partials/
cp kotti-brand/mkdocs-theme/stylesheets/kotti.css docs/stylesheets/
cp kotti-brand/svg/*.svg docs/assets/
```

### Pattern 2: mkdocstrings API Page
**What:** Each mkdocstrings API page uses the `:::` injection syntax
**When to use:** One `.md` file per module in docs/api/
**Example (Source: Context7 /mkdocstrings/mkdocstrings):**
```markdown
# kotti.events

::: kotti.events
    options:
      docstring_style: sphinx
      show_source: true
      members: true
      member_order: source
      filters:
        - "!^_"
```

### Pattern 3: mkdocstrings Plugin Configuration
**What:** Plugin config in mkdocs.yml enabling Python docstring parsing
**When to use:** Must be added to the brand kit's mkdocs.yml during scaffolding
**Example (Source: Context7 /mkdocstrings/mkdocstrings):**
```yaml
plugins:
  - search
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          options:
            docstring_style: sphinx
            show_source: true
            show_root_heading: true
            show_root_full_path: true
            show_bases: true
            show_submodules: false
            members_order: source
```

### Pattern 4: pandoc Batch Conversion
**What:** Use pandoc to convert RST files to Markdown as first pass
**When to use:** Narrative docs (non-API). Requires manual cleanup of RST roles after.
**Example:**
```bash
# Convert a single file
pandoc -f rst -t markdown input.rst -o output.md

# The output will contain patterns like:
#   `label`{.interpreted-text role="ref"}   ← must become [label](relative-link.md)
#   `kotti.events`{.interpreted-text role="mod"}  ← must become [`kotti.events`](../api/kotti.events.md)
```

### Pattern 5: ReadTheDocs v2 Configuration
**What:** `.readthedocs.yaml` for MkDocs builds
**When to use:** Required for ReadTheDocs to auto-build on push
**Example (Source: Official RTD docs):**
```yaml
version: 2

build:
  os: "ubuntu-22.04"
  tools:
    python: "3.12"

mkdocs:
  configuration: mkdocs.yml

python:
  install:
    - requirements: docs/requirements.txt
```

Or using pip extras:
```yaml
python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```

### Pattern 6: mike Versioning Setup
**What:** Version selector in mkdocs.yml (already commented out in brand kit)
**When to use:** Uncomment the mike provider block; mike itself is deployed via CI not during build
**Example (Source: Context7 /websites/squidfunk_github_io_mkdocs-material):**
```yaml
extra:
  version:
    provider: mike
    alias: true
    default: stable
```

### Pattern 7: Social Cards Plugin
**What:** Auto-generates Open Graph images; requires cairosvg via [imaging] extra
**When to use:** Enable in mkdocs.yml (already commented out in brand kit)
**Example (Source: Context7 /websites/squidfunk_github_io_mkdocs-material):**
```yaml
plugins:
  - search
  - social:
      enabled: !ENV [CI, false]  # disable locally for faster builds
  - mkdocstrings:
      ...
```

### Anti-Patterns to Avoid
- **Auto-converting RST roles without review:** pandoc converts `:ref:`, `:mod:`, `:func:` to `{.interpreted-text role="ref"}` — these are NOT valid Markdown and will cause build failures. Every RST role must be manually replaced.
- **Using `mkdocs-autorefs` plugin:** CONTEXT.md explicitly excludes this. Use plain relative markdown links.
- **Using `navigation.indexes` without index pages:** The nav structure uses `index.md` files as section landing pages; they must exist before the nav references them.
- **Social cards in local builds without cairosvg:** The social plugin requires cairosvg system dependencies. Use `!ENV [CI, false]` to disable locally.
- **Leaving `repoze.sphinx.autointerface` in docs dependencies:** It's a Sphinx plugin; it's useless and will cause import errors with MkDocs.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| RST → MD conversion | Custom sed/awk scripts | pandoc | pandoc handles RST structure, tables, code blocks, admonitions, footnotes correctly |
| Python docstring API pages | Manual markdown | mkdocstrings[python] | Handles griffe introspection, source links, inheritance, signatures |
| Multi-version docs | Custom redirect logic | mike | Integrates with Material version selector; manages gh-pages branches |
| Social card images | Custom OG image templates | Material social plugin | Native Material feature, uses cairosvg, respects brand colors |
| Site search | Custom search index | MkDocs built-in search plugin | Already included; zero configuration needed |

**Key insight:** The kotti-brand kit was purpose-built for this migration. Treat it as the canonical mkdocs.yml — don't start from scratch. Copy it, then add the nav structure and mkdocstrings plugin.

---

## Common Pitfalls

### Pitfall 1: RST Cross-Reference Roles After pandoc
**What goes wrong:** pandoc outputs `` `label`{.interpreted-text role="ref"} `` for every `:ref:`, `:mod:`, `:func:` etc. These are not valid Markdown — MkDocs build succeeds but renders literal text instead of links.
**Why it happens:** pandoc faithfully represents the RST role semantics in a Markdown extension syntax that no standard Markdown processor understands.
**How to avoid:** After pandoc conversion, grep for `{.interpreted-text` and replace each occurrence with a proper relative Markdown link.
**Warning signs:** `grep -r "interpreted-text" docs/` returns any results after conversion.

### Pitfall 2: `.. include::` Directives
**What goes wrong:** Two RST files use `.. include::`: `changes.rst` includes `../CHANGES.txt`, and `developer-manual.rst` includes `../../../kotti/tests/nodes.txt`. pandoc fails to resolve these at conversion time.
**Why it happens:** pandoc does not resolve RST include directives relative to the project root.
**How to avoid:**
  - `changes.rst` → create `docs/community/changelog.md` with a direct copy (or symlink) of CHANGES.txt content, converted to Markdown headers.
  - `developer-manual.rst` include of nodes.txt → the file is a test fixture. Review what it contains and either inline the relevant snippet or remove it from the narrative docs.
**Warning signs:** pandoc emits `[WARNING] Could not load include file` during conversion.

### Pitfall 3: Sphinx `.. automodule::` in Narrative Docs
**What goes wrong:** `docs/developing/basic/testing.rst` contains an `.. automodule:: kotti.tests :members:` directive inside a narrative doc page. pandoc does not convert this.
**Why it happens:** It's a Sphinx directive, not RST.
**How to avoid:** Replace with a mkdocstrings `:::` block or with a link to the API reference page for kotti.tests.

### Pitfall 4: RST Figure Table for Side-by-Side Images
**What goes wrong:** `blobs.rst` uses an RST substitution + table trick to display two SVGs side by side with captions. pandoc converts this to a markdown table with embedded image syntax — which MkDocs renders but may look broken.
**Why it happens:** RST has `.. figure::` and image substitutions; Markdown has no equivalent table-with-images standard.
**How to avoid:** After pandoc, manually rewrite the blobs image section using HTML `<div>` grid or standard image with explicit sizing.

### Pitfall 5: `.. raw:: html` Block
**What goes wrong:** `developer-manual.rst` has a `.. raw:: html` block with a YouTube iframe. pandoc converts this to raw HTML inline in Markdown. MkDocs with Material processes raw HTML in Markdown — this usually works, but must be verified.
**Why it happens:** RST raw directives pass HTML through; pandoc preserves this.
**How to avoid:** After conversion, verify the YouTube embed renders correctly in `mkdocs serve`. The `md_in_html` extension in the brand kit's markdown_extensions should support this.

### Pitfall 6: mkdocstrings Needs kotti Installed in Build Env
**What goes wrong:** mkdocstrings imports the actual Python modules at build time to introspect docstrings. If kotti's dependencies aren't installed, the build fails with ImportError.
**Why it happens:** Unlike Sphinx's autodoc which can mock imports, mkdocstrings-python (griffe) imports the real module.
**How to avoid:** The .readthedocs.yaml must install kotti itself (not just docs deps) before building. Use `pip install -e .[docs]` or equivalent that pulls in the full kotti package.

### Pitfall 7: Sphinx Dependencies Still in [docs] Group
**What goes wrong:** pyproject.toml currently has `[project.optional-dependencies].docs` containing Sphinx, docutils, repoze.sphinx.autointerface, sphinx_rtd_theme. These conflict with MkDocs and waste install time.
**Why it happens:** The old docs group predates the migration decision.
**How to avoid:** Replace the entire docs group in the same commit that adds MkDocs deps.

### Pitfall 8: Social Plugin Fails Without cairosvg System Libs
**What goes wrong:** `mkdocs-material[imaging]` installs cairosvg, which needs libcairo system library. ReadTheDocs ubuntu-22.04 has it; local macOS may not.
**Why it happens:** cairosvg is a C extension wrapper.
**How to avoid:** Use `enabled: !ENV [CI, false]` for the social plugin so it only runs on RTD/CI, not locally.

### Pitfall 9: Intersphinx Links in Content
**What goes wrong:** Some narrative docs contain intersphinx-style references to external libraries (bleach, pyramid, sqlalchemy docs). pandoc converts these to `{.interpreted-text}` patterns. They can't resolve in MkDocs — just convert to regular hyperlinks to the external doc URLs.
**Why it happens:** Sphinx intersphinx maps external project inventories; MkDocs has no equivalent.
**How to avoid:** During cleanup pass, convert intersphinx cross-references to direct hyperlinks.

---

## Code Examples

Verified patterns from official sources:

### mkdocstrings API page (standard pattern)
```markdown
# kotti.events

::: kotti.events
    options:
      docstring_style: sphinx
      show_source: true
      members: true
      member_order: source
      filters:
        - "!^_"
```

### mkdocstrings index/overview page pattern
```markdown
# API Reference

Kotti Python API documentation, generated from source docstrings.

| Module | Description |
|--------|-------------|
| [kotti](kotti.md) | Main package — `main()`, `base_configure()`, `conf_defaults` |
| [kotti.events](kotti.events.md) | Event system — `ObjectEvent`, `subscribe` decorator |
| [kotti.resources](kotti.resources.md) | Content model — `Node`, `Content`, `Document`, `File` |
| ... | ... |
```

### mkdocstrings plugin config (goes into mkdocs.yml)
```yaml
plugins:
  - search
  - social:
      enabled: !ENV [CI, false]
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          options:
            docstring_style: sphinx
            show_source: true
            show_root_heading: true
            show_root_full_path: true
            show_bases: true
            members_order: source
            filters:
              - "!^_"
```

### Navigation structure (goes into mkdocs.yml)
```yaml
nav:
  - Overview: index.md
  - Guides:
    - Getting Started:
      - Overview: guides/getting-started/overview.md
      - Installation: guides/getting-started/installation.md
      - Tutorial: guides/getting-started/tutorial.md
      - Tutorial Part 1: guides/getting-started/tut-1.md
      - Tutorial Part 2: guides/getting-started/tut-2.md
      - Tutorial Part 3: guides/getting-started/tut-3.md
    - User Guide:
      - Developer Manual: guides/user-guide/developer-manual.md
      - Security: guides/user-guide/security.md
      - Configuration: guides/user-guide/configuration.md
      - Testing: guides/user-guide/testing.md
      - Translations: guides/user-guide/translations.md
      - Deployment: guides/user-guide/deployment.md
      - Advanced:
        - As a Library: guides/user-guide/as-a-library.md
        - Close to Anonymous: guides/user-guide/close-to-anonymous.md
        - Default Views: guides/user-guide/default-views.md
        - Edit Interface: guides/user-guide/add-to-edit-interface.md
        - Events: guides/user-guide/events.md
        - Front Page Template: guides/user-guide/frontpage-different-template.md
        - Images: guides/user-guide/images.md
        - Blob Storage: guides/user-guide/blobs.md
        - Static Resources: guides/user-guide/static-resource-management.md
        - Startup Internals: guides/user-guide/understanding-kotti-startup.md
        - Sanitizers: guides/user-guide/sanitizers.md
  - API:
    - Reference: api/index.md
    - kotti: api/kotti.md
    # ... all modules
  - Community:
    - Help: community/help.md
    - Contributing: community/contributing.md
    - Changelog: community/changelog.md
```

### .readthedocs.yaml
```yaml
version: 2

build:
  os: "ubuntu-22.04"
  tools:
    python: "3.12"

mkdocs:
  configuration: mkdocs.yml

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```

### pyproject.toml docs group (replacement for current Sphinx group)
```toml
[project.optional-dependencies]
docs = [
    "mkdocs-material[imaging]>=9.5",
    "mkdocstrings[python]>=0.24",
    "mike>=2.0",
]
```

### RST role cleanup grep pattern (post-pandoc)
```bash
# Find all pandoc-output RST role remnants
grep -rn "interpreted-text" docs/

# Common patterns to replace manually:
# `label`{.interpreted-text role="ref"}  → [label](relative-path.md)
# `kotti.events`{.interpreted-text role="mod"} → [`kotti.events`](../api/kotti.events.md)
# `ClassName`{.interpreted-text role="class"} → [`ClassName`](../api/module.md#classname)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Sphinx + RST | MkDocs + Markdown | This phase | Simpler authoring, no Sphinx build chain, Material theme |
| sphinx.ext.autodoc | mkdocstrings[python] (griffe) | 2021+ | Griffe-based, faster, no Sphinx required |
| mkdocstrings legacy python handler | mkdocstrings[python] new handler | 0.19 | `selection` key merged into `options`; `restructured-text` style renamed to `sphinx` |
| `extra.version.method: mike` | `extra.version.provider: mike` | Material 7.x | The `method` key is deprecated; use `provider` |
| sphinx_rtd_theme on ReadTheDocs | MkDocs Material with `.readthedocs.yaml` v2 | RTD 2023 | RTD v2 config is required; RTD auto-detects MkDocs when `mkdocs.configuration` is set |

**Deprecated/outdated in pyproject.toml:**
- `Sphinx`, `docutils`, `repoze.sphinx.autointerface`, `sphinx_rtd_theme`: All removed from docs group
- `rtd.txt`: Entire file is obsolete (Sphinx-era RTD requirements file)

---

## Open Questions

1. **Kotti docstring style (RST vs Google vs NumPy)**
   - What we know: The existing Sphinx config had no explicit docstring style. Scanning source files shows most docstrings use plain text with some RST field syntax (`:param x:`, `:returns:`). The mkdocstrings option `docstring_style: sphinx` handles this format.
   - What's unclear: Some docstrings may be inconsistently formatted — the exact rendering quality depends on docstring hygiene in each module.
   - Recommendation: Use `docstring_style: sphinx` as the default. If a module renders poorly, note it and move on — the discretion decision says "include what has meaningful docstrings, skip undocumented internals."

2. **How many API modules have meaningful docstrings?**
   - What we know: The codebase has 20% overall docstring coverage (249 of 1235 functions/classes have docstrings). Top-level modules like `kotti.events`, `kotti.security`, `kotti.resources` have API pages in the Sphinx docs — they have some coverage.
   - What's unclear: Whether those specific modules have enough docstrings to make useful API pages, or just function stubs.
   - Recommendation: Generate pages for all 16 top-level modules + kotti.views subtree that had existing Sphinx pages. Omit `kotti.tests` from the published API (it's the test module) despite it having an existing Sphinx page — tests aren't public API.

3. **mike deployment on ReadTheDocs vs GitHub Pages**
   - What we know: The CONTEXT.md says "Host on ReadTheDocs." Mike normally deploys to a gh-pages branch. RTD and mike can conflict if mike manages the gh-pages deploy while RTD also builds from the same branch.
   - What's unclear: Whether the intent is to use mike's gh-pages deployment OR just the mike version selector UI widget without the full gh-pages multi-version deployment.
   - Recommendation: For Phase 5, implement the mike `extra.version.provider: mike` config for the UI selector widget, but defer the actual mike gh-pages deployment workflow to a future task. RTD will build from the `master` branch with the current version — this satisfies the phase requirement. Document the limitation in a note.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (for Python tests); `mkdocs build` (for docs validation) |
| Config file | `pyproject.toml` [tool.pytest.ini_options] |
| Quick run command | `mkdocs build --strict` |
| Full suite command | `mkdocs build --strict && mkdocs serve --no-livereload` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOC-01 | Material for MkDocs theme renders with Kotti brand | smoke | `mkdocs build --strict` | ❌ Wave 0: `mkdocs.yml` must exist |
| DOC-02 | `mkdocs build` completes with no errors | smoke | `mkdocs build --strict` | ❌ Wave 0: `mkdocs.yml` + all `.md` files |
| DOC-03 | All 29 narrative pages + changelog present in built site | smoke | `find site/ -name "*.html" \| wc -l` + manual spot check | ❌ Wave 0: docs/ directory must be populated |
| DOC-04 | API pages exist and contain module docstrings | smoke | `ls site/api/*.html` + `grep -l "class\|function" site/api/*.html` | ❌ Wave 0: `docs/api/` mkdocstrings pages must exist |

### Sampling Rate
- **Per task commit:** `mkdocs build --strict 2>&1 | tail -5`
- **Per wave merge:** `mkdocs build --strict` — full clean build, zero errors/warnings
- **Phase gate:** `mkdocs build --strict` green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `mkdocs.yml` — does not exist yet at project root (copy from kotti-brand/mkdocs-theme/mkdocs.yml)
- [ ] `docs/` — existing Sphinx docs directory; must be restructured before any build is possible
- [ ] `docs/overrides/partials/logo.html` — missing
- [ ] `docs/stylesheets/kotti.css` — missing
- [ ] `docs/assets/` — SVG files missing
- [ ] pyproject.toml `[docs]` group — contains Sphinx deps, not MkDocs deps
- [ ] `.readthedocs.yaml` — does not exist

*(All Wave 0 gaps are scaffold/infrastructure, not test files — the "test" is the build itself.)*

---

## Sources

### Primary (HIGH confidence)
- `/mkdocstrings/mkdocstrings` (Context7) — Python handler options, `:::` syntax, docstring_style values, plugin config in mkdocs.yml
- `/websites/squidfunk_github_io_mkdocs-material` (Context7) — mike versioning setup, social plugin config, navigation.tabs feature name
- `kotti-brand/mkdocs-theme/mkdocs.yml` (in-repo) — complete brand configuration; directly usable
- `kotti-brand/BRAND.md` (in-repo) — brand palette and setup instructions
- `docs/` RST files (in-repo) — actual content inventory; 61 files confirmed
- `docs/conf.py` (in-repo) — current Sphinx extensions (autodoc, graphviz, inheritance_diagram, intersphinx)
- `pandoc --version` (local system) — confirmed 3.8.3 available

### Secondary (MEDIUM confidence)
- ReadTheDocs official docs (WebFetch) — `.readthedocs.yaml` v2 format for MkDocs, `mkdocs.configuration` key, `ubuntu-22.04` OS target
- pandoc conversion test results — live tested on overview.rst and developer-manual.rst; confirmed RST role output pattern and include file warning behavior

### Tertiary (LOW confidence)
- 20% docstring coverage estimate — derived from AST analysis; includes all functions (public + private + test functions), so the actual public API coverage is higher than 20%

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — mkdocstrings and Material for MkDocs verified via Context7; brand kit already exists in-repo
- Architecture: HIGH — directory structure derived from locked CONTEXT.md decisions + existing RST inventory (61 files counted)
- Pitfalls: HIGH for pandoc conversion pitfalls (live tested); MEDIUM for RTD/mike interaction (derived from official docs)

**Research date:** 2026-02-28
**Valid until:** 2026-03-30 (MkDocs Material and mkdocstrings are stable; RTD config format stable)
