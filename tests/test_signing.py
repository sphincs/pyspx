
import pytest
import pyspx.shake256_192s as pyspx

import os


def test_sign_verify():
    publickey, secretkey = pyspx.generate_keypair()
    message = os.urandom(32)
    signature = pyspx.sign(message, secretkey)
    assert pyspx.verify(message, signature, publickey)
