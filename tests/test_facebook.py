"""
test_facebook
~~~~~~~~~~~~~

Unit tests for the pjisocial.facebook module.
"""
import unittest as ut
from unittest.mock import patch

import requests
import keyring

from pjisocial import connect as c
from pjisocial import facebook as fb


# Side effect functions for patches.
def get_facebook_redirect(*args, **kwargs):
    """Call the redirect URI for Facebook with the proper code."""
    url = 'http://127.0.0.1:5002/facebook_login'
    q = {
        'code': '_facebook_login_response'
    }
    requests.get(url, q)


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
    @patch('webview.create_window')
    def test_login(self, mock_get, mock_secrets):
        """When given an app ID token, send a login request to
        Facebook.
        """
        # Expected values.
        exp_title = 'Facebook Login'
        exp_url = ('https://www.facebook.com/v12.0/dialog/oauth?'
                   f'client_id={self.app_id}&'
                   f'redirect_uri=http://127.0.0.1:5002/facebook_login&'
                   f'state=eggs')
        exp_return = '_facebook_login_response'

        # Test data and state.
        mock_secrets.return_value = 'eggs'
        mock_get.side_effect = get_facebook_redirect
        token = c.Token(self.app_id_loc, self.app_id_account)

        # Run test.
        act_return = fb.login(token)

        # Determine test result.
        last_call = mock_get.call_args
        act_title = last_call[0][0]
        act_url = last_call[0][1]
        self.assertEqual(exp_return, act_return)
        self.assertEqual(exp_title, act_title)
        self.assertEqual(exp_url, act_url)
