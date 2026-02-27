---
status: awaiting_human_verify
trigger: "5 test failures in src/kotti/tests/test_file.py found during CI run on Python 3.12"
created: 2026-02-27T00:00:00Z
updated: 2026-02-27T01:00:00Z
---

## Current Focus

hypothesis: CONFIRMED - FieldStorage with filename=None bypasses depot's _is_fieldstorage_like check, causing the FieldStorage object itself to be stored instead of its bytes content
test: Fixed by using `target.filename or "unnamed"` fallback in _save_data
expecting: All 25 test_file.py tests pass; 363 total tests pass with no regressions
next_action: Await human verification

## Symptoms

expected: All tests pass (378 pass, 0 fail)
actual: 5 failures in test_file.py, 378 passed, 367 warnings
errors:
  - FAILED test_file.py::TestFileEditForm::test_edit_without_file - TypeError: a bytes-like object is required, not 'FieldStorage'
  - FAILED test_file.py::TestDepotStore::test_create[File] - TypeError: a bytes-like object is required, not 'FieldStorage'
  - FAILED test_file.py::TestDepotStore::test_edit_content[File] - TypeError: a bytes-like object is required, not 'FieldStorage'
  - FAILED test_file.py::TestUploadedFileResponse::test_unknown_filename - AssertionError: assert 'application/....brew-app-res' == 'application/octet-stream'
  - FAILED test_file.py::TestStoredFileResponse::test_unknown_filename - AssertionError: assert 'application/....brew-app-res' == 'application/octet-stream'
reproduction: Run `uv run pytest src/kotti/tests/test_file.py`
started: Found during first CI run after Phase 3 (CI modernization). Likely pre-existing issues exposed by running on current dependency versions.

## Eliminated

- hypothesis: MIME type failures (test_unknown_filename) are a real bug
  evidence: These tests pass in the current environment - the original report was macOS-specific (system MIME DB returns 'application/...-brew-app-res' for unknown extensions on some macOS builds). On Linux CI these would pass.
  timestamp: 2026-02-27T00:30:00Z

- hypothesis: FileIntent is the right replacement for _to_fieldstorage in _save_data
  evidence: FileIntent bypasses depot's filename-based MIME type guessing (_FileInfo._resolve returns immediately with content_type=None for FileIntent, then falls back to octet-stream), breaking test_guess_content_type. The FieldStorage approach preserves MIME guessing from filename.
  timestamp: 2026-02-27T00:45:00Z

## Evidence

- timestamp: 2026-02-27T00:10:00Z
  checked: depot/io/utils.py _is_fieldstorage_like function
  found: `return (getattr(obj, 'filename', None) is not None and getattr(obj, 'file', None) not in (None, False))`
  implication: A FieldStorage with filename=None fails this check and is treated as an opaque object, not a file container

- timestamp: 2026-02-27T00:15:00Z
  checked: depot/io/memory.py MemoryFileStorage.__save_file
  found: Only calls content.read() if hasattr(content, 'read'). cgi.FieldStorage has no read() method. So when _is_fieldstorage_like returns False for a FieldStorage, the FieldStorage object itself is stored as 'data', not its bytes content.
  implication: When filename=None, FieldStorage stored directly -> later io.BytesIO(FieldStorage) raises TypeError

- timestamp: 2026-02-27T00:20:00Z
  checked: resources.py _save_data method
  found: When value is bytes, it creates FieldStorage via _to_fieldstorage(fp=..., filename=target.filename, ...). If target.filename is None (default for new File(data) calls), filename=None is passed, breaking _is_fieldstorage_like.
  implication: Root cause confirmed. Fix: use `target.filename or "unnamed"` to ensure filename is never None

## Resolution

root_cause: In `SaveDataMixin._save_data` (resources.py line 778), `_to_fieldstorage` was called with `filename=target.filename` which can be `None`. Depot's `_is_fieldstorage_like()` check requires `filename is not None` to recognize the object as a FieldStorage container. When filename is None, depot treats the FieldStorage as an opaque non-file object, stores it directly as bytes data, and later `io.BytesIO(FieldStorage_obj)` raises `TypeError: a bytes-like object is required, not 'FieldStorage'`.

fix: Changed `filename=target.filename` to `filename=target.filename or "unnamed"` in `_to_fieldstorage` call in `_save_data`. This matches depot's own DEFAULT_NAME = 'unnamed' convention and ensures _is_fieldstorage_like() always returns True for these FieldStorage objects.

verification: All 25 test_file.py tests pass. Full suite (363 tests, excluding functional) passes with no regressions.
files_changed:
  - src/kotti/resources.py
