"""
test_httplistener
~~~~~~~~~~~~~

Unit tests for the pjisocial.httplistener module.
"""
import multiprocessing as mp
from time import sleep
import unittest as ut
from unittest.mock import patch

from requests import get

from pjisocial import httplistener as hl


# Configuration.
mp.set_start_method('fork')


# Test cases.
class HttpListenerTestCase(ut.TestCase):
    def setUp(self):
        self.protocol = 'http'
        self.fqdn = '127.0.0.1'
        self.port = '5001'

        # Start the flask server for testing.
        kwargs = {
            'port': self.port,
        }
        self.P = hl.ctx.Process(target=hl.app.run, kwargs=kwargs)
        self.P.start()

        # Give the server time to stand up.
        sleep(.01)

    def tearDown(self):
        if self.P.is_alive():
            self.P.terminate()
        sleep(.05)
        if self.P.is_alive():
            self.P.kill()

    def test_health(self):
        """When /health is called, the server should return OK."""
        # Expected values.
        exp_code = 200
        exp_body = 'OK'

        # Test data and state.
        path = '/health'
        url = f'{self.protocol}://{self.fqdn}:{self.port}{path}'

        # Run test.
        resp = get(url)

        # Determine test result.
        act_code = resp.status_code
        act_body = resp.text
        self.assertEqual(exp_code, act_code)
        self.assertEqual(exp_body, act_body)

    @patch('secrets.token_urlsafe')
    def test_facebook_login(self, mock_secrets):
        """When /facebook_login is called with the code parameter,
        the server should return the value of code to the application
        that started the server.
        """
        # Expected value.
        exp = 'spam'

        # Test data and state.
        mock_secrets.return_value = 'eggs'
        path = '/facebook_login'
        url = f'{self.protocol}://{self.fqdn}:{self.port}{path}'
        query = {
            'code': exp,
            'state': 'eggs'
        }

        # Run test.
        _ = get(url, query)
        act = hl.queue.get()

        # Determine test results.
        self.assertEqual(exp, act)
