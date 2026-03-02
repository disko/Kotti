# Phase 4: Code Quality and Formatting - Research

**Researched:** 2026-02-28
**Domain:** Python code quality tooling — ruff lint+format, pre-commit hooks, type annotation modernization, exception handling
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Ruff rule selection**
- Comprehensive rule set: pyflakes (F), pycodestyle (E/W), isort (I), bugbear (B), pyupgrade (UP), SIM, RUF
- Auto-fix all safe fixes; review unsafe fixes manually
- Adopt ruff defaults over existing codebase conventions
- Line length: 88 (ruff/Black default)

**Formatting commit strategy**
- First commit in the phase is pure formatting: ruff format + isort applied to entire codebase
- Single commit covering all code (not split by package)
- Set up .git-blame-ignore-revs with .gitattributes config so git blame skips the formatting commit automatically
- Config first approach not needed — formatting commit comes first

**Pre-commit hook scope**
- Hooks: ruff (lint + format), trailing-whitespace, end-of-file-fixer, check-yaml, check-merge-conflict, check-added-large-files, check-toml, debug-statements
- Hooks block the commit on failure (standard enforcement)
- Pre-commit also runs in CI (`pre-commit run --all-files`) as a check
- Pin hook versions to specific tags/SHAs for reproducibility

**Code cleanup boundaries**
- Code duplication removal (CQ-04): conservative — only exact or near-exact repeated blocks, no refactoring for DRY-ness
- pyupgrade modernizations (LNT-05): all safe modernizations — super() without args, X | None union syntax, f-strings, etc. (Python 3.10+ target makes all safe)
- Type annotations (CQ-02): modernize to X | None syntax, replace Union[X, None] and Optional[X], add `from __future__ import annotations` where needed
- Deprecation warnings (CQ-03): add DeprecationWarning for any public API changes made during this phase

### Claude's Discretion

- Bare except handler replacements (CQ-01): Claude reads each handler in alembic/env.py and views/cache.py and picks the most appropriate specific exception type
- Exact ruff rule configuration details beyond the selected rule sets
- Order of linting fix commits after the initial formatting commit

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| LNT-01 | ruff configured for linting in pyproject.toml (replaces flake8) | Ruff config with full ruleset (E,W,F,I,B,UP,SIM,RUF) documented below; existing partial config must be expanded |
| LNT-02 | ruff configured for formatting in pyproject.toml (replaces black/isort) | `[tool.ruff.format]` section with line-length=88; no additional keys needed for defaults |
| LNT-03 | pytest-flake8 removed from test dependencies | Verified absent from pyproject.toml and uv.lock — already done in earlier phases; no action needed |
| LNT-04 | Formatting applied in isolated first commit (preserves git blame) | Formatting commit strategy + .git-blame-ignore-revs + .gitattributes fully documented |
| LNT-05 | pyupgrade-style modernizations applied (super(), union syntax, etc.) | 452 violations measured; 308 safe-fixable via `ruff --fix`; UP rules handle all pyupgrade modernizations |
| LNT-06 | pre-commit hooks configured (.pre-commit-config.yaml) | Full hook config documented; ruff-pre-commit v0.15.4, pre-commit-hooks v6.0.0 pinned |
| CQ-01 | Bare except handlers replaced with specific exceptions (alembic/env.py, views/cache.py) | Both handlers analyzed; specific exception choices documented |
| CQ-02 | Union[int, "NoneType"] patterns replaced with Optional[int] or X \| None syntax | 63 UP007+UP045 violations; all auto-fixable; `from __future__ import annotations` required in some files |
| CQ-03 | Deprecation warnings added for any changed public APIs | No public API changes expected in this phase; B028 stacklevel fixes for existing warnings documented |
| CQ-04 | Code duplication identified and removed where safe | Conservative approach; no obvious exact-block duplication found; B015/B018 useless-expression cleanup is primary CQ-04 work |
</phase_requirements>

## Summary

