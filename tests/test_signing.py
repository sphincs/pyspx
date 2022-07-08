import pytest
import os
import random
import importlib
import struct

paramsets = [
    'shake_128s',
    'shake_128f',
    'shake_192s',
    'shake_192f',
    'shake_256s',
    'shake_256f',
    'sha2_128s',
    'sha2_128f',
    'sha2_192s',
    'sha2_192f',
    'sha2_256s',
    'sha2_256f',
    'haraka_128s',
    'haraka_128f',
    'haraka_192s',
    'haraka_192f',
    'haraka_256s',
    'haraka_256f',
]

expected_sizes = [
    [32, 64,  7856],
    [32, 64,  17088],
    [48, 96,  16224],
    [48, 96,  35664],
    [64, 128, 29792],
    [64, 128, 49856],
    [32, 64,  7856],
    [32, 64,  17088],
    [48, 96,  16224],
    [48, 96,  35664],
    [64, 128, 29792],
    [64, 128, 49856],
    [32, 64,  7856],
    [32, 64,  17088],
    [48, 96,  16224],
    [48, 96,  35664],
    [64, 128, 29792],
    [64, 128, 49856],
]

instances = []

for paramset in paramsets:
    instances.append(importlib.import_module('pyspx.' + paramset))


@pytest.mark.parametrize("pyspx,sizes", zip(instances, expected_sizes))
def test_sizes(pyspx, sizes):
    print(pyspx, pyspx.crypto_sign_PUBLICKEYBYTES, pyspx.crypto_sign_SECRETKEYBYTES, pyspx.crypto_sign_BYTES)
    assert pyspx.crypto_sign_PUBLICKEYBYTES == sizes[0]
    assert pyspx.crypto_sign_SECRETKEYBYTES == sizes[1]
    assert pyspx.crypto_sign_BYTES == sizes[2]


@pytest.mark.parametrize("pyspx", instances)
def test_keygen(pyspx):
    seed = bytes()
    with pytest.raises(MemoryError):
        pyspx.generate_keypair(seed)
    seed = os.urandom(pyspx.crypto_sign_SEEDBYTES)
    publickey, secretkey = pyspx.generate_keypair(seed)


@pytest.mark.parametrize("pyspx", instances)
def test_sign_verify(pyspx):
    seed = os.urandom(pyspx.crypto_sign_SEEDBYTES)
    publickey, secretkey = pyspx.generate_keypair(seed)
    message = os.urandom(32)
    signature = pyspx.sign(message, secretkey)
    assert pyspx.verify(message, signature, publickey)


@pytest.mark.parametrize("pyspx", instances)
def test_invalid_signature(pyspx):
    seed = os.urandom(pyspx.crypto_sign_SEEDBYTES)
    publickey, secretkey = pyspx.generate_keypair(seed)
    message = os.urandom(32)

    # incorrect sk length
    with pytest.raises(MemoryError):
        pyspx.sign(message, bytes())

    # incorrect type for message or key
    with pytest.raises(TypeError):
        pyspx.sign(42, secretkey)
    with pytest.raises(TypeError):
        pyspx.sign(message, 42)

    signature = pyspx.sign(message, secretkey)

    for _ in range(10):
        n = random.randint(0, len(signature))

        # Flip a random bit
        ba_sig = bytearray(signature)
        ba_sig[n] ^= 1

        assert not pyspx.verify(message, bytes(ba_sig), publickey)    

    # incorrect pk length
    with pytest.raises(MemoryError):
        pyspx.verify(message, signature, bytes())
    # incorrect signature length
    with pytest.raises(MemoryError):
        pyspx.verify(message, bytes(), publickey)

    # incorrect type for message, signature or key
    with pytest.raises(TypeError):
        pyspx.verify(42, signature, publickey)
    with pytest.raises(TypeError):
        pyspx.verify(message, 42, publickey)
    with pytest.raises(TypeError):
        pyspx.verify(message, signature, 42)


@pytest.mark.parametrize("pyspx", instances)
def test_long_message(pyspx):
    seed = os.urandom(pyspx.crypto_sign_SEEDBYTES)
    publickey, secretkey = pyspx.generate_keypair(seed)
    message = bytes(2**20)
    signature = pyspx.sign(message, secretkey)
    assert pyspx.verify(message, signature, publickey)
