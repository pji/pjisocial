"""
httplistener
~~~~~~~~~~~~

A webserver for interacting with social media API calls.
"""
import click                                    # type: ignore
import logging
import multiprocessing as mp
from typing import Optional

from flask import Flask, make_response, request

from pjisocial import connect as cx


# Exceptions.
class Csrf(RuntimeError):
    """The anti-CSRF token was not in the request."""


# Silence the logger since this is just to grab http redirects.
def silence(text, file=None, nl=None, err=None, color=None, **styles):
    """Dummy function to silence screen output from flask."""


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
click.echo = silence                            # type: ignore
click.secho = silence                           # type: ignore


# Multiprocessing configuration.
ctx = mp.get_context('fork')
queue = ctx.Queue()

# Create an anti-CSRF token to prevent cross-site request forgery.
anticsrf: Optional[str] = None

# Create the web application.
app = Flask(__name__)


# HTTP Responders.
@app.route('/facebook_login', methods=['GET', ])
def facebook_login() -> tuple[str, int]:
    """Get the code value from a facebook login."""
    # If the anticsrf token wasn't returned, the request probably
    # didn't come from Facebook.
    if anticsrf != request.args['state']:
        queue.put(Csrf('Token was not returned'))
        return('Forbidden', 403)

    # If the anticsrf token was returned, it was from Facebook.
    queue.put(request.args['code'])
    return('Success', 200)


@app.route('/health', methods=['GET', ])
def running() -> tuple[str, int]:
    """Return OK to prove the server is running."""
    return('OK', 200)
