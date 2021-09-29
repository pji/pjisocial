"""
connect
~~~~~~~

Basic HTTP connectivity for the pjisocial module.
"""
import secrets

from keyring import delete_password, get_password, set_password


# Exceptions.
class PermanentSecret(RuntimeError):
    """Tokens that change must be created as temporary."""


class SecretDoesNotExist(RuntimeError):
    """The OS's secret store doesn't contain the requested secret."""


class SecretExists(RuntimeError):
    """The OS's secret store already contains that secret."""


# Public classes.
class Token:
    """A secret stored in the OS's native secret store.

    :param service: The name the secret is stored under.
    :param user: The user tied to the secret.
    :param temp: (Optional.) Whether the token value changes while the
        application is running. This can be used to prevent accidentally
        changing the values of long lived secrets like API keys and
        passwords, but allow changing of short lived secrets like
        session tokens. The default is false.
    """
    def __init__(self, service: str, user: str, temp: bool = False) -> None:
        self.service = service
        self.user = user
        self.temp = temp

    def __repr__(self) -> str:
        return f"Token('{self.service}', '{self.user}')"

    # Public methods.
    def clear(self) -> None:
        """Remove the secret from the store."""
        # This allows the temp parameter to serve as a soft control
        # to prevent accidentally deleting tokens that should live
        # beyond this run. It does nothing to prevent malicious use.
        if not self.temp:
            raise PermanentSecret('Cannot clear a permanent secret.')

        delete_password(self.service, self.user)

    def get(self) -> str:
        """Return the value of the secret."""
        secret = get_password(self.service, self.user)
        if not secret:
            msg = 'Expected secret not in OS secret store.'
            raise SecretDoesNotExist(msg)
        return secret

    def set(self, value: str) -> None:
        """Store a secret."""
        # This allows the temp parameter to serve as a soft control
        # to prevent accidentally deleting tokens that should live
        # beyond this run. It does nothing to prevent malicious use.
        if not self.temp:
            msg = 'Cannot create a permanent secret.'
            raise PermanentSecret(msg)

        set_password(self.service, self.user, value)

    def set_random(self, length: int, urlsafe: bool = False) -> None:
        if not urlsafe:
            raw = secrets.token_bytes(length)
            value = str(raw, encoding='utf_8')
        else:
            value = secrets.token_urlsafe(length)
        set_password(self.service, self.user, value)
