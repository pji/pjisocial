"""
connect
~~~~~~~

Basic HTTP connectivity for the pjisocial module.
"""
# Public classes.
class Token:
    """A secret stored in the OS's native secret store."""
    def __init__(self, service: str, user: str) -> None:
        self.service = service
        self.user = user
