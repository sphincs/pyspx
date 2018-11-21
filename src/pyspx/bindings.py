
class PySPXBindings(object):

    def __init__(self, ffi, lib):
        self.ffi = ffi
        self.lib = lib

    @property
    def crypto_sign_BYTES(self):
        return self.lib.crypto_sign_bytes()

    @property
    def crypto_sign_SECRETKEYBYTES(self):
        return self.lib.crypto_sign_secretkeybytes()

    @property
    def crypto_sign_PUBLICKEYBYTES(self):
        return self.lib.crypto_sign_publickeybytes()

    @property
    def crypto_sign_SEEDBYTES(self):
        return self.lib.crypto_sign_seedbytes()

    def sign(self, message, secretkey):
        if not isinstance(message, bytes):
            raise TypeError('Input message must be of type bytes')
        if not isinstance(secretkey, bytes):
            raise TypeError('Secret key must be of type bytes')

        if len(secretkey) != self.crypto_sign_SECRETKEYBYTES:
            raise MemoryError('Secret key is of length {}, expected {}'
                              .format(len(secretkey),
                                      self.crypto_sign_SECRETKEYBYTES))

        sm = self.ffi.new("unsigned char[]",
                          len(message) + self.crypto_sign_BYTES)
        mlen = self.ffi.cast("unsigned long long", len(message))
        smlen = self.ffi.new("unsigned long long *")
        self.lib.crypto_sign(sm, smlen, message, mlen, secretkey)
        return bytes(self.ffi.buffer(sm, self.crypto_sign_BYTES))

    def verify(self, message, signature, publickey):
        if not isinstance(message, bytes):
            raise TypeError('Message must be of type bytes')
        if not isinstance(signature, bytes):
            raise TypeError('Signature must be of type bytes')
        if not isinstance(publickey, bytes):
            raise TypeError('Public key must be of type bytes')

        if len(publickey) != self.crypto_sign_PUBLICKEYBYTES:
            raise MemoryError('Public key is of length {}, expected {}'
                              .format(len(publickey),
                                      self.crypto_sign_PUBLICKEYBYTES))
        if len(signature) != self.crypto_sign_BYTES:
            raise MemoryError('Signature is of length {}, expected {}'
                              .format(len(signature), self.crypto_sign_BYTES))

        smlen = self.ffi.cast("unsigned long long",
                              len(message) + self.crypto_sign_BYTES)
        mlen = self.ffi.new("unsigned long long *")
        m = self.ffi.new("unsigned char[]", int(smlen))
        sm = self.ffi.new("unsigned char[]", signature + message)
        return self.lib.crypto_sign_open(m, mlen, sm, smlen, publickey) == 0

    def generate_keypair(self, seed):
        pk = self.ffi.new("unsigned char[]", self.crypto_sign_PUBLICKEYBYTES)
        sk = self.ffi.new("unsigned char[]", self.crypto_sign_SECRETKEYBYTES)
        if len(seed) != self.crypto_sign_SEEDBYTES:
            raise MemoryError('Seed is of length {}, expected {}'
                              .format(len(seed), self.crypto_sign_SEEDBYTES))
        self.lib.crypto_sign_seed_keypair(pk, sk, seed)

        return bytes(self.ffi.buffer(pk)), bytes(self.ffi.buffer(sk))

    def __repr__(self):  # pragma: no cover
        return repr(self.lib).replace("Lib", "PySPXBindings")
