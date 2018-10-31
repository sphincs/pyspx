from _spx import ffi, lib


CRYPTO_BYTES = lib.crypto_bytes()
CRYPTO_SECRETKEYBYTES = lib.crypto_secretkeybytes()
CRYPTO_PUBLICKEYBYTES = lib.crypto_publickeybytes()
CRYPTO_SEEDBYTES = lib.crypto_seedbytes()


def sign(message, secretkey):
    if not isinstance(message, bytes):
        raise TypeError('Input message must be of type bytes')
    if not isinstance(secretkey, bytes):
        raise TypeError('Secret key must be of type bytes')

    if len(secretkey) != CRYPTO_SECRETKEYBYTES:
        raise MemoryError('Secret key is of length {}, expected {}'.format(len(secretkey), CRYPTO_SECRETKEYBYTES))

    sm = ffi.new("unsigned char[]", len(message) + CRYPTO_BYTES)
    mlen = ffi.cast("unsigned long long", len(message))
    smlen = ffi.new("unsigned long long *")
    lib.crypto_sign(sm, smlen, message, len(message), secretkey)
    return bytes(sm)[:CRYPTO_BYTES]


def verify(message, signature, publickey):
    if not isinstance(message, bytes):
        raise TypeError('Message must be of type bytes')
    if not isinstance(signature, bytes):
        raise TypeError('Signature must be of type bytes')
    if not isinstance(publickey, bytes):
        raise TypeError('Public key must be of type bytes')

    if len(publickey) != CRYPTO_PUBLICKEYBYTES:
        raise MemoryError('Public key is of length {}, expected {}'.format(len(publickey), CRYPTO_PUBLICKEYBYTES))
    if len(signature) != CRYPTO_BYTES:
        raise MemoryError('Signature is of length {}, expected {}'.format(len(signature), CRYPTO_BYTES))

    smlen = ffi.cast("unsigned long long", len(message) + CRYPTO_BYTES)
    mlen = ffi.new("unsigned long long *")
    m = ffi.new("unsigned char[]", int(smlen))
    sm = ffi.new("unsigned char[]", int(smlen))
    return int(lib.crypto_sign_open(m, mlen, sm, smlen, publickey)) == 0


def generate_keypair():
    pk = ffi.new("unsigned char[]", CRYPTO_PUBLICKEYBYTES)
    sk = ffi.new("unsigned char[]", CRYPTO_SECRETKEYBYTES)
    lib.crypto_sign_keypair(pk, sk)

    return bytes(pk), bytes(sk)
