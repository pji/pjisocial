"""
httplistener
~~~~~~~~~~~~

A webserver for interacting with social media API calls.
"""
import multiprocessing as mp

from flask import Flask, make_response, request


# Multiprocessing configuration.
ctx = mp.get_context('fork')
queue = ctx.Queue()


# Create the web application.
app = Flask(__name__)


# HTTP Responders.
@app.route('/facebook_login', methods=['GET', ])
def facebook_login() -> tuple[str, int]:
    """Get the code value from a facebook login."""
    queue.put(request.args['code'])
    return('Success', 200)


@app.route('/health', methods=['GET', ])
def running() -> tuple[str, int]:
    """Return OK to prove the server is running."""
    return('OK', 200)
