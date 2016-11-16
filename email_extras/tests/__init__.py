import os
from unittest.mock import patch
from django.test import TestCase, override_settings
from email_extras.models import Key, GPG
from email_extras.utils import send_mail, EncryptionFailedError
from email_extras import settings




class KeysTestCase(TestCase):

    @classmethod
    @patch("email_extras.models.GNUPG_HOME", settings.TEST_GNUPG_HOME)
    @patch("email_extras.utils.GNUPG_HOME", settings.TEST_GNUPG_HOME)
    def setUpClass(cls):
        """Create the Keys/Addresses

        Make sure the four public keys and three secret keys exist as expected
        """
        super().setUpClass()
        cls.gpg = GPG(gnupghome=settings.TEST_GNUPG_HOME, use_agent=True)
        cls.keys = {}
        for keydata in cls.gpg.list_keys():
            keyid = keydata["keyid"]
            uid = keydata["uids"][0]
            name = uid[uid.find("<") + 1: uid.find("@")]
            pubkey = cls.gpg.export_keys(keyid)
            cls.keys[name] = Key.objects.get_or_create(key=pubkey)[0]

        cls.gpg.trust_keys(
            [cls.keys[name].fingerprint for name in ("trusted_valid", "trusted_expired")], "TRUST_ULTIMATE")

        cls.gpg.trust_keys( [cls.keys[name].fingerprint for name in ("untrusted_valid", "untrusted_expired")], "TRUST_UNDEFINED")

        assert len(cls.gpg.list_keys(secret=True)) == 3 , f"Three secret keys in {settings.TEST_GNUPG_HOME} expected."