Phase 4 is primarily a tooling configuration and mechanical code cleanup phase. The codebase already has a partial ruff configuration (targeting `E4,E7,E9,F` rules only, with `E711,E721,F821,F841` intentionally deferred). Phase 4 expands this to the full agreed ruleset (`E,W,F,I,B,UP,SIM,RUF`) with `E711,E721,F821,F841` re-examined and resolved.

A full violation inventory was run against the proposed ruleset: **452 violations across 65 files**, of which **392 are auto-fixable** with `ruff --fix` (including 84 that need `--unsafe-fixes`). The remaining ~60 violations require manual fixes. The single largest category is I001 (159 unsorted import blocks), all auto-fixable. The formatting-only commit will touch 51 files.

The pre-commit infrastructure is entirely absent — `.pre-commit-config.yaml` does not exist. The CI lint job currently only runs `ruff check .` (not `ruff format --check`). Both gaps must be closed. The phase has a strict commit ordering constraint: formatting first (isolated commit), then config changes, then linting fixes, then pre-commit setup.

**Primary recommendation:** Run ruff fixes in two passes — (1) `ruff format` in an isolated commit, (2) `ruff check --fix --select "E,W,F,I,B,UP,SIM,RUF"` for the bulk of mechanical fixes, then handle the 55 RUF059 unsafe fixes and ~10 manual cases in targeted commits.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| ruff | >=0.11 (installed: 0.15.4) | Lint + format (replaces flake8, black, isort, pyupgrade) | Single-tool replacement for entire Python code quality stack |
| pre-commit | latest (install via uv tool) | Git hook management | Industry standard; hooks run same checks locally and in CI |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| ruff-pre-commit | v0.15.4 | Pre-commit integration for ruff | Always pair with ruff; pins hook to exact ruff version |
| pre-commit-hooks | v6.0.0 | Standard utility hooks (trailing-whitespace, etc.) | Complementary hooks for non-language-specific hygiene |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| ruff format | black | ruff is faster and already installed; black adds a dependency |
| ruff check --select I | isort standalone | ruff's I001 handles import sorting; isort is redundant |
| pre-commit | local shell hooks | pre-commit provides version pinning, language management, CI compatibility |

**Installation:**
```bash
# ruff is already a dev dependency in pyproject.toml
# pre-commit installed as tool (not project dep):
uv tool install pre-commit
```

## Architecture Patterns

### Recommended pyproject.toml ruff Configuration

```toml
[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "RUF"]
ignore = [
    "F821",   # Undefined name — false positives on forward references in security.py, filedepot.py
    "B008",   # Function call in default argument — intentional pattern in views/login.py (translation), views/users.py
    "SIM300", # Yoda conditions — 9 violations, all in test files; test assert style is subjective
]

[tool.ruff.lint.per-file-ignores]
"src/kotti/tests/**/*.py" = [
    "B018",   # Useless expression — intentional side-effect-triggering property access in test_util_views.py
]

[tool.ruff.format]
# All defaults acceptable (double-quotes, 4-space indent, auto line endings)
```

**Notes on ignored rules:**
- `F821`: String annotations like `"Node"` and `"Request"` in security.py trigger F821 (undefined name). The correct fix is `from __future__ import annotations` — but this interacts with SQLAlchemy's declarative model system. Safer to keep ignoring or add `# noqa: F821` per-occurrence.
- `B008`: The `_("You have reset your password.")` default arg in `views/login.py:271` is a deliberate i18n pattern. `PrincipalFull()` defaults in `views/users.py` (3 occurrences) are existing API that cannot be changed without a deprecation cycle. Ignore globally.
- `SIM300`: 9 Yoda condition violations, all in test files. The pytest convention is mixed (either `assert expected == actual` or `assert actual == expected`). Fixing these is mechanical but subjective; ignoring avoids churn in test files.

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.4
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: check-toml
      - id: debug-statements
```

**Version pinning rationale:** `rev: v0.15.4` pins the ruff hook to the exact version installed in the project. This ensures CI and local dev see identical results. Update via `pre-commit autoupdate` during maintenance.

### Git Blame Preservation

```bash
# After the formatting commit, capture its SHA:
FORMATTING_SHA=$(git rev-parse HEAD)

