"""Test package for CI/CD.

Contains only testcode.
"""

from .calc import get_sum

__version__ = "0.1.0"

session = None

ERROR_NO_SESSIONS_FOUND = "No session found"


class TPException(Exception):
    """Custom exception for test project."""


def login(username: str, password: str):
    """Test login function."""
    global session
    if username == "admin" and password == "admin1":
        session = "admin"
        return True
    return False


def logout():
    """Logout function."""
    global session
    try:
        if not session:
            raise TPException(ERROR_NO_SESSIONS_FOUND)
        session = None
    except TPException:
        print(ERROR_NO_SESSIONS_FOUND)


def is_session_active():
    """Check if session is active."""
    global session
    return session is not None


def print_username():
    """Print username."""
    global session
    if session:
        print(session)
        print(get_sum(10, 20))
    else:
        print(ERROR_NO_SESSIONS_FOUND)
