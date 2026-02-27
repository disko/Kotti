---
phase: 03-python-version-and-ci-modernization
verified: 2026-02-27T00:00:00Z
status: human_needed
score: 5/6 must-haves verified (1 requires human)
human_verification:
  - test: "Run the CI matrix on a pull request or push to master"
    expected: "All 12 test jobs (Python 3.10-3.13 x SQLite/PostgreSQL/MySQL) pass and the ruff lint job passes"
    why_human: "PYV-04 requires tests to actually pass on all four Python versions; Python 3.13 + Pyramid 1.x compatibility is unverified locally (noted as a risk in research). CI must actually execute to confirm."
---

# Phase 03: Python Version and CI Modernization Verification Report

**Phase Goal:** Configure ruff linting, create consolidated CI matrix workflow (Python 3.10-3.13 x SQLite/PostgreSQL/MySQL), set up Dependabot
**Verified:** 2026-02-27
**Status:** human_needed
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | ruff check passes cleanly on the codebase with the configured rule set | VERIFIED | `uv run ruff check .` → "All checks passed!" (verified live) |
| 2 | A single ci.yml replaces the three old workflow files | VERIFIED | `.github/workflows/` contains only `ci.yml`; `sqlite.yml`, `postgres.yml`, `mysql.yml` deleted (confirmed by directory listing) |
| 3 | CI test matrix covers Python 3.10, 3.11, 3.12, 3.13 x SQLite, PostgreSQL, MySQL | VERIFIED | ci.yml lines 16-17: `python-version: ["3.10", "3.11", "3.12", "3.13"]`, `db-backend: [sqlite, postgres, mysql]` |
| 4 | CI lint job runs ruff check as a separate parallel job | VERIFIED | ci.yml lines 82-98: distinct `lint` job with `uv run ruff check .` at line 98 |
| 5 | CI uses uv sync and uv run — no pip or tox invocations | VERIFIED | ci.yml uses `uv sync --locked --group test` (lines 56, 95) and `uv run pytest` (lines 68, 72, 76); `uv pip install` for psycopg2-binary/pymysql is `uv pip`, not bare `pip`; no `tox` or `setup-python` found |
| 6 | Dependabot monitors both pip and github-actions ecosystems weekly | VERIFIED | dependabot.yml contains two entries: `package-ecosystem: "pip"` and `package-ecosystem: "github-actions"`, both with `interval: "weekly"` |

**Score:** 6/6 truths verified by static analysis. 1 additional truth (PYV-04: all tests pass on Python 3.10-3.13) requires CI execution to confirm.

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `pyproject.toml` | ruff configuration and ruff in test dependencies | VERIFIED | `[tool.ruff]` at line 208; `target-version = "py310"` at line 209; `select = ["E4", "E7", "E9", "F"]` at line 212; `ruff>=0.11` in both `[project.optional-dependencies].test` (line 126) and `[dependency-groups].test` (line 153) |
| `.github/workflows/ci.yml` | Consolidated CI matrix workflow with test and lint jobs | VERIFIED | 99-line file with test matrix job (12 combinations) and separate lint job; uses `actions/checkout@v6` and `astral-sh/setup-uv@v7`; no `actions/setup-python` |
| `.github/dependabot.yml` | Automated dependency update configuration | VERIFIED | 22-line file; pip + github-actions ecosystems; weekly schedule; grouped minor+patch PRs; limit 5 open PRs |
| `uv.lock` | Updated with ruff v0.15.4 | VERIFIED | `grep "ruff"` in uv.lock returns 28 matches; version is `0.15.4` (≥0.11 requirement satisfied) |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `.github/workflows/ci.yml` | `pyproject.toml [tool.ruff]` | `uv run ruff check` reads config from pyproject.toml | VERIFIED | Line 98 of ci.yml: `run: uv run ruff check .`; pyproject.toml has `[tool.ruff]` section with rule configuration |
| `.github/workflows/ci.yml` | `uv.lock` | `uv sync --locked` uses committed lockfile | VERIFIED | Lines 56 and 95 of ci.yml: `run: uv sync --locked --group test` |

---

### Requirements Coverage

