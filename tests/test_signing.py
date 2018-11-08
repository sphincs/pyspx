import pyspx.shake256_192s as pyspx

import os


def test_sign_verify():
    seed = os.urandom(pyspx.crypto_sign_SEEDBYTES)
    publickey, secretkey = pyspx.generate_keypair(seed)
    message = os.urandom(32)
    signature = pyspx.sign(message, secretkey)
    assert pyspx.verify(message, signature, publickey)
