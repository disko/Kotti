# Automated Tests

Kotti uses [pytest](http://pytest.org), [zope.testbrowser](http://pypi.python.org/pypi/zope.testbrowser) and [WebTest](http://webtest.pythonpaste.org) for automated testing.

## Running the tests

Before you can run the tests, you must install Kotti's `testing` extras.
Inside your Kotti checkout directory, using uv:

```bash
uv sync --group testing
uv run pytest
```

Or with pip in a virtualenv:

```bash
bin/pip install -e ".[testing]"
bin/pytest
```

## Using Kotti's test fixtures/funcargs in third party add-ons' tests

To be able to use all of Kotti's fixtures and funcargs in your own package's tests, you only need to "include" them with a line like this in your `conftest.py` file:

```python
pytest_plugins = "kotti"
```

### Available fixtures

For the full testing API, see the [kotti.testing API reference](../../api/kotti.testing.md).

## Continuous Integration

Kotti is tested against Python 3.10–3.13 as well as SQLite, MySQL, and PostgreSQL (in every combination) on every commit and pull request via [GitHub Actions](https://github.com/Kotti/Kotti/actions).

If you want your add-on packages to be tested the same way with additional testing against multiple versions of Kotti (including the current master), you can add a GitHub Actions workflow file to your repo.
See the [Kotti Actions workflow](https://github.com/Kotti/Kotti/tree/master/.github/workflows) for an example to base yours on.
