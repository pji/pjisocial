"""
connect
~~~~~~~

Basic HTTP connectivity for the pjisocial module.
"""
from keyring import get_password


# Exceptions.
class SecretDoesNotExist(RuntimeError):
    """The OS's secret store doesn't contain the requested secret."""


# Public classes.
class Token:
    """A secret stored in the OS's native secret store."""
    def __init__(self, service: str, user: str) -> None:
        self.service = service
        self.user = user
    
    def __repr__(self):
        return f"Token('{self.service}', '{self.user}')"

    # Public methods.
    def get(self) -> str:
        """Return the value of the secret."""
        secret = get_password(self.service, self.user)
        if not secret:
            msg = 'Expected secret not in OS secret store.'
            raise SecretDoesNotExist(msg)
        return secret