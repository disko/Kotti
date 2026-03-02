---
phase: 04-code-quality-and-formatting
plan: 01
subsystem: infra
tags: [ruff, formatting, git-blame, pyproject.toml, code-quality]

# Dependency graph
requires:
  - phase: 03-python-version-ci-modernization
    provides: ruff already installed as dev dep; partial ruff config (E4,E7,E9,F) to expand
provides:
  - Expanded ruff config (E,W,F,I,B,UP,SIM,RUF) in pyproject.toml
  - Isolated formatting commit (96b5b597) covering 51 files
  - .git-blame-ignore-revs with formatting commit SHA
  - .gitattributes with export-ignore for blame file
affects: [04-02, pre-commit setup, CI lint job, all subsequent code changes]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Isolated formatting commit pattern: config commit -> format commit -> blame-ignore commit"
    - ".git-blame-ignore-revs + .gitattributes for GitHub blame preservation"
    - "ruff line-length=88 (Black default) as project standard"

key-files:
  created:
    - .git-blame-ignore-revs
    - .gitattributes
  modified:
    - pyproject.toml

key-decisions:
  - "ruff ruleset E,W,F,I,B,UP,SIM,RUF — F821/B008/SIM300 globally ignored (ORM forward refs, i18n patterns, test assert style)"
  - "B018 per-file-ignored in src/kotti/tests/**/*.py (intentional property-access side effects)"
  - "Formatting commit isolated as 96b5b597 — recorded in .git-blame-ignore-revs for blame preservation"
  - "line-length=88 consistent with ruff/Black default"

patterns-established:
  - "Three-commit ordering: config -> format -> blame-ignore"
  - "Never mix formatting and lint fixes in the same commit"

requirements-completed: [LNT-01, LNT-02, LNT-03, LNT-04]

# Metrics
duration: 8min
completed: 2026-02-28
---

# Phase 4 Plan 01: Ruff Config Expansion + Isolated Formatting Commit Summary

**Expanded ruff config to full E,W,F,I,B,UP,SIM,RUF ruleset, applied isolated formatting commit (51 files) with .git-blame-ignore-revs for blame history preservation**

## Performance

- **Duration:** ~8 min
- **Started:** 2026-02-28T00:20:57Z
- **Completed:** 2026-02-28T00:28:30Z
- **Tasks:** 1
- **Files modified:** 53 (51 reformatted + pyproject.toml + 2 new infra files)

## Accomplishments

- Expanded pyproject.toml ruff config from minimal E4/E7/E9/F to full E,W,F,I,B,UP,SIM,RUF ruleset with researched ignore list
- Applied `ruff format` in isolated commit (51 files reformatted, matching research prediction)
- Created .git-blame-ignore-revs with formatting commit SHA for git blame preservation
- Created .gitattributes with export-ignore directive; configured local git blame.ignoreRevsFile
- Confirmed pytest-flake8 absent (LNT-03 satisfied)

## Task Commits

Three commits as required by plan (strict ordering enforced):

1. **Config** - `d9879ffb` chore: expand ruff config to full ruleset (E,W,F,I,B,UP,SIM,RUF)
2. **Format (isolated)** - `96b5b597` style: apply ruff format to entire codebase
3. **Blame infra** - `7294aa01` chore: add .git-blame-ignore-revs for formatting commit

## Files Created/Modified

- `pyproject.toml` - Expanded [tool.ruff], [tool.ruff.lint], [tool.ruff.lint.per-file-ignores], [tool.ruff.format] sections
- `.git-blame-ignore-revs` - Contains SHA 96b5b5974781ecd259835335473111de2101d858 (formatting commit)
- `.gitattributes` - `.git-blame-ignore-revs export-ignore` (GitHub web blame respects this)
- `docs/conf.py` + 50 `src/kotti/**/*.py` files - Reformatted (whitespace/quote normalization only)

## Decisions Made

- F821 globally ignored — string annotations in security.py/resources.py are SQLAlchemy forward refs; adding `from __future__ import annotations` risks breaking ORM introspection in SQLAlchemy 1.4
- B008 globally ignored — `_()` i18n patterns and `PrincipalFull()` schema defaults are intentional API patterns
- SIM300 globally ignored — Yoda condition preference in test files is subjective style, not a bug
- B018 per-file-ignored in tests — intentional property-access side effects in test_util_views.py
- E711/E721 enabled (included in full `E` selector) — deferred from Phase 3, now live for Plan 02 to fix

## Deviations from Plan

None — plan executed exactly as written. Three-commit ordering maintained: config -> format -> blame-ignore.

## Issues Encountered

Minor: `git add` for alembic file `814c4ec72f1_...` failed with mismatched filename in initial attempt (extra `8` prefix). Resolved by using `git diff --name-only | xargs git add` to stage all formatting-changed files precisely.

## User Setup Required

None — no external service configuration required. Developers who want local git blame to skip the formatting commit should run:
```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```
(already done for this repo via this plan)

## Next Phase Readiness

- `ruff format --check .` passes with zero violations — formatting baseline established
- 441 ruff lint violations visible under expanded ruleset — Plan 02 addresses these
- .git-blame-ignore-revs in place — `git blame` will skip the formatting commit automatically on GitHub
- No blockers for Plan 02

---
*Phase: 04-code-quality-and-formatting*
*Completed: 2026-02-28*

## Self-Check: PASSED

- FOUND: .git-blame-ignore-revs
- FOUND: .gitattributes
- FOUND: pyproject.toml
- FOUND: 04-01-SUMMARY.md
- FOUND: d9879ffb (config commit)
- FOUND: 96b5b597 (format commit)
- FOUND: 7294aa01 (blame commit)
