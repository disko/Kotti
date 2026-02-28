# Kotti Documentation

Kotti is a high-level, Pythonic web application framework based on [Pyramid](https://docs.pylonsproject.org/projects/pyramid/) and [SQLAlchemy](https://www.sqlalchemy.org/).
It includes an extensible Content Management System called the **Kotti CMS**.

If you are a user of a Kotti site who was referred here, you will likely want to go directly to the [Kotti User Manual](https://kotti-user-manual.readthedocs.io/).

The documentation below is for **developers** of Kotti or applications built on top of it.

---

## Getting Started

Get an [overview](guides/getting-started/overview.md) of what you can do with Kotti, how to [install](guides/getting-started/installation.md) it and how to [create](guides/getting-started/tutorial.md) your first Kotti project or add-on.

## Guides

The [Guides](guides/getting-started/overview.md) tab contains:

- **[Getting Started](guides/getting-started/overview.md)** — Overview, installation, and the step-by-step tutorial
- **[User Guide](guides/user-guide/developer-manual.md)** — Developer manual, security, configuration, testing, translations, deployment, and advanced topics

## API Reference

The [API](api/index.md) tab provides generated API documentation for all Kotti modules, extracted from source docstrings.

## Community

- [Getting Help](community/help.md)
- [Contributing](community/contributing.md)
- [Changelog](community/changelog.md)

---

## Key Features

- **User-friendliness**: editors can edit content where it appears — the edit interface is contextual and intuitive
- **WYSIWYG editor**: includes a rich text editor
- **Responsive design**: built on [Twitter Bootstrap](http://twitter.github.com/bootstrap/)
- **Templating**: easily extend the CMS with your own look & feel
- **Add-ons**: install a variety of add-ons and customize them via an INI configuration file
- **Security**: advanced user and permissions management that scales to large organizations
- **Internationalized**: the user interface is fully translatable; Unicode is used everywhere

## Python Support

Kotti supports **Python 3.10–3.13** with PostgreSQL, MySQL, and SQLite.

[![PostgreSQL CI](https://github.com/Kotti/Kotti/workflows/PostgreSQL/badge.svg?branch=master)](https://github.com/Kotti/Kotti/actions)
[![MySQL CI](https://github.com/Kotti/Kotti/workflows/MySQL/badge.svg?branch=master)](https://github.com/Kotti/Kotti/actions)
[![SQLite CI](https://github.com/Kotti/Kotti/workflows/SQLite/badge.svg?branch=master)](https://github.com/Kotti/Kotti/actions)