| Requirement | Source Plan | Description (from REQUIREMENTS.md) | Status | Evidence |
|-------------|------------|-------------------------------------|--------|----------|
| PYV-01 | 03-01-PLAN.md | Python 3.6-3.9 classifiers and support dropped | SATISFIED | `requires-python = ">=3.10"` (line 10); no `3.6`/`3.7`/`3.8`/`3.9` classifier in pyproject.toml; confirmed by grep returning no matches |
| PYV-02 | 03-01-PLAN.md | Python 3.10-3.13 classifiers declared | SATISFIED | pyproject.toml lines 36-39 include all four version classifiers |
| PYV-03 | 03-01-PLAN.md | CI test matrix covers Python 3.10, 3.11, 3.12, 3.13 | SATISFIED | ci.yml line 16 matrix definition confirmed |
| PYV-04 | 03-01-PLAN.md | All tests pass on Python 3.10-3.13 | NEEDS HUMAN | Tests pass on Python 3.12 locally (verified in research); Python 3.13 + Pyramid 1.x compatibility unconfirmed per research notes; requires CI execution to verify |
| CI-01 | 03-01-PLAN.md | GitHub Actions updated to current versions (checkout@v4, setup-python@v5) | SATISFIED (spirit) | ci.yml uses `actions/checkout@v6` and `astral-sh/setup-uv@v7` — newer than the v4/v5 versions named in the requirement; no `actions/setup-python` used at all (replaced by uv) |
| CI-02 | 03-01-PLAN.md | CI uses uv for package installation (astral-sh/setup-uv action) | SATISFIED | `astral-sh/setup-uv@v7` used; `uv sync --locked --group test` for installation |
| CI-03 | 03-01-PLAN.md | Separate ruff lint/format check job in CI | SATISFIED (lint only) | Separate `lint` job exists running `uv run ruff check .`; no ruff format job yet (format is Phase 4, LNT-02) |
| CI-04 | 03-01-PLAN.md | 3 separate workflow files consolidated into 1 matrix workflow (Python version x DB backend) | SATISFIED | Only `ci.yml` remains in `.github/workflows/`; old `sqlite.yml`, `postgres.yml`, `mysql.yml` deleted |
| CI-05 | 03-01-PLAN.md | Dependabot configured for automated dependency PRs | SATISFIED | `dependabot.yml` exists with pip + github-actions monitoring |

#### Orphaned Requirements (mapped to Phase 3 in REQUIREMENTS.md but not claimed by any plan)

| Requirement | REQUIREMENTS.md Status | Description | Finding |
|-------------|----------------------|-------------|---------|
| LNT-03 | Pending (Phase 3) | pytest-flake8 removed from test dependencies | ALREADY DONE — not present in `pyproject.toml` or `uv.lock` (confirmed by grep). Research.md noted this was complete before Phase 3 began. The REQUIREMENTS.md traceability table incorrectly marks this as Pending and maps it to Phase 3. No plan claimed it because no action was needed. |

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | — | — | — | No TODO/FIXME/placeholder/empty-implementation patterns found in any of the 4 modified/created files |

---

### Human Verification Required

#### 1. CI Matrix Execution on All Python Versions (PYV-04)

**Test:** Push to master (or open a PR targeting master) to trigger the CI matrix defined in `.github/workflows/ci.yml`
**Expected:** All 12 test jobs (Python 3.10/3.11/3.12/3.13 x SQLite/PostgreSQL/MySQL) pass green; the lint job also passes
**Why human:** Python 3.13 + Pyramid 1.x (pinned `<2`) compatibility was identified as unverified in the Phase 3 research notes: "Pyramid docs show testing through 3.12. Python 3.13 support for Pyramid 1.x is unverified — this is the main risk for PYV-04." Static analysis cannot substitute for actual test execution across all four Python versions.

---

### Requirements Consistency Note

**LNT-03 discrepancy:** REQUIREMENTS.md traceability table maps LNT-03 to Phase 3 with status "Pending," but the requirement was already satisfied during Phase 1 (pytest-flake8 was never added to pyproject.toml). Phase 3 research confirmed this. The REQUIREMENTS.md should be updated: change LNT-03 status to checked `[x]` and update the traceability row to reflect Phase 1 or mark it as "N/A — was never a dep."

**CI-01 description drift:** REQUIREMENTS.md states CI-01 as "GitHub Actions updated to current versions (checkout@v4, setup-python@v5)" — but the implementation correctly uses `checkout@v6` and replaces `setup-python` entirely with `astral-sh/setup-uv@v7`. The requirement's spirit (use current action versions) is satisfied with newer versions. The description in REQUIREMENTS.md should be updated to reflect the actual implementation.

---

## Gaps Summary

No blocking gaps. All six observable truths pass static analysis. All three key artifacts are substantive (not stubs). Both key links are wired. All nine requirement IDs from the PLAN are either satisfied or qualify for human verification.

One item requires human verification before the phase can be declared fully complete: PYV-04 (all tests pass on Python 3.10-3.13) depends on actual CI execution, particularly for Python 3.13 + Pyramid 1.x compatibility.

One documentation inconsistency exists (LNT-03 marked Pending in REQUIREMENTS.md despite being already satisfied) but this does not block the phase goal.

---

_Verified: 2026-02-27_
_Verifier: Claude (gsd-verifier)_
