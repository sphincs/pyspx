#!/bin/bash

# This script can be used to create wheels based on manylinux1, as follows:
# sudo docker run --rm -v `pwd`:/io quay.io/pypa/manylinux1_x86_64 /io/build-wheels.sh
# sudo docker run --rm -v `pwd`:/io quay.io/pypa/manylinux1_i686 linux32 /io/build-wheels.sh

set -e -x

yum install -y openssl-devel

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install "cffi>=1.0.0"
    "${PYBIN}/pip" wheel /io/ -w dist/
done

# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    auditwheel repair "$whl" -w /io/dist/
done

# TODO actually test the wheels here