# Create .git-blame-ignore-revs:
echo "# Formatting-only commit — ruff format applied to entire codebase" > .git-blame-ignore-revs
echo "$FORMATTING_SHA" >> .git-blame-ignore-revs

# Configure .gitattributes for git blame to auto-use:
echo ".git-blame-ignore-revs export-ignore" >> .gitattributes
```

And configure git locally (developers run once):
```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

GitHub respects `.git-blame-ignore-revs` automatically in the web UI as of 2022.

### Bare Except Handler Analysis

**`src/kotti/alembic/env.py` (line 28):**
```python
try:
    context.run_migrations()
    mark_changed(DBSession())
except:  # noqa: E722
    traceback.print_exc()
    transaction.abort()
```
This catch-all is protecting a migration run. The intent is to abort the transaction on ANY error (including SystemExit, KeyboardInterrupt). Correct replacement: `except Exception:` — this catches all non-system exceptions (regular exceptions + database errors) while allowing `SystemExit` and `KeyboardInterrupt` to propagate. The `traceback.print_exc()` already handles logging.

**`src/kotti/views/cache.py` (line 116):**
```python
try:
    caching_policy = caching_policy_chooser(context, request, response)
except:  # noqa: E722
    logger.exception(f"{caching_policy_chooser} raised an exception.")
```
This is a defensive catch wrapping a user-provided callable. Intent is to never let a bad caching policy break a response. Correct replacement: `except Exception:` — same rationale; user code won't raise `SystemExit`.

### Type Annotation Modernization (CQ-02)

**Violation counts:**
- UP045 (Optional[X] → X | None): 50 violations
- UP007 (Union[X, Y] → X | Y): 13 violations
- UP035 (deprecated typing imports): 18 violations
- UP006 (typing.List → list, typing.Dict → dict): 25 violations

All 63 UP045+UP007 violations are auto-fixable with `ruff check --fix`. UP006/UP035 (deprecated generic imports) are also auto-fixable.

**Critical: `from __future__ import annotations`**

Files with string-quoted forward references (`"Node"`, `"NestedGroup"`, `"NoneType"`) need special handling:

- `src/kotti/security.py`: `"Node"` and `"Request"` in function signatures — these are string annotations to avoid circular imports. Adding `from __future__ import annotations` would allow removing the quotes AND resolve the F821 false positives. However, SQLAlchemy 1.4's ORM introspects annotations at class definition time; `from __future__ import annotations` makes all annotations lazy (PEP 563), which can break `sqlalchemy.orm.relationship()` and column type inference. **Safe approach: keep F821 in the ignore list for security.py and add per-line noqa comments instead of blanket __future__ import.**
- `src/kotti/filedepot.py`: `"NoneType"` in return type — this is invalid anyway (`NoneType` is not accessible). Replace with `None` in the return type annotation.
- `src/kotti/resources.py`: `"Node"` in `__getitem__` — forward reference to avoid circular import; same SQLAlchemy concern applies.

**Practical approach:** Use `ruff --fix` for all UP007/UP045/UP006/UP035. Then manually add `from __future__ import annotations` only to files that don't use SQLAlchemy ORM relationship introspection (view files, utility modules). Keep F821 ignored for ORM model files.

### Anti-Patterns to Avoid

