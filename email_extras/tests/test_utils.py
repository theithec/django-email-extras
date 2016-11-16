import logging
from unittest.mock import patch
import django.core.mail
from email_extras.utils import send_mail, EncryptionFailedError
from email_extras import settings
from email_extras.tests import KeysTestCase


logger = logging.getLogger(__name__)

SUBJECT = "Subject"
BODY = "Text"
SENDER = "sender@localhost@localdomain"


def _addr(name):
    return name + "@localhost.localdomain"


@patch("email_extras.models.GNUPG_HOME", settings.TEST_GNUPG_HOME)
@patch("email_extras.utils.GNUPG_HOME", settings.TEST_GNUPG_HOME)
class UtilsTestCase(KeysTestCase):

    def is_encrypted(self, passphrase):
        mail = django.core.mail.outbox[0]
        self.assertTrue(
            mail.body.startswith("""-----BEGIN PGP MESSAGE-----"""))
        logger.debug("MAILBODY: %s", mail.body)
        result = self.gpg.decrypt(mail.body, passphrase=passphrase, always_trust=True)
        self.assertEqual(
            str(result), BODY)

    # trusted_valid

    @patch("email_extras.utils.ALWAYS_TRUST", False)
    def test_success_send_trusted_valid_no_always_trust(self):
        send_mail(SUBJECT, BODY, SENDER, [_addr("trusted_valid")])
        self.is_encrypted("trusted_valid")

    # untrusted_valid

    @patch("email_extras.utils.ALWAYS_TRUST", True)
    def test_success_send_untrusted_valid_with_always_trust(self):
        send_mail(SUBJECT, BODY, SENDER, [_addr("untrusted_valid")])
        self.is_encrypted("untrusted_valid")

    @patch("email_extras.utils.ALWAYS_TRUST", False)
    def test_fail_send_untrusted_valid_no_always_trust(self):
        with self.assertRaises(EncryptionFailedError):
            send_mail(SUBJECT, BODY, SENDER, [_addr("untrusted_valid")])

    # trusted_expired

    @patch("email_extras.utils.ALWAYS_TRUST", False)
    def test_fail_send_trusted_expired_no_always_trust(self):
        with self.assertRaises(EncryptionFailedError):
            send_mail(SUBJECT, BODY, SENDER, [_addr("trusted_expired")])

    @patch("email_extras.utils.ALWAYS_TRUST", True)
    def test_fail_send_trusted_expired_with_always_trust(self):
        with self.assertRaises(EncryptionFailedError):
            send_mail(SUBJECT, BODY, SENDER, [_addr("trusted_expired")])

    # untrusted_expired

    @patch("email_extras.utils.ALWAYS_TRUST", False)
    def test_fail_send_untrusted_expired_no_always_trust(self):
        with self.assertRaises(EncryptionFailedError):
            send_mail(SUBJECT, BODY, SENDER, [_addr("untrusted_expired")])

    @patch("email_extras.utils.ALWAYS_TRUST", True)
    def test_fail_send_untrusted_expired_with_always_trust(self):
        with self.assertRaises(EncryptionFailedError):
            send_mail(SUBJECT, BODY, SENDER, [_addr("untrusted_expired")])

