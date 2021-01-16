"""
test_connect
~~~~~~~~~~~~

Unit tests for the pjisocial.connect module.
"""
import unittest as ut

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
