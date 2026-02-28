# Overview

Kotti is most useful when you are developing CMS-like applications that

- have complex security requirements,
- use workflows, and/or
- work with hierarchical data.

Built on top of a number of *best-of-breed* software components, most
notably [Pyramid](http://docs.pylonsproject.org/projects/pyramid/dev/)
and [SQLAlchemy](http://www.sqlalchemy.org/), Kotti introduces only a
few concepts of its own, thus hopefully keeping the learning curve flat
for the developer.

## Features

The Kotti CMS is a content management system that's heavily inspired by
[Plone](http://plone.org/). Its **main features** are:

- **User-friendliness**: editors can edit content where it appears; thus
  the edit interface is contextual and intuitive
- **WYSIWYG editor**: includes a rich text editor
- **Responsive design**: Kotti builds on [Twitter
  Bootstrap](http://twitter.github.com/bootstrap/), which looks good
  both on desktop and mobile
- **Templating**: easily extend the CMS with your own look & feel with
  little programming required (see [Static Resource Management](../user-guide/static-resource-management.md))
- **Add-ons**: install a variety of add-ons and customize them as well
  as many aspects of the built-in CMS by use of an INI configuration
  file (see [Configuration](../user-guide/configuration.md))
- **Security**: the advanced user and permissions management is
  intuitive and scales to fit the requirements of large organizations
- **Internationalized**: the user interface is fully translatable,
  Unicode is used everywhere to store data (see [Translations](../user-guide/translations.md))

## For developers

For developers, Kotti delivers a strong foundation for building
different types of web applications that either extend or replace the
built-in CMS.

Developers can add and modify through a well-defined API:

- views,
- templates and layout (both via
  [Pyramid](http://docs.pylonsproject.org/projects/pyramid/dev/)),
- [content types](../user-guide/developer-manual.md#content-types),
- "portlets" (see [`kotti.views.slots`](../../api/kotti.views/kotti.views.slots.md)),
- access control and the user database (see [Security](../user-guide/security.md)),
- workflows (via [repoze.workflow](http://docs.repoze.org/workflow/)),
- and much more.

Kotti has a **down-to-earth** API. Developers working with Kotti will
most of the time make direct use of the
[Pyramid](http://docs.pylonsproject.org/projects/pyramid/dev/) and
[SQLAlchemy](http://www.sqlalchemy.org/) libraries. Other notable
components used but not enforced by Kotti are
[Colander](http://docs.pylonsproject.org/projects/colander/en/latest/)
and [Deform](http://docs.pylonsproject.org/projects/deform/en/latest/)
for forms, and [Chameleon](https://chameleon.readthedocs.io/) for
templating.

Kotti itself is [developed on GitHub](https://github.com/Kotti/Kotti).
You can check out Kotti's source code via its GitHub repository. Use
this command:

```bash
git clone git@github.com:Kotti/Kotti
```

[Continuous testing](https://github.com/Kotti/Kotti/actions) against
different versions of Python and with *PostgreSQL*, *MySQL* and *SQLite*
and a complete test coverage make Kotti a **stable** platform to work
with.

[![PostgreSQL CI](https://github.com/Kotti/Kotti/workflows/PostgreSQL/badge.svg?branch=stable)](https://github.com/Kotti/Kotti/actions?query=workflow%3APostgreSQL+branch%3Astable)
[![MySQL CI](https://github.com/Kotti/Kotti/workflows/MySQL/badge.svg?branch=stable)](https://github.com/Kotti/Kotti/actions?query=workflow%3AMySQL+branch%3Astable)
[![SQLite CI](https://github.com/Kotti/Kotti/workflows/SQLite/badge.svg?branch=stable)](https://github.com/Kotti/Kotti/actions?query=workflow%3ASQLite+branch%3Astable)

## Support

- Python 3.10–3.13
- Support for PostgreSQL, MySQL and SQLite (tested regularly), and a
  list of [other SQL databases](http://www.sqlalchemy.org/docs/core/engines.html#supported-databases)
- Support for WSGI and a [variety of web servers](http://wsgi.org/wsgi/Servers), including Apache
