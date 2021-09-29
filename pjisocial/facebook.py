"""
facebook
~~~~~~~~

A module for automating Facebook.
"""
import multiprocessing as mp
from time import sleep

import webview                              # type: ignore

from pjisocial import httplistener as hl
from pjisocial.connect import Token


# Configuration.
SCHEME = 'https'
DOMAIN = 'www.facebook.com'
API = '/v12.0'
APP_ID_LOCATION = 'pjisocial_fb_app_id'
APP_ID_ACCOUNT = 'pjisocial'
TIMEOUT = 30


# Login functions.
def login(app_id: Token) -> None:
    """Log into Facebook."""
    # Facebook redirects the user to the redirect URI after login
    # is successful. This server receives that redirect.
    ctx = mp.get_context('fork')
    queue = ctx.Queue()
    hl.queue = queue
    kwargs = {
        'port': '5002',
    }
    P_redirect = hl.ctx.Process(target=hl.app.run, kwargs=kwargs)
    P_redirect.start()
    sleep(.01)

    # Configure call.
    try:
        anticsrf = Token('pjisocial_fb_login_anticsrf', app_id.user, temp=True)
        anticsrf.set_random(32, urlsafe=True)
        redirect_uri = f'http://127.0.0.1:{kwargs["port"]}/facebook_login'
        path = '/dialog/oauth'

        # Create the window for the manual login and give it the
        # URL for the Facebook login.
        title = 'Facebook Login'
        url = (f'{SCHEME}://{DOMAIN}{API}{path}'
               f'?client_id={app_id.get()}'
               f'&redirect_uri={redirect_uri}'
               f'&state={anticsrf.get()}')
        resp = webview.create_window(title, url)

        # Poll the local server for the data from the Facebook login
        # redirect.
        count = 0
        while count < TIMEOUT * 10:
            code = hl.queue.get()
            if code:
                break
            count += 1
            sleep(0.1)

    # Clean up.
    finally:
        P_redirect.terminate()

    return code
