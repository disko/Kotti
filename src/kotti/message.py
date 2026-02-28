import hashlib
import time
from urllib.parse import urlencode

from html2text import HTML2Text
from pyramid.renderers import render
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message

from kotti import get_settings
from kotti.request import Request
from kotti.security import Principal

_inject_mailer = []


def get_mailer():
    # Consider that we may have persistent settings
    if _inject_mailer:
        return _inject_mailer[0]
    return Mailer.from_settings(get_settings())  # pragma: no cover


def make_token(user: Principal, seconds: float | None = None) -> str:
    secret = get_settings()["kotti.secret2"]
    if seconds is None:
        seconds = time.time()
    token = f"{user.name}:{secret}:{seconds}"
    return "{}:{}".format(hashlib.sha224(token.encode("utf8")).hexdigest(), seconds)


def validate_token(user: Principal, token: str, valid_hrs: int = 24) -> bool:
    """
    >>> from kotti.testing import setUp, tearDown
    >>> ignore = setUp()
    >>> class User(object):
    ...     pass
    >>> daniel = User()
    >>> daniel.name = u'daniel'
    >>> alice = User()
    >>> alice.name = u'alice'
    >>> token = make_token(daniel)
    >>> validate_token(daniel, token)
    True
    >>> validate_token(alice, token)
    False
    >>> validate_token(daniel, 'foo')
    False
    >>> token = make_token(daniel, seconds=time.time() - 100000)
    >>> validate_token(daniel, token)
    False
    >>> validate_token(daniel, token, valid_hrs=48)
    True
    >>> tearDown()
    """
    try:
        seconds = float(token.split(":")[1])
    except (IndexError, ValueError):
        return False
    valid_duration = 60 * 60 * valid_hrs
    token_valid = token == make_token(user, seconds)
    not_expired = time.time() - seconds < valid_duration
    return bool(token_valid and not_expired)


def send_email(
    request: Request,
    recipients: list[str],
    template_name: str,
    template_vars: dict[str, str] | None = None,
) -> None:
    """General email sender.

    :param kotti.request.Request request: current request.
    :param list recipients: list of email addresses. Each email should be a
        string like: ``'"John Doe" <joedoe@foo.com>'``.
    :param str template_name: asset specification (e.g.
        ``'mypackage:templates/email.pt'``).
    :param dict template_vars: set of variables present on template.
    """

    if template_vars is None:
        template_vars = {}

    text = render(template_name, template_vars, request)
    subject, htmlbody = text.strip().split("\n", 1)
    subject = subject.replace("Subject:", "", 1).strip()
    html2text = HTML2Text()
    html2text.body_width = 0
    textbody = html2text.handle(htmlbody).strip()

    message = Message(
        recipients=recipients, subject=subject, body=textbody, html=htmlbody
    )
    mailer = get_mailer()
    mailer.send(message)


def email_set_password(
    user: Principal,
    request: Request,
    template_name: str | None = "kotti:templates/email-set-password.pt",
    add_query: dict[str, str] | None = None,
) -> None:
    site_title = get_settings()["kotti.site_title"]
    token = make_token(user)
    user.confirm_token = token
    set_password_query = {"token": token, "email": user.email}
    if add_query:
        set_password_query.update(add_query)
    url = f"{request.application_url}/@@set-password?{urlencode(set_password_query)}"
    variables = dict(user_title=user.title, site_title=site_title, url=url)
    recipients = [f'"{user.title}" <{user.email}>']  # XXX naive?
    send_email(request, recipients, template_name, variables)