- **Don't add `from __future__ import annotations` to ORM model files**: SQLAlchemy 1.4 (pinned until Phase FWK-02) introspects annotations at class-definition time. The `from __future__ import annotations` directive (PEP 563) makes all annotations strings lazily evaluated, breaking `Column()` and `relationship()` type inference in declarative models.
- **Don't apply unsafe RUF059 fixes blindly**: The 55 `RUF059` violations (unused unpacked variables) require renaming variables to `_x` form. This is safe in production code but requires checking that the variable isn't used later or in test assertions.
- **Don't apply SIM300 (Yoda) fixes in test files**: Pytest assert formatting is a style choice; flipping `assert [expected] == var` to `assert var == [expected]` changes nothing semantically but creates noisy diff.
- **Don't run `ruff format` and `ruff check --fix` in the same commit**: The formatting commit must be isolated for git blame preservation.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Import sorting | Manual import reordering | `ruff check --fix --select I` | I001 affects 159 import blocks; ruff handles all isort-style rules |
| Type annotation updates | Find-and-replace Union/Optional | `ruff check --fix --select UP` | UP rules handle all 88 UP-category violations safely and atomically |
| Pre-commit hook scripts | Custom bash hooks in .git/hooks/ | .pre-commit-config.yaml | pre-commit handles version management, CI compatibility, hook installation |
| noqa comment cleanup | Manual search for stale noqa | `ruff check --fix --select RUF100` | 23 unused noqa directives; all auto-fixable |

**Key insight:** The ruff `--fix` pass eliminates the vast majority of manual work. The remaining manual effort is ~10 cases (bare excepts, B015 pointless comparisons in tests, B018 in non-test code, E501 long lines in docstrings/comments).

## Common Pitfalls

### Pitfall 1: noqa Comments Become Stale After Rule Expansion
**What goes wrong:** The current config ignores E711/E721/F821/F841. Several existing `# noqa: E722` comments (bare except suppression) will become `RUF100` (unused noqa) violations once E722 is enabled and the bare excepts are fixed.
**Why it happens:** noqa suppresses specific rule codes; when the rule is no longer triggered (because the code is fixed), the noqa becomes dead.
**How to avoid:** Fix the violations first, THEN run `ruff check --fix --select RUF100` to clean up dead noqa comments in a separate pass.
**Warning signs:** RUF100 violations appearing after other fixes are applied.

### Pitfall 2: Formatting Commit SHA Must Be Captured Immediately
**What goes wrong:** Developer applies `ruff format`, stages all changes, and commits — but forgets to capture the SHA before moving on. Now they must `git log` to find it.
**Why it happens:** The .git-blame-ignore-revs file must contain the formatting commit SHA, which isn't known until after the commit is made.
**How to avoid:** The plan task for the formatting commit must include the step to append the new SHA to .git-blame-ignore-revs as the very next action.
**Warning signs:** .git-blame-ignore-revs exists but is empty, or contains a placeholder.

### Pitfall 3: ruff format Versus ruff check --fix Order
**What goes wrong:** Running `ruff check --fix` before `ruff format` means the format check will still fail, requiring another commit. The formatting commit must be 100% formatting only.
**Why it happens:** `ruff check --fix` makes code changes (import sorting, annotation syntax) that may affect how `ruff format` subsequently formats the code.
**How to avoid:** Strict ordering: (1) `ruff format` commit isolated, (2) `ruff check --fix` for lint violations in subsequent commits.

### Pitfall 4: CI Lint Job Does Not Check Formatting
**What goes wrong:** The existing CI lint job only runs `ruff check .` — it does NOT run `ruff format --check .`. After Phase 4, the format check must also be part of CI.
**Why it happens:** The Phase 3 CI job was created with only the linting check; format checking was deferred.
**How to avoid:** Update the CI lint job to add `uv run ruff format --check .` as a separate step (or add pre-commit CI job instead).

### Pitfall 5: B008 Violations Have Intentional Patterns
**What goes wrong:** Auto-fixing or blindly suppressing B008 (function call in default argument) would flag legitimate translation function calls (`_("...")`) and `PrincipalFull()` schema defaults that are intentional API patterns.
**Why it happens:** B008 is generally valid but has exceptions for i18n patterns and schema defaults.
**How to avoid:** Ignore B008 globally in the ruff config (already identified above).

### Pitfall 6: RUF059 Unsafe Fixes Can Break Test Assertions
**What goes wrong:** RUF059 flags unused unpacked variables (e.g., `[email1, email2, email3] = mailer.outbox` where email1 is unused). The unsafe fix renames to `_email1`. If a later test assertion accidentally references the old name, a NameError occurs.
**Why it happens:** Renaming variables is considered "unsafe" because ruff cannot statically guarantee the variable isn't referenced in complex dynamic code.
**How to avoid:** Apply RUF059 fixes one file at a time, run tests after each file's changes.

