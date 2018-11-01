from _spx import ffi, lib


crypto_sign_BYTES = lib.crypto_sign_spx_shake256_192s_bytes()
crypto_sign_SECRETKEYBYTES = lib.crypto_sign_spx_shake256_192s_secretkeybytes()
crypto_sign_PUBLICKEYBYTES = lib.crypto_sign_spx_shake256_192s_publickeybytes()
crypto_sign_SEEDBYTES = lib.crypto_sign_spx_shake256_192s_seedbytes()

# TODO make this more generic for parameter sets that are not shake256_192s

def sign(message, secretkey):
    if not isinstance(message, bytes):
        raise TypeError('Input message must be of type bytes')
    if not isinstance(secretkey, bytes):
        raise TypeError('Secret key must be of type bytes')

    if len(secretkey) != crypto_sign_SECRETKEYBYTES:
        raise MemoryError('Secret key is of length {}, expected {}'.format(len(secretkey), crypto_sign_SECRETKEYBYTES))

    sm = ffi.new("unsigned char[]", len(message) + crypto_sign_BYTES)
    mlen = ffi.cast("unsigned long long", len(message))
    smlen = ffi.new("unsigned long long *")
    lib.crypto_sign_spx_shake256_192s(sm, smlen, message, mlen, secretkey)
    return bytes(sm)[:crypto_sign_BYTES]


def verify(message, signature, publickey):
    if not isinstance(message, bytes):
        raise TypeError('Message must be of type bytes')
    if not isinstance(signature, bytes):
        raise TypeError('Signature must be of type bytes')
    if not isinstance(publickey, bytes):
        raise TypeError('Public key must be of type bytes')

    if len(publickey) != crypto_sign_PUBLICKEYBYTES:
        raise MemoryError('Public key is of length {}, expected {}'.format(len(publickey), crypto_sign_PUBLICKEYBYTES))
    if len(signature) != crypto_sign_BYTES:
        raise MemoryError('Signature is of length {}, expected {}'.format(len(signature), crypto_sign_BYTES))

    smlen = ffi.cast("unsigned long long", len(message) + crypto_sign_BYTES)
    mlen = ffi.new("unsigned long long *")
    m = ffi.new("unsigned char[]", int(smlen))
    sm = ffi.new("unsigned char[]", signature + message)
    return int(lib.crypto_sign_spx_shake256_192s_open(m, mlen, sm, smlen, publickey)) == 0


def generate_keypair():
    pk = ffi.new("unsigned char[]", crypto_sign_PUBLICKEYBYTES)
    sk = ffi.new("unsigned char[]", crypto_sign_SECRETKEYBYTES)
    lib.crypto_sign_spx_shake256_192s_keypair(pk, sk)

    return bytes(pk), bytes(sk)
