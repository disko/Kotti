# Events

Kotti has a builtin event system that is based on the [Publish-subscribe
pattern](http://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern).

The basic concept is that whenever a specific event occurs, all handler
functions that have subscribed to that event will be executed.

There are two different types of events:

- **Object events** relate to a specific object. In most cases this object will be a
  node from the content tree (i.e. the same as `context` in view callables).

  Events of type [`ObjectEvent`](../../api/kotti.events.md) have `object` and
  `request` attributes. `event.request` may be `None` when no request is available.

- **Generic events** don't have that kind of context.

  Kotti supports such events but doesn't use them anywhere.

The event types provided by Kotti (see [kotti.events API](../../api/kotti.events.md)) may be extended with your
own event types. Subclass [`ObjectEvent`](../../api/kotti.events.md) (for object events) or `object` (for
generic events) and follow the subscription instructions below, as you would
for Kotti-provided events.

## Subscribing to Events

To add a handler for a specific event type, you must implement a
function which takes a single argument `event` and associate that to the
appropriate event type by decorating it with the
[`subscribe`](../../api/kotti.events.md) decorator.

That decorator takes up to two arguments that restrict the handler
execution to specific events only. When called without arguments the
handler is subscribed to *all* events:

```python
from kotti.events import subscribe

@subscribe()
def all_events_handler(event):
    print(event)
```

To subscribe to a specific event type, supply the desired type as the
first argument to [`subscribe`](../../api/kotti.events.md):

```python
from kotti.events import ObjectInsert
from kotti.events import subscribe

@subscribe(ObjectInsert)
def document_insert_handler(event):
    print(event.object, event.request)
```

You can further narrow the subscription by adding a second argument that
limits the subscription to specific object types. For example, to
subscribe to [`ObjectDelete`](../../api/kotti.events.md) events of
[`Document`](../../api/kotti.resources.md) types, write:

```python
from kotti.events import ObjectDelete
from kotti.events import subscribe
from kotti.resources import Document

@subscribe(ObjectDelete, Document)
def document_delete_handler(event):
    print(event.object, event.request)
```

## Triggering Event Handler Execution

Notifying listeners of an event is as simple as calling
[`notify`](../../api/kotti.events.md):

```python
from kotti.events import notify
notify(MyFunnyEvent())
```

Listeners are generally called in the order in which they are
registered.