## Code Examples

### Complete pyproject.toml ruff Section

```toml
# Source: verified against ruff 0.15.4 docs and codebase violation analysis
[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "RUF"]
ignore = [
    "F821",   # Undefined name — forward ref false positives in ORM model files
    "B008",   # Function call in default argument — intentional i18n and schema patterns
    "SIM300", # Yoda conditions — test file assert style preference
]

[tool.ruff.lint.per-file-ignores]
"src/kotti/tests/**/*.py" = [
    "B018",  # Useless expression — intentional property-access side effects in test_util_views.py
]
```

### Formatting Commit Sequence

```bash
# Step 1: Apply formatting only
uv run ruff format .

# Step 2: Stage all formatting changes
git add -A

# Step 3: Commit (isolated)
git commit -m "style: apply ruff format to entire codebase"

# Step 4: Capture SHA for git-blame-ignore-revs
FORMATTING_SHA=$(git rev-parse HEAD)

# Step 5: Create .git-blame-ignore-revs
cat > .git-blame-ignore-revs << EOF
# Formatting-only commit: ruff format applied to entire codebase
$FORMATTING_SHA
EOF

# Step 6: Update .gitattributes
echo ".git-blame-ignore-revs export-ignore" >> .gitattributes
git config blame.ignoreRevsFile .git-blame-ignore-revs

# Step 7: Add both files to next commit
git add .git-blame-ignore-revs .gitattributes
```

### Bulk Lint Fix Sequence

```bash
# Pass 1: all safe auto-fixes (308 violations)
uv run ruff check --fix --select "E,W,F,I,B,UP,SIM,RUF" --ignore "F821,B008,SIM300" .

# Pass 2: unsafe fixes after manual review (55 RUF059 + ~29 others)
# Review the diff carefully before applying:
uv run ruff check --fix --unsafe-fixes --select "RUF059" .

# Pass 3: verify format still clean
uv run ruff format --check .

# Pass 4: final check — should be zero violations
uv run ruff check --select "E,W,F,I,B,UP,SIM,RUF" --ignore "F821,B008,SIM300" .
```

### Bare Except Fixes

```python
# alembic/env.py — replace bare except with Exception:
# Before:
except:  # noqa: E722
    traceback.print_exc()
    transaction.abort()

# After:
except Exception:
    traceback.print_exc()
    transaction.abort()

# views/cache.py — replace bare except with Exception:
# Before:
except:  # noqa: E722
    logger.exception(f"{caching_policy_chooser} raised an exception.")

# After:
except Exception:
    logger.exception(f"{caching_policy_chooser} raised an exception.")
```

### CI Lint Job Update

```yaml
# .github/workflows/ci.yml — update lint job to also check formatting
  lint:
    name: Lint (ruff)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install uv and Python
        uses: astral-sh/setup-uv@v7
        with:
          python-version: "3.12"
          enable-cache: true

      - name: Install project
        run: uv sync --locked --group test

      - name: Run ruff check
        run: uv run ruff check .

      - name: Run ruff format check
        run: uv run ruff format --check .

      - name: Run pre-commit
        run: |
          uv tool install pre-commit
          pre-commit run --all-files
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| flake8 + black + isort + pyupgrade | ruff (all-in-one) | ruff 0.1+ (2023) | Single tool, 10-100x faster, one config section |
| typing.Optional[X] | X \| None | Python 3.10 / PEP 604 | Shorter syntax, native to language |
| typing.List, typing.Dict | list, dict | Python 3.9 / PEP 585 | Deprecated imports; use builtins directly |
| bare `except:` | `except Exception:` | Python best practices (always) | Allows SystemExit/KeyboardInterrupt to propagate |
| git hooks in .git/hooks/ | pre-commit framework | ~2015+ | Version-controlled, shareable, multi-language |

**Deprecated/outdated:**
- `typing.Optional`, `typing.Union`, `typing.List`, `typing.Dict`, `typing.Tuple`, `typing.Set`, `typing.Callable`: All deprecated since Python 3.9 (PEP 585) or 3.10 (PEP 604). Kotti's target of 3.10+ means these can all be replaced.
- `u"string"` prefix: Python 3 doesn't need `u""` prefix; UP025 flags 2 occurrences in docs/conf.py.
- `.format()` when f-strings suffice: UP032 flags 14 occurrences.

## Open Questions

1. **F821 and SQLAlchemy ORM model files**
   - What we know: `"Node"`, `"Request"` in string annotations in security.py trigger F821. Adding `from __future__ import annotations` would resolve these but risks breaking SQLAlchemy 1.4 ORM introspection.
   - What's unclear: Exactly which files are safe to add `__future__` annotations to without breaking SQLAlchemy behavior.
   - Recommendation: Keep F821 in the global ignore list. Add targeted `# noqa: F821` comments on the specific forward-ref lines in security.py. For the `"NoneType"` in filedepot.py (invalid annotation), replace with `None` directly.

