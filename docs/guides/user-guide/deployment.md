# Deployment

Kotti deployment is not different from deploying any other WSGI app.
You have a bunch of options on multiple layers: OS, RDBMS, Webserver, etc.

This document assumes the following stack:

- **OS:** Ubuntu (recent LTS)
- **Webserver:** Nginx
- **RDBMS:** PostgreSQL
- **Kotti:** latest version available on PyPI, installed with uv or virtualenv, deployed in a uWSGI application container

## Manual installation

Install OS packages:

```bash
apt-get install build-essential libpq-dev python3 python3-dev python3-venv
```

Install PostgreSQL:

```bash
apt-get install postgresql
```

Create a DB user:

```bash
sudo -u postgres createuser -P

Enter name of role to add: kotti
Enter password for new role:
Enter it again:
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

Create a DB:

```bash
sudo -u postgres createdb -O kotti kotti
```

Install Nginx:

```bash
apt-get install nginx-full
```

Create a config file in `/etc/nginx/sites-available/<your_domain>.conf`:

```nginx
server {
    listen 80;
    server_name <your_domain>;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/kotti/<your_domain>.sock;
    }
}
```

Create a user for your Kotti application:

```bash
useradd -m kotti
```

Install Kotti in a virtual environment in the new user's home directory:

```bash
sudo -u kotti python3 -m venv /home/kotti
sudo -u kotti /home/kotti/bin/pip install Kotti
```

Create an ini file in `/home/kotti/kotti.ini`:

```ini
[app:main]
use = egg:kotti
pyramid.includes = pyramid_tm
sqlalchemy.url = postgresql://kotti:<db_password>@127.0.0.1:5432/kotti
kotti.configurators = kotti_tinymce.kotti_configure
kotti.site_title = My Kotti Site
kotti.secret = changethis
filter-with = fanstatic

[filter:fanstatic]
use = egg:fanstatic#fanstatic

[alembic]
script_location = kotti:alembic

[uwsgi]
socket = /home/kotti/<your_domain>.sock
master = true
chmod-socket = 666
processes = 2
lazy = true      # needed if want processes > 1
lazy-apps = true
```

Install Supervisor:

```bash
apt-get install supervisor
```

Create a supervisor config for Kotti / uWSGI in `/etc/supervisor/conf.d/kotti.conf`:

```ini
[program:kotti]
autorestart=true
command=uwsgi_python --ini-paste /home/kotti/kotti.ini
directory=/home/kotti
redirect_stderr=true
```

Reload the supervisor config:

```bash
supervisorctl reload
```

That's all. Your Kotti deployment should now happily serve pages.

## Fabfile

!!! warning
    This is only an example. Do not run this unmodified against a host that is intended to do anything else or things WILL break!

For your convenience there is a [fabric](http://docs.fabfile.org/) file that automates all of the above.
If you don't know what fabric is and how it works, read their documentation first.

On your local machine make a separate virtualenv first and install the `fabric` and `fabtools` packages into that virtualenv:

```bash
mkvirtualenv kotti_deployment && cdvirtualenv
pip install fabric fabtools
```

Get the fabfile:

```bash
wget https://gist.github.com/gists/4079191/download
```

Read and modify the file to fit your needs. Then run it against your server:

```bash
fab install_all
```

You're done. Everything is installed and configured to serve Kotti under `http://kotti.yourdomain.com/`.
