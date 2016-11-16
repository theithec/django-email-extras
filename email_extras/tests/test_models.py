import os
from django.test import TestCase
from unittest.mock import patch
from unittest import skipIf
from email_extras.models import Address, Key, GPG
from email_extras import settings
from email_extras.tests import KeysTestCase

@patch("email_extras.models.GNUPG_HOME", settings.TEST_GNUPG_HOME)
@patch("email_extras.utils.GNUPG_HOME", settings.TEST_GNUPG_HOME)
class AddressTestCase(KeysTestCase):

    @skipIf(not settings.WRITABLE_TEST_GNUPG_HOME, "settings.WRITABLE_TEST_GNUPG_HOME not True")
    def test_gpgkey_deleted_on_address_delete(self):
        assert any(["untrusted_expired" in keydata["uids"][0] for keydata in self.gpg.list_keys()])
        key = self.keys["untrusted_expired"]
        for address in key.address_set.all():
            address.delete()

        assert not any(["untrusted_expired" in keydata["uids"][0] for keydata in self.gpg.list_keys()])
        # reimport
        with open(os.path.join(settings.TEST_GNUPG_HOME, "untrusted_expired.asc")) as keyfile:
            self.gpg.import_keys(keyfile.read())

