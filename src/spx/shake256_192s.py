import spx.bindings


def sign(message, secretkey):
    return spx.bindings.sign(message, secretkey)


def verify(message, signature, publickey):
    return spx.bindings.verify(message, signature, publickey)


def generate_keypair():
    return spx.bindings.generate_keypair()


crypto_sign_BYTES = spx.bindings.crypto_sign_BYTES
crypto_sign_SECRETKEYBYTES = spx.bindings.crypto_sign_SECRETKEYBYTES
crypto_sign_PUBLICKEYBYTES = spx.bindings.crypto_sign_PUBLICKEYBYTES
crypto_sign_SEEDBYTES = spx.bindings.crypto_sign_SEEDBYTES