2. **B015 pointless comparisons in test_sqla.py**
   - What we know: Three B015 violations in test_sqla.py where a comparison expression has no effect (missing `assert`). These look like real bugs — missing asserts that should verify behavior.
   - What's unclear: Were these intentionally written without assert (testing that the code doesn't crash) or are they bugs (the test never actually asserts)?
   - Recommendation: Read each B015 case in context and add `assert` where the intent is clear, or convert to a comment explaining intent.

3. **E711/E721 deferred rules — should they be enabled in Phase 4?**
   - What we know: The STATE.md says E711/E721 were "deferred to Phase 4 code quality work." The CONTEXT.md doesn't explicitly say to re-enable them in the final ruleset.
   - What's unclear: The CONTEXT.md's rule selection (`E,W,F,I,B,UP,SIM,RUF`) uses the full `E` selector which would include E711/E721 — so they ARE included unless explicitly ignored.
   - Recommendation: Enable E711 and E721 (they're in the `E` selector). There are only 2 E711 and 6 E721 violations. E721 has unsafe fixes only (type comparison → isinstance); E711 is auto-fixable. Apply E721 fixes manually.

## Violation Inventory (for Planning)

Complete count of violations under proposed ruleset (`E,W,F,I,B,UP,SIM,RUF` minus `F821,B008,SIM300`):

| Rule | Count | Category | Fix Method | Manual Work |
|------|-------|----------|------------|-------------|
| I001 | 159 | Import sorting | `ruff --fix` | None |
| RUF059 | 55 | Unused unpacked vars | `--unsafe-fixes` | Review each |
| UP045 | 50 | Optional → X\|None | `ruff --fix` | None |
| UP006 | 25 | typing.List → list | `ruff --fix` | None |
| RUF100 | 23 | Dead noqa comments | `ruff --fix` | None |
| UP035 | 18 | Deprecated typing imports | `ruff --fix` | None |
| SIM117 | 17 | Nested with → combined | `ruff --fix` | None |
| UP032 | 14 | .format() → f-string | `ruff --fix` | None |
| UP007 | 13 | Union[X,Y] → X\|Y | `ruff --fix` | None |
| E501 | 7 | Line too long | Manual | 7 lines |
| SIM108 | 6 | if/else → ternary | `ruff --fix` | None |
| RUF005 | 6 | list concat → spread | `ruff --fix` | None |
| SIM118 | 5 | key in dict.keys() | `ruff --fix` | None |
| B904 | 5 | raise without from | Manual | 5 raises |
| B018 | 5 | Useless expression | noqa or fix | 2 manual |
| RUF012 | 4 | Mutable class attr | Manual | 4 fixes |
| B028 | 4 | warnings stacklevel | Manual | 4 fixes |
| B015 | 4 | Pointless comparison | Manual | 4 test fixes |
| B010 | 3 | setattr → assignment | `ruff --fix` | None |
| UP025 | 2 | u"str" prefix | `ruff --fix` | None |
| RUF013 | 2 | Implicit Optional | `ruff --fix` | None |
| B007 | 2 | Unused loop var | Manual | 2 renames |
| E711 | 2 | == None → is None | `ruff --fix` | None |
| E721 | 6 | type() == → isinstance | `--unsafe-fixes` | Review |
| F841 | 4 | Assigned unused var | Manual | 4 removals |
| Others | ~5 | misc | Mixed | Small |
| **TOTAL** | **~452** | | **~392 auto** | **~60 manual** |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8+ |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `uv run pytest src/kotti/tests/test_cache.py -x -q` |
| Full suite command | `uv run pytest` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LNT-01 | `ruff check .` passes with zero violations | smoke | `uv run ruff check .` | N/A (CLI tool) |
| LNT-02 | `ruff format --check .` passes with zero violations | smoke | `uv run ruff format --check .` | N/A (CLI tool) |
| LNT-03 | pytest-flake8 absent from dependencies | smoke | `grep -r pytest.flake8 pyproject.toml uv.lock` (expects no match) | N/A (config check) |
| LNT-04 | Formatting commit is isolated (git blame clean) | manual | `git log --oneline -5` (visual check) | N/A (process) |
| LNT-05 | No pyupgrade-style violations remain | smoke | `uv run ruff check --select UP .` (expects 0) | N/A (CLI tool) |
| LNT-06 | pre-commit run --all-files passes | smoke | `pre-commit run --all-files` | ❌ Wave 0: `.pre-commit-config.yaml` |
| CQ-01 | No bare `except:` in alembic/env.py or views/cache.py | unit | `uv run pytest src/kotti/tests/test_cache.py -x -q` | ✅ exists |
| CQ-02 | No Union[]/Optional[] patterns remain | smoke | `uv run ruff check --select UP045,UP007,UP006,UP035 .` | N/A (CLI tool) |
| CQ-03 | DeprecationWarning for public API changes | unit | `uv run pytest src/kotti/tests/test_deprecated.py -x -q` | ✅ exists |
| CQ-04 | Pointless/useless expressions removed | smoke | `uv run ruff check --select B015,B018 .` | N/A (CLI tool) |

### Sampling Rate
- **Per task commit:** `uv run ruff check . && uv run pytest src/kotti/tests/test_cache.py -x -q`
- **Per wave merge:** `uv run pytest` (full suite)
- **Phase gate:** `uv run ruff check . && uv run ruff format --check . && pre-commit run --all-files && uv run pytest`

### Wave 0 Gaps
- [ ] `.pre-commit-config.yaml` — covers LNT-06; must be created before pre-commit can be verified

*(No test infrastructure gaps — existing test files cover all unit-level requirements. Smoke tests are CLI commands, not test files.)*

## Sources

### Primary (HIGH confidence)
- `/astral-sh/ruff` Context7 — pyproject.toml configuration, pre-commit hook configuration, rule selection
- `/pre-commit/pre-commit-hooks` Context7 — available hooks and their YAML configuration
- `uv run ruff check` — live violation counts run against actual codebase (ruff 0.15.4)
- `uv run ruff format --check` — live formatting check against actual codebase
- GitHub API — `ruff-pre-commit` latest tag: v0.15.4; `pre-commit-hooks` latest tag: v6.0.0

### Secondary (MEDIUM confidence)
- Ruff documentation on `from __future__ import annotations` and SQLAlchemy 1.x interaction — based on known SQLAlchemy 1.x behavior with PEP 563; not explicitly documented in ruff docs
- `.git-blame-ignore-revs` behavior — GitHub web UI support documented in GitHub blog post 2022

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — ruff 0.15.4 confirmed installed; pre-commit hook versions confirmed via GitHub API
- Architecture patterns: HIGH — all configs verified against live codebase violations
- Pitfalls: HIGH — all pitfalls identified from actual violation analysis, not theoretical
- Violation inventory: HIGH — counts from live ruff run; breakdown precise to individual rules

**Research date:** 2026-02-28
**Valid until:** 2026-03-28 (ruff releases frequently; re-verify hook versions if > 2 weeks before planning)
