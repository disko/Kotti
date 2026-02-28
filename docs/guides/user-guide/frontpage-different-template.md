# Use a Different Template for the Front Page

This recipe describes a way to override the template used for a specific
object in your database. Imagine you want your front page to stand out
from the rest of your site and use a unique layout.

We can set the *default view* for any content object by setting its
`default_view` attribute, which is usually `None`. Inside our own
populator (see [Configuration](configuration.md)), we write this:

```python
from kotti.resources import get_root

def populate():
    site = get_root()
    site.default_view = 'front-page'
```

What's left is to register the `front-page` view:

```python
def includeme(config):
    config.add_view(
        name='front-page',
        renderer='myapp:templates/front-page.pt',
    )
```

!!! note
    If you want to override instead the template of *all pages*, not
    only that of a particular page, you should look at the
    `kotti.override_assets` setting (see [Configuration](configuration.md)).
