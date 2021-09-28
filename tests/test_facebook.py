"""
test_facebook
~~~~~~~~~~~~~

Unit tests for the pjisocial.facebook module.
"""
import unittest as ut
from unittest.mock import patch

from pjisocial import facebook as fb


# Test cases.
class LoginTestCase(ut.TestCase):
    @patch('requests.get')
    def test_login(self, mock_get):
        """When called, send a login request to Facebook."""
        # Expected values.
        exp_url = 'https://www.facebook.com/v12.0/dialog/oauth'
        exp_q = {
            'client_id': 'spam',
            'redirect_uri': 'http://127.0.0.1:5001/facebook_login',
            'state': 'eggs',
        }

        # Run test.
        _ = fb.login()

        # Determine test result.
        last_call = mock_get.call_args
        act_url = last_call[0][0]
        act_q = last_call[0][1]
        self.assertEqual(exp_url, act_url)
        self.assertEqual(exp_q, act_q)
