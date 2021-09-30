"""
facebook
~~~~~~~~

A module for automating Facebook.
"""
from json import loads
import multiprocessing as mp
from time import sleep
from typing import Any
import webbrowser

from requests import get                                # type: ignore

from pjisocial import httplistener as hl
from pjisocial.connect import Token


# Configuration.
SCHEME = 'https'
DOMAIN = 'graph.facebook.com'
FB_DOMAIN = 'www.facebook.com'
API = '/v12.0'
APP_ID_LOCATION = 'pjisocial_fb_app_id'
APP_ID_ACCOUNT = 'pjisocial'
APP_SECRET_LOCATION = 'pjisocial_fb_app_secret'
APP_SECRET_ACCOUNT = 'pjisocial'
TIMEOUT = 30


# Login functions.
def login(app_id: Token) -> str:
    """Log into Facebook.

    Information on Facebook access tokens:

        https://developers.facebook.com/docs/facebook-login/access-tokens
    """
    # Create the anti-CSRF token.
    anticsrf = Token('pjisocial_fb_login_anticsrf', app_id.user, temp=True)
    anticsrf.set_random(32, urlsafe=True)
    hl.anticsrf = anticsrf.get()

    # Facebook redirects the user to the redirect URI after login
    # is successful. This server receives that redirect.
    ctx = mp.get_context('fork')
    queue = ctx.Queue()
    hl.queue = queue
    kwargs = {
        'port': '5002',
        'ssl_context': 'adhoc',
    }
    P_redirect = hl.ctx.Process(target=hl.app.run, kwargs=kwargs)
    P_redirect.start()
    sleep(.01)

    # Configure call.
    try:
        # Configure the manual auth flow.
        redirect_uri = f'https://127.0.0.1:{kwargs["port"]}/facebook_login'

        # Call the manual auth flow.
        get_dialog_oauth(app_id, redirect_uri, anticsrf)

        # Poll the local server for the data from the Facebook login
        # redirect.
        count = 0
        while count < TIMEOUT * 10:
            code = hl.queue.get()
            if code:
                break
            count += 1
            sleep(0.1)

        # Ensure the anticsrf token was passed.
        if isinstance(code, hl.Csrf):
            raise code

    # Clean up.
    finally:
        P_redirect.terminate()

    return code


# Facebook interactive calls.
def get_dialog_oauth(app_id: Token,
                     redirect_uri: str,
                     state: Token) -> None:
    """Starts the manual authentication flow."""
    # Configure call.
    path = '/dialog/oauth'

    # Make call.
    url = (f'{SCHEME}://{FB_DOMAIN}{API}{path}'
           f'?client_id={app_id.get()}'
           f'&redirect_uri={redirect_uri}'
           f'&state={state.get()}')
    webbrowser.open(url)


# Oauth API calls.
def get_access_token(app_id: Token,
                     redirect_uri: str,
                     app_secret: Token,
                     code: str) -> dict[str, Any]:
    """Get an access token for a code."""
    # Configure call.
    path = '/oauth/access_token'
    q = {
        'client_id': app_id.get(),
        'redirect_uri': redirect_uri,
        'client_secret': app_secret.get(),
        'code': code,
    }

    # Make the call.
    url = f'{SCHEME}://{DOMAIN}{API}{path}'
    resp = get(url, q)

    # Translate the response.
    return loads(resp.text)


if __name__ == '__main__':
    app_id = Token(APP_ID_LOCATION, APP_ID_ACCOUNT)
    code = login(app_id)
    print(code)
