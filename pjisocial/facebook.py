"""
facebook
~~~~~~~~

A module for automating Facebook.
"""
import requests                                 # type: ignore


# Configuration.
SCHEME = 'https'
DOMAIN = 'www.facebook.com'
API = '/v12.0'
APP_ID = 'spam'


# Login functions.
def login() -> None:
    """Log into Facebook."""
    # Configure API call.
    path = '/dialog/oauth'
    q = {
        'client_id': APP_ID,
        'redirect_uri': 'http://127.0.0.1:5001/facebook_login',
        'state': 'eggs',
    }

    # Make API call.
    url = f'{SCHEME}://{DOMAIN}{API}{path}'
    resp = requests.get(url, q)

