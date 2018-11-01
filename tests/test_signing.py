
import pytest
import spx.shake256_192s as spx

import os


def test_sign_verify():
    publickey, secretkey = spx.generate_keypair()
    message = os.urandom(32)
    signature = spx.sign(message, secretkey)
    assert spx.verify(message, signature, publickey)
