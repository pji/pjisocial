"""
test_connect
~~~~~~~~~~~~

Unit tests for the pjisocial.connect module.
"""
import unittest as ut
from unittest.mock import patch

import keyring

from pjisocial import connect as cx


# Test classes.
class TokenTestCase(ut.TestCase):
    def setUp(self):
        """Create common test data and state."""
        self.service = '_pjisocial_test_service'
        self.user = '_pjisocial'
        self.value = '_pjisocial_secret'
        keyring.set_password(self.service, self.user, self.value)

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
        obj = cx.Token(**exp)

        # Extract test result.
        act = {
            'service': obj.service,
            'user': obj.user,
        }

        # Determine if test passed.
        self.assertDictEqual(exp, act)

    def tearDown(self):
        keyring.delete_password(self.service, self.user)
