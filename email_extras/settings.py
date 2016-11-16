import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


GNUPG_HOME = getattr(settings, "EMAIL_EXTRAS_GNUPG_HOME", None)
USE_GNUPG = getattr(settings, "EMAIL_EXTRAS_USE_GNUPG", GNUPG_HOME is not None)
ALWAYS_TRUST = getattr(settings, "EMAIL_EXTRAS_ALWAYS_TRUST_KEYS", False)
GNUPG_ENCODING = getattr(settings, "EMAIL_EXTRAS_GNUPG_ENCODING", None)
TEST_GNUPG_HOME = getattr(
    settings, "EMAIL_EXTRAS_TEST_GNUPG_HOME",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "testenv", "gpg_keyring"))
WRITABLE_TEST_GNUPG_HOME = getattr(settings, "EMAIL_EXTRAS_WRITABLE_TEST_GNUPG_DIR", True)

if USE_GNUPG:
    try:
        import gnupg  # noqa: F401
    except ImportError:
        raise ImproperlyConfigured("Could not import gnupg")
