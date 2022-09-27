# PySPX [![SPHINCS Python Bindings](https://github.com/sphincs/pyspx/actions/workflows/python-app.yml/badge.svg)](https://github.com/sphincs/pyspx/actions/workflows/python-app.yml)

This repository contains a Python package that provides bindings for [SPHINCS+](https://github.com/sphincs/sphincsplus). It provides support for all parameter sets included as part of [the SPHINCS+ submission](http://sphincs.org/data/sphincs+-specification.pdf) to [NIST's Post-Quantum Cryptography Standardization project](https://csrc.nist.gov/projects/post-quantum-cryptography).

While this package is functionally complete, it may still be subject to small API changes.
Currently, the bindings only wrap the reference code. Code optimized for specific platforms (such as machines with AVX2 or AESNI support) is ignored.

### Installation

The package is [available on PyPI](https://pypi.org/project/PySPX/) and can be installed by simply calling `pip install pyspx`.

For Linux, binary wheels are available based on the `manylinux1` docker image. On other platforms it may take a few moments to compile the SPHINCS+ code. Currently the `sphincsplus` reference code requires `openssl` for its SHA256 function. When compiling from source, be sure to install openssl with development files.

### API

After installing the package, import a specific instance of SPHINCS+ as follows (e.g. for `shake256-128f`):

```
import pyspx.shake_128f
```

This exposes the following straight-forward functions. All parameters are assumed to be `bytes` objects. Similarly, the returned keys and signatures are `bytes`. The `verify` function returns a boolean indicating success or failure.

```
>>> public_key, secret_key = pyspx.shake_128f.generate_keypair(seed)
>>> signature = pyspx.shake_128f.sign(message, secret_key)
>>> pyspx.shake_128f.verify(message, signature, public_key)
True
```

Additionally, the following attributes expose the expected sizes, as a consequence of the selected parameter set:

```
>>> pyspx.shake_128f.crypto_sign_BYTES
29792
>>> pyspx.shake_128f.crypto_sign_PUBLICKEYBYTES
64
>>> pyspx.shake_128f.crypto_sign_SECRETKEYBYTES
128
>>> pyspx.shake_128f.crypto_sign_SEEDBYTES
96
```

### Custom SPHINCS+ parameters

It is fairly easy to compile with additional SPHINCS+ parameters.
To do this, clone the repository, initialize the `src/sphincsplus` submodule,
and add a new parameter set to `src/sphincsplus/ref/params`.
Make sure to follow the `params-sphincs-[parameters-shorthand].h` naming convention.
Installing the Python package from this modified source will expose the parameter set using the API described above.
