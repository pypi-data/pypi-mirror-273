from unittest import TestCase

from tc66c2mqtt.tc66_decryptor import tc66_decryptor
from tc66c2mqtt.tests.fixtures import DECRYPTED_DATA, RAW_TC66_DATA


class TC66DecryptorTestCase(TestCase):
    def test_tc66_decryptor(self):
        result: bytes = tc66_decryptor(crypted_data=RAW_TC66_DATA)
        self.assertEqual(result.hex(), DECRYPTED_DATA.hex())
