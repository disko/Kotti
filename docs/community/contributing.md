# Contributing

The Kotti project can use your help in developing the software, requesting features, reporting bugs, writing developer and end-user documentation — the usual assortment for an open source project.

Please devote some of your time to the project.

## Contributing to the Code Base

To contribute to Kotti itself, and to test and run against the master branch (the current development code base), first create an account on GitHub if you don't have one.
Fork [Kotti](https://github.com/Kotti/Kotti) to your GitHub account, and follow the usual steps to get a local clone, with `origin` as your fork, and with `upstream` as the Kotti/Kotti repo.
Then, you will be able to make branches for contributing, etc.
Please read the docs on GitHub if you are new to development, but the steps, after you have your own fork, would be something like this:

```bash
git clone https://github.com/your_github/Kotti.git

cd Kotti

git remote add upstream git://github.com/Kotti/Kotti.git
```

Now you should be set up to make branches for this and that, doing a pull request from a branch, and the usual git procedures.
You may wish to read the [GitHub fork-a-repo help](https://help.github.com/articles/fork-a-repo).

To run and develop within your clone, install Kotti with its development dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv sync --group testing
```

Or with pip in a virtualenv:

```bash
python3 -m venv .
bin/pip install -e ".[testing]"
```

Run `uv pip install kotti_someaddon`, and add a `kotti_someaddon` entry to `app.ini`, as you would do normally, to use add-ons.

## Running the Tests

To run Kotti's test suite:

```bash
uv run pytest
```

Or with the virtualenv activated:

```bash
bin/pytest
```

## Contributing to Developer Docs

Kotti's documentation now uses [MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
Use the normal git procedures for first making a branch, e.g., `navigation_docs`, then after making changes, commit, push to this branch on your fork, and do a pull request from there, just as you would for contributing to the code base.

In your Kotti clone you can install the requirements for building and viewing the documents locally:

```bash
uv sync --group docs
```

Or with pip:

```bash
pip install -e ".[docs]"
```

Then serve the docs locally:

```bash
uv run mkdocs serve
```

Or build them:

```bash
uv run mkdocs build
```

Then you can check the built HTML files in the `site/` directory locally, before you do an actual pull request.

The rendered docs are built and hosted on [ReadTheDocs](https://kotti.readthedocs.io/).

## Contributing to User Docs

The [Kotti User Manual](https://kotti-user-manual.readthedocs.io) is a separate project.
Please follow the readme instructions in the [Kotti User Manual repo](https://github.com/Kotti/kotti_user_manual) to get set up for contributing to the user manual.
