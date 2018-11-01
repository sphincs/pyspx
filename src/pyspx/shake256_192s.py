import pyspx.bindings


def sign(message, secretkey):
    return pyspx.bindings.sign(message, secretkey)


def verify(message, signature, publickey):
    return pyspx.bindings.verify(message, signature, publickey)


def generate_keypair():
    return pyspx.bindings.generate_keypair()


crypto_sign_BYTES = pyspx.bindings.crypto_sign_BYTES
crypto_sign_SECRETKEYBYTES = pyspx.bindings.crypto_sign_SECRETKEYBYTES
crypto_sign_PUBLICKEYBYTES = pyspx.bindings.crypto_sign_PUBLICKEYBYTES
crypto_sign_SEEDBYTES = pyspx.bindings.crypto_sign_SEEDBYTES
