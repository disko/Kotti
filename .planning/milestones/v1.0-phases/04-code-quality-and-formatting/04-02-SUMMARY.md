---
phase: 04-code-quality-and-formatting
plan: 02
subsystem: code-quality
tags: [ruff, linting, type-annotations, python310, code-modernization]

# Dependency graph
requires:
  - phase: 04-01
    provides: expanded ruff ruleset with E,W,F,I,B,UP,SIM,RUF rules configured
provides:
  - zero ruff violations across entire codebase
  - modernized type annotations (X | None syntax throughout)
  - bare except -> except Exception in alembic/env.py and views/cache.py
  - proper exception chaining (raise ... from err) in resources, security, traversal
  - B028 stacklevel added to all warnings.warn() calls
  - pointless test comparisons converted to assertions
  - stale noqa comments removed
affects: [05-documentation, future-maintenance]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "SQLAlchemy ORM column comparisons use == None not is None (generates IS NULL SQL)"
    - "RUF012 mutable class attrs in ORM/framework classes use # noqa: RUF012"
    - "Nested with statements collapsed to single with A, B: or with (A, B): form"
    - "typing.Optional/Union -> X | None / X | Y union syntax throughout"

key-files:
  created: []
  modified:
    - src/kotti/alembic/env.py
    - src/kotti/views/cache.py
    - src/kotti/resources.py
    - src/kotti/security.py
    - src/kotti/traversal.py
    - src/kotti/testing.py
    - src/kotti/filedepot.py
    - src/kotti/message.py
    - src/kotti/tests/test_app.py
    - src/kotti/tests/test_sqla.py
    - src/kotti/tests/test_search.py

key-decisions:
  - "[04-02]: SQLAlchemy ORM filter Node.parent_id == None must NOT be changed to is None — ruff E711 fix reverted with # noqa: E711"
  - "[04-02]: RUF012 for SQLAlchemy __mapper_args__, Pyramid __acl__, DummyRequest.POST get # noqa: RUF012 (framework-managed)"
  - "[04-02]: B015 pointless comparisons in tests (test_sqla.py, test_node.py) fixed to assert statements"
  - "[04-02]: typing.Tuple/Optional/Union removed from security.py and filedepot.py — replaced with builtin tuple/X|None syntax"

patterns-established:
  - "ORM column == None comparisons: use # noqa: E711 to suppress false-positive lint"
  - "Framework mutable class attrs: use # noqa: RUF012 rather than ClassVar annotations"

requirements-completed: [LNT-05, CQ-01, CQ-02, CQ-03, CQ-04]

# Metrics
duration: 20min
completed: 2026-02-28
---

# Phase 4 Plan 2: Lint Violation Resolution Summary

**Zero ruff violations achieved: 452 violations fixed via bulk auto-fix (313), unsafe fix pass (93), and manual fixes (46) covering bare excepts, type annotations, exception chaining, and pointless comparisons**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-02-28T00:44:22Z
- **Completed:** 2026-02-28T01:04:14Z
- **Tasks:** 2
- **Files modified:** 44 src files + 1 planning file

## Accomplishments

- Eliminated all 452 ruff lint violations — codebase now exits clean on `ruff check .`
- Modernized type annotations: `Optional[X]` -> `X | None`, `Union[X, Y]` -> `X | Y`, `typing.List/Dict/Tuple` -> builtin forms
- Fixed both bare `except:` handlers in alembic/env.py and views/cache.py -> `except Exception:`
- Added proper `raise ... from err` / `raise ... from None` exception chaining in resources.py, security.py, traversal.py
- Collapsed 16 nested `with` statements (SIM117) across test files into single multi-context form
- Converted 4 pointless test comparisons (B015) to proper `assert` statements

## Task Commits

Each task was committed atomically:

1. **Task 1: Bulk auto-fix safe lint violations** - `b3757fbd` (fix)
2. **Task 2: Fix manual violations, bare excepts, unsafe fixes, and clean up stale noqa** - `a8753220` (fix)

**Plan metadata:** (docs commit to follow)

## Files Created/Modified

- `src/kotti/alembic/env.py` - bare except -> except Exception
- `src/kotti/views/cache.py` - bare except -> except Exception
- `src/kotti/resources.py` - type annotations modernized, raise-from, RUF012 noqa, SQLAlchemy E711 preserved
- `src/kotti/security.py` - typing.Tuple/Optional/Union removed, raise-from, B904 fixed
- `src/kotti/traversal.py` - raise-from for URLDecodeError, long line broken
- `src/kotti/filedepot.py` - typing.Dict/List removed, long docstring line broken
- `src/kotti/message.py` - long line broken into readable form
- `src/kotti/testing.py` - RUF012 noqa for POST/acl, B018 fixed, E402 noqa for late import
- `src/kotti/tests/test_app.py` - 10 nested with statements collapsed to single form
- `src/kotti/tests/test_sqla.py` - 3 pointless comparisons -> assert statements, RUF040 fixed
- `src/kotti/alembic/versions/413fa5fcc581_add_filedepot.py` - E741 ambiguous `l` -> `lst`

## Decisions Made

- SQLAlchemy ORM `filter(Node.parent_id == None)` kept as-is with `# noqa: E711` — ruff's E711 "fix" converts `== None` to `is None` which breaks the ORM query (Python `is None` on a column attribute evaluates to `True` not generating `IS NULL`)
- RUF012 violations in framework-managed attributes (SQLAlchemy `__mapper_args__`, Pyramid `__acl__`, test `DummyRequest.POST`) suppressed with `# noqa: RUF012` rather than `ClassVar` annotations which would confuse the frameworks
- B015 pointless comparisons in test_sqla.py converted to real assertions — these were genuine test bugs (results were computed but never asserted)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Reverted SQLAlchemy ORM E711 mis-fix**
- **Found during:** Task 2 (running full test suite)
- **Issue:** Bulk ruff auto-fix changed `Node.parent_id == None` to `Node.parent_id is None` inside a SQLAlchemy `bakery()` lambda. In Python, `Column is None` evaluates to `True` (Python identity check), not `IS NULL` SQL. This broke `DefaultRootCache.root_id` which returns `NoResultFound`.
- **Fix:** Reverted to `Node.parent_id == None  # noqa: E711` — the `== None` form generates the correct `IS NULL` SQL expression
- **Files modified:** `src/kotti/resources.py`
- **Verification:** `test_app.py::TestApp::test_override_settings` passes
- **Committed in:** a8753220 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - bug)
**Impact on plan:** Critical correctness bug caught and fixed. The SQLAlchemy ORM pattern is now explicitly documented as requiring `== None` (not `is None`) for column comparisons.

## Issues Encountered

- The bulk ruff E711 auto-fix (Task 1) incorrectly converted a SQLAlchemy ORM query filter from `== None` to `is None`, causing `NoResultFound` in `DefaultRootCache.root_id`. Caught by test suite in Task 2. Fixed by reverting with `# noqa: E711` comment.
- RUF100 (stale noqa cleanup) pass removed freshly-added `# noqa: RUF012` comments that were added during the same execution. Required re-adding them after the cleanup pass. This is expected behavior — RUF100 must run last, after all violations are fixed.

## Next Phase Readiness

- Phase 4, Plan 3 (documentation) can proceed — zero lint violations, all tests green
- The SQLAlchemy `== None` pattern documented as a known exception to E711 rule
- All CQ-01 through CQ-04 requirements satisfied

---
*Phase: 04-code-quality-and-formatting*
*Completed: 2026-02-28*
