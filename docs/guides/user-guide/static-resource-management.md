# Static Resource Management

In the default settings Kotti uses
[Fanstatic](http://www.fanstatic.org/) to manage its static resources
(i.e. CSS, JS, etc.). This is accomplished by a WSGI pipeline:

```ini
[app:kotti]
use = egg:kotti

[filter:fanstatic]
use = egg:fanstatic#fanstatic

[pipeline:main]
pipeline =
    fanstatic
    kotti

[server:main]
use = egg:waitress#main
host = 127.0.0.1
port = 5000
```

## Defining Resources in Third-Party Add-ons

Defining your own resources and having them rendered in the pages produced
by Kotti is also easy. You just need to define resource objects ([as
described in the corresponding Fanstatic
documentation](https://fanstatic.readthedocs.io/en/latest/library.html))
and add them to either `edit_needed` or `view_needed` in
[kotti.fanstatic](../../api/kotti.fanstatic.md):

```python
from fanstatic import Library
from fanstatic import Resource
from kotti.fanstatic import edit_needed
from kotti.fanstatic import view_needed

my_library = Library('my_package', 'resources')
my_resource = Resource(my_library, "my.js")

def includeme(config):
    # add to edit_needed if the resource is needed in edit views
    edit_needed.add(my_resource)
    # add to view_needed if the resource is needed in view views
    view_needed.add(my_resource)
```

Don't forget to add an `entry_point` to your package's `setup.py` (or `pyproject.toml`):

```python
entry_points={
    'fanstatic.libraries': [
        'foo = my_package:my_library',
        ],
    },
```

Fanstatic has many more useful options, such as being able to define
additional minified resources for deployment. Please consult
[Fanstatic's documentation](https://fanstatic.readthedocs.io/) for a
complete list of options.

## Overriding Kotti's Default Definitions

You can override the resources to be included in the configuration file.

The defaults are:

```ini
[app:kotti]

kotti.fanstatic.edit_needed = kotti.fanstatic.edit_needed
kotti.fanstatic.view_needed = kotti.fanstatic.view_needed
```

which is actually a shortcut for:

```ini
[app:kotti]

kotti.fanstatic.edit_needed =
    kotti.fanstatic.edit_needed_js
    kotti.fanstatic.edit_needed_css

kotti.fanstatic.view_needed =
    kotti.fanstatic.view_needed_js
    kotti.fanstatic.view_needed_css
```

You may add as many `kotti.fanstatic.NeededGroup`, `fanstatic.Group` or
`fanstatic.Resource` (or actually anything that provides a `.need()`
method) objects in dotted notation as you want.

Say you want to completely abandon Kotti's CSS resources (and use your
own for both view and edit views) but use Kotti's JS resources plus an
additional JS resource defined within your app (only in edit views).
Your configuration file might look like this:

```ini
[app:kotti]

kotti.fanstatic.edit_needed =
    kotti.fanstatic.edit_needed_js
    myapp.fanstatic.js_resource
    myapp.fanstatic.css_resource

kotti.fanstatic.view_needed =
    kotti.fanstatic.view_needed_js
    myapp.fanstatic.css_resource
```

## Using Kotti Without Fanstatic

To handle resources yourself, you can easily and completely turn off
fanstatic:

```ini
[app:main]
use = egg:kotti

[server:main]
use = egg:waitress#main
host = 127.0.0.1
port = 5000
```
