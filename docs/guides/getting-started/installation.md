# Installation

## Requirements

- Python >= 3.10
- `build_essential` and `python-dev` (on Debian or Ubuntu), or
- `Xcode` (on macOS), or
- equivalent build toolchain for your OS.

## Installation using `uv` (recommended)

[uv](https://github.com/astral-sh/uv) is the recommended way to install Kotti in a managed environment:

```bash
uv venv mysite
cd mysite
uv pip install Kotti
```

## Installation using `virtualenv`

You can also install Kotti inside a standard virtualenv:

```bash
python3 -m venv mysite
cd mysite
bin/pip install Kotti
```

This will install the latest released version of Kotti and all its requirements into your virtualenv.

Kotti uses [Paste Deploy](http://pythonpaste.org/deploy/#the-config-file) for configuration and deployment.
An example configuration file is included with Kotti's source distribution.
Download it to your virtualenv directory (`mysite`):

```bash
wget https://raw.github.com/Kotti/Kotti/stable/app.ini
```

See the list of [Kotti tags](https://github.com/Kotti/Kotti/tags), perhaps to find the latest released version.
You can search the [Kotti listing on PyPI](https://pypi.python.org/pypi?%3Aaction=search&term=kotti&submit=search) also, for the latest Kotti release (Kotti with a capital K is Kotti itself, kotti_this and kotti_that are add-ons in the list on PyPI).

## Running Kotti

To run Kotti using the `app.ini` example configuration file:

```bash
bin/pserve app.ini
```

This command runs Waitress, Pyramid's WSGI server, which Kotti uses as a default server.
You will see console output giving the local URL to view the site in a browser.

As you learn more, install other servers, with WSGI enabled, as needed.
For instance, for Apache, you may install the optional mod_wsgi module, or for Nginx, you may use uWSGI.
See the Pyramid documentation for a variety of server and server configuration options.

The pserve command above uses SQLite as the default database.
On first run, Kotti will create a SQLite database called `Kotti.db` in your `mysite` directory.
Kotti includes support for PostgreSQL, MySQL and SQLite (tested regularly), and [other SQL databases](http://www.sqlalchemy.org/docs/core/engines.html#supported-databases).
The default use of SQLite makes initial development easy.
Although SQLite may prove to be adequate for some deployments, Kotti is flexible for installation of your choice of database during development or at deployment.
