"""
test_connect
~~~~~~~~~~~~

Unit tests for the pjisocial.connect module.
"""
import unittest as ut
from unittest.mock import call, patch

import keyring

from pjisocial import connect as cx


# Test classes.
class TokenTestCase(ut.TestCase):
    def setUp(self):
        """Create common test data and state."""
        # Create the test secret.
        self.service = '_pjisocial_test_service'
        self.user = '_pjisocial'
        self.value = '_pjisocial_secret'
        keyring.set_password(self.service, self.user, self.value)

        # Ensure the non-existing secret doesn't exist.
        self.not_service = '_pjisocial_not_service'
        if keyring.get_password(self.not_service, self.user):
            raise RunTimeError(f'Abort. {self.not_service} exists.')

    def test_initialize(self):
        """Given a service and a username, the Token class should
        return an instance with those attributes set.
        """
        # Expected values.
        exp = {
            'service': self.service,
            'user': self.user,
        }

        # Run test.
        token = cx.Token(**exp)

        # Extract test result.
        act = {
            'service': token.service,
            'user': token.user,
        }

        # Determine if test passed.
        self.assertDictEqual(exp, act)

    def test_clear(self):
        """When called on a temporary token, the token should be
        removed from the OS's secret store.
        """
        # Expected value.
        exp_before = '_remove'
        exp_after = None

        # Test data and state.
        service = '__TokenTestCase_test_remove'
        user = self.user
        temp = True
        if keyring.get_password(service, user):
            raise RuntimeError('Secret already existed.')
        token = cx.Token(service, user, temp)
        token.set(exp_before)
        act_before = keyring.get_password(service, user)

        # Run test.
        token.clear()

        # Determine test result.
        act_after = keyring.get_password(service, user)
        self.assertEqual(exp_before, act_before)
        self.assertEqual(exp_after, act_after)

    def test_do_not_clear_permanent_secrets(self):
        """When called on a permanent token, raise a PermanentSecret
        error.
        """
        # Expected value.
        exp_ex = cx.PermanentSecret
        exp_msg = 'Cannot clear a permanent secret.'
        exp_value = self.value

        # Test data and state.
        token = cx.Token(self.service, self.user, temp=False)

        # Run test and determine result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            token.clear()
        act_value = keyring.get_password(self.service, self.user)
        self.assertEqual(exp_value, act_value)

    def test_get(self):
        """When called, the get() method should return the value of the
        secret as a string.
        """
        # Expected values.
        exp = self.value

        # Create specific test data and state.
        token = cx.Token(self.service, self.user)

        # Run test.
        act = token.get()

        # Determine if test passed.
        self.assertEqual(exp, act)

    def test_get_secret_does_not_exist(self):
        """If the secret doesn't exist in the OS's secret store, get()
        should raise a connect.SecretDoesNotExist exception.
        """
        # Expected value.
        exp = cx.SecretDoesNotExist
        exp_msg = 'Expected secret not in OS secret store.'

        # Set up specific test data and state.
        token = cx.Token(self.not_service, self.user)

        # Determine if test passed when block completes.
        with self.assertRaisesRegex(exp, exp_msg):

            # Run test.
            _ = token.get()

    @patch('secrets.token_bytes')
    def test_set_random(self, mock_secrets):
        """Given a token length in bytes, set the secret as a
        cryptographically bytes of the given length.
        """
        # Expected value.
        exp_call = call(32)
        exp_token = b'spam'

        # Test data and state.
        mock_secrets.return_value = exp_token
        service = '__TokenTestCase_test_set_random'
        user = self.user
        temp = True
        if keyring.get_password(service, user):
            raise RuntimeError('Secret already existed.')
        token = cx.Token(service, user, temp)
        length = 32

        # Run test.
        try:
            token.set_random(length)

            # Determine test result.
            act_call = mock_secrets.call_args
            raw_token = keyring.get_password(service, user)
            act_token = bytes(raw_token, encoding='utf_8')
            self.assertEqual(exp_call, act_call)
            self.assertEqual(exp_token, act_token)

        # Clean up.
        finally:
            keyring.delete_password(service, user)

    @patch('secrets.token_urlsafe')
    def test_set_random_urlsafe(self, mock_secrets):
        """If the urlsafe parameter is true, generate a URL safe
        cryptographically random token.
        """
        # Expected value.
        exp_call = call(32)
        exp_token = 'spam'

        # Test data and state.
        mock_secrets.return_value = exp_token
        service = '__TokenTestCase_test_set_random_urlsafe'
        user = self.user
        temp = True
        if keyring.get_password(service, user):
            raise RuntimeError('Secret already existed.')
        token = cx.Token(service, user, temp)
        length = 32
        urlsafe = True

        # Run test.
        try:
            token.set_random(length, urlsafe)

            # Determine test result.
            act_call = mock_secrets.call_args
            act_token = keyring.get_password(service, user)
            self.assertEqual(exp_call, act_call)
            self.assertEqual(exp_token, act_token)

        # Clean up.
        finally:
            keyring.delete_password(service, user)

    def test_set(self):
        """When given a value, the value should be stored as a secret."""
        # Expected value.
        exp = 'spam'

        # Test data and state.
        service = '__TokenTestCase_test_make'
        user = self.user
        token = cx.Token(service, user, temp=True)

        # Run test.
        token.set(exp)

        # Determine test result.
        try:
            act = keyring.get_password(service, user)
            self.assertEqual(exp, act)

        # Clean up if exception.
        finally:
            keyring.delete_password(service, user)

    def test_do_not_set_if_token_not_temporary(self):
        """If the secret isn't temporary, raise a PermanentSecret
        exception."""
        # Expected values.
        exp_ex = cx.PermanentSecret
        exp_msg = 'Cannot create a permanent secret.'
        exp_value = self.value

        # Test data and state.
        value = 'spam'
        token = cx.Token(self.service, self.user, temp=False)

        # Run test and determine result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            token.set(value)
        act_value = keyring.get_password(self.service, self.user)
        self.assertEqual(exp_value, act_value)

    def test_repr(self):
        """When needed, Token objects should return a representation of
        themselves useful for debugging.
        """
        # Expected value.
        exp = f"Token('{self.service}', '{self.user}')"

        # Set up specific test data and state.
        token = cx.Token(self.service, self.user)

        # Run test.
        act = repr(token)

        # Determine is test passed.
        self.assertEqual(exp, act)

    def tearDown(self):
        keyring.delete_password(self.service, self.user)
