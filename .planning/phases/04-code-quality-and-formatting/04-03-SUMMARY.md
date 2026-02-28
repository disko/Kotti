---
phase: 04-code-quality-and-formatting
plan: "03"
subsystem: infra
tags: [pre-commit, ruff, ci, github-actions, code-quality]

# Dependency graph
requires:
  - phase: 04-02
    provides: zero ruff violations, clean codebase ready for hook enforcement
provides:
  - pre-commit hooks that enforce ruff lint, ruff format, and hygiene on every commit
  - CI lint job that verifies format compliance and runs pre-commit hooks
affects: [all future phases — commits must pass pre-commit hooks]

# Tech tracking
tech-stack:
  added: [pre-commit 4.5.1, ruff-pre-commit v0.15.4, pre-commit-hooks v6.0.0]
  patterns: [pre-commit enforces ruff-check + ruff-format before every commit, CI duplicates hook checks as bypass prevention]

key-files:
  created: [.pre-commit-config.yaml]
  modified: [.github/workflows/ci.yml, src/kotti/locale/Kotti.pot, src/kotti/static/base.min.css, src/kotti/static/contents.min.js, src/kotti/static/upload.min.css, docs/api/index.rst, .planning/config.json, pip-selfcheck.json]

key-decisions:
  - "kotti-brand/ excluded from check-yaml hook — external asset directory with Python YAML constructors (!!python/name:) that check-yaml cannot parse"
  - "Pre-commit auto-fixed trailing whitespace in Kotti.pot and missing end-of-file newlines in static assets"

patterns-established:
  - "Pre-commit hook order: ruff-check (--fix) → ruff-format → hygiene hooks ensures lint fixes are formatted before commit"
  - "CI pre-commit step uses uv tool install pre-commit to match local developer workflow"

requirements-completed: [LNT-06]

# Metrics
duration: 2min
completed: "2026-02-28"
---

# Phase 4 Plan 03: Pre-commit Hooks and CI Format Enforcement Summary

**Pre-commit hooks with ruff v0.15.4 and hygiene checks enforced on every commit; CI lint job extended with ruff format --check and pre-commit run --all-files**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-02-28T00:49:10Z
- **Completed:** 2026-02-28T00:50:24Z
- **Tasks:** 2
- **Files modified:** 9

## Accomplishments

- Created `.pre-commit-config.yaml` with ruff-pre-commit v0.15.4 (ruff-check --fix + ruff-format) and pre-commit-hooks v6.0.0 (7 hygiene hooks)
- Updated CI lint job to include `ruff format --check .` and `pre-commit run --all-files` steps
- `pre-commit run --all-files` passes with zero failures
- Auto-fixed trailing whitespace and missing end-of-file newlines in 6 tracked files

## Task Commits

Each task was committed atomically:

1. **Task 1: Create pre-commit configuration** - `9db30c02` (chore)
2. **Task 2: Update CI lint job with format check and pre-commit** - `8bb55c0b` (ci)

## Files Created/Modified

- `.pre-commit-config.yaml` - Pre-commit hook configuration with ruff and hygiene hooks
- `.github/workflows/ci.yml` - Added ruff format check and pre-commit steps to lint job
- `src/kotti/locale/Kotti.pot` - Auto-fixed trailing whitespace
- `src/kotti/static/base.min.css` - Auto-fixed missing end-of-file newline
- `src/kotti/static/contents.min.js` - Auto-fixed missing end-of-file newline
- `src/kotti/static/upload.min.css` - Auto-fixed missing end-of-file newline
- `docs/api/index.rst` - Auto-fixed missing end-of-file newline
- `.planning/config.json` - Auto-fixed missing end-of-file newline
- `pip-selfcheck.json` - Auto-fixed missing end-of-file newline

## Decisions Made

- Excluded `kotti-brand/` from the `check-yaml` hook. That directory is untracked and contains `mkdocs.yml` with `!!python/name:material.extensions.emoji.twemoji` Python YAML constructors that the standard YAML parser rejects. Since it's external brand assets (not source code), exclusion is correct.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added kotti-brand/ exclusion to check-yaml hook**
- **Found during:** Task 1 (Create pre-commit configuration)
- **Issue:** `pre-commit run --all-files` failed on `kotti-brand/mkdocs-theme/mkdocs.yml` — file uses `!!python/name:` YAML constructors for MkDocs Material theme emoji config, which are not valid standard YAML
- **Fix:** Added `exclude: ^kotti-brand/` to the `check-yaml` hook in `.pre-commit-config.yaml`
- **Files modified:** `.pre-commit-config.yaml`
- **Verification:** `pre-commit run --all-files` exits 0 after exclusion
- **Committed in:** `9db30c02` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug/blocking)
**Impact on plan:** Exclusion is correct — kotti-brand/ is untracked external content, not project source. No scope creep.

## Issues Encountered

Pre-commit auto-fixed trailing whitespace and missing newlines in 6 tracked files. These were staged and included in the Task 1 commit as specified in the plan instructions.

## User Setup Required

None - no external service configuration required.

Developers who want to use pre-commit locally should run:
```bash
uv tool install pre-commit
pre-commit install
```

## Next Phase Readiness

- Phase 4 is now complete: ruff config, zero violations, pre-commit enforcement, CI verification
- Phase 5 (Documentation) can proceed — no blockers from Phase 4
- Pre-commit hooks are installed in CI and will block future violations automatically

---
*Phase: 04-code-quality-and-formatting*
*Completed: 2026-02-28*
