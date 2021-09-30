"""
test_facebook
~~~~~~~~~~~~~

Unit tests for the pjisocial.facebook module.
"""
import json
import unittest as ut
from unittest.mock import call, MagicMock, patch

import requests
import keyring

from pjisocial import connect as cx
from pjisocial import facebook as fb


# Side effect functions for patches.
def get_facebook_redirect(*args, **kwargs):
    """Call the redirect URI for Facebook with the proper code."""
    url = 'https://127.0.0.1:5002/facebook_login'
    q = {
        'code': '_facebook_login_response',
        'state': 'eggs',
    }
    requests.get(url, q, verify=False)


# Test cases.
class LoginTestCase(ut.TestCase):
    def setUp(self):
        self.app_id_loc = '__test_facebook_LoginTestCase_app_id'
        self.app_id_account = 'pjisocial'
        self.app_id = 'spam'
        self.app_id_loc_buffer = fb.APP_ID_LOCATION
        self.app_id_account_buffer = fb.APP_ID_ACCOUNT
        fb.APP_ID_LOCATION = self.app_id_loc
        fb.APP_ID_ACCOUNT = self.app_id_account

        # Build test token values.
        keyring.set_password(
            self.app_id_loc,
            self.app_id_account,
            self.app_id
        )

    def tearDown(self):
        fb.APP_ID_LOCATION = self.app_id_loc_buffer
        fb.APP_ID_ACCOUNT = self.app_id_account_buffer
        keyring.delete_password(self.app_id_loc, self.app_id_account)

    @patch('secrets.token_urlsafe')
    @patch('webbrowser.open')
    def test_login(self, mock_get, mock_secrets):
        """When given an app ID token, send a login request to
        Facebook.
        """
        # Expected values.
        exp_url = ('https://www.facebook.com/v12.0/dialog/oauth?'
                   f'client_id={self.app_id}&'
                   f'redirect_uri=https://127.0.0.1:5002/facebook_login&'
                   f'state=eggs')
        exp_return = '_facebook_login_response'

        # Test data and state.
        mock_secrets.return_value = 'eggs'
        mock_get.side_effect = get_facebook_redirect
        token = cx.Token(self.app_id_loc, self.app_id_account)

        # Run test.
        act_return = fb.login(token)

        # Determine test result.
        last_call = mock_get.call_args
        act_url = last_call[0][0]
        self.assertEqual(exp_return, act_return)
        self.assertEqual(exp_url, act_url)


class OauthTestCase(ut.TestCase):
    def setUp(self):
        self.app_id_loc = '__test_facebook_OauthTestCase_app_id'
        self.app_id_account = 'pjisocial'
        self.app_id = 'spam'
        self.app_id_loc_buffer = fb.APP_ID_LOCATION
        self.app_id_account_buffer = fb.APP_ID_ACCOUNT
        fb.APP_ID_LOCATION = self.app_id_loc
        fb.APP_ID_ACCOUNT = self.app_id_account

        self.app_secret_loc = '__test_facebook_OauthTestCase_app_secret'
        self.app_secret_account = 'pjisocial'
        self.app_secret = 'tomato'
        self.app_secret_loc_buffer = fb.APP_SECRET_LOCATION
        self.app_secret_account_buffer = fb.APP_SECRET_ACCOUNT
        fb.APP_SECRET_LOCATION = self.app_secret_loc
        fb.APP_SECRET_ACCOUNT = self.app_secret_account

        # Build test token values.
        keyring.set_password(
            self.app_id_loc,
            self.app_id_account,
            self.app_id
        )
        keyring.set_password(
            self.app_secret_loc,
            self.app_secret_account,
            self.app_secret
        )

    def tearDown(self):
        fb.APP_ID_LOCATION = self.app_id_loc_buffer
        fb.APP_ID_ACCOUNT = self.app_id_account_buffer
        fb.APP_SECRET_LOCATION = self.app_secret_loc_buffer
        fb.APP_SECRET_ACCOUNT = self.app_secret_account_buffer
        keyring.delete_password(self.app_id_loc, self.app_id_account)
        keyring.delete_password(self.app_secret_loc, self.app_secret_account)

    @patch('pjisocial.facebook.get')
    def test_get_access_token(self, mock_get):
        """Given the app ID, the original login URI, the app secret,
        and the login code, call the oauth/access_token endpoint and
        return the response from Facebook.
        """
        # Expected values.
        exp_call = call(
            'https://graph.facebook.com/v12.0/oauth/access_token',
            {
                'client_id': self.app_id,
                'redirect_uri': 'https://127.0.0.1:5002/facebook_login',
                'client_secret': self.app_secret,
                'code': 'eggs',
            },
        )
        exp_resp = {
            'access_token': 'bacon',
            'token_type': 'sausages',
            'expires_in': 1000,
        }

        # Test data and state.
        resp = MagicMock()
        resp.text = json.dumps(exp_resp)
        mock_get.return_value = resp
        app_id = cx.Token(self.app_id_loc, self.app_id_account)
        redirect_uri = 'https://127.0.0.1:5002/facebook_login'
        app_secret = cx.Token(self.app_secret_loc, self.app_secret_account)
        code = 'eggs'

        # Run test.
        act_resp = fb.get_access_token(app_id, redirect_uri, app_secret, code)

        # Determine test result.
        act_call = mock_get.call_args
        self.assertEqual(exp_call, act_call)
        self.assertEqual(exp_resp, act_resp)
