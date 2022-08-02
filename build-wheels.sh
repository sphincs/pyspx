#!/bin/bash

# This script can be used to create wheels based on manylinux1, as follows:
# docker run --rm -v `pwd`:/io quay.io/pypa/manylinux_2_28_x86_64 /io/build-wheels.sh
# python3 -m twine upload dist/*

set -e -x

yum install -y openssl-devel

cd /io

# Compile wheels
for PYBIN in /opt/python/cp*/bin; do
    "${PYBIN}/pip" install --upgrade build
    "${PYBIN}/python" -m build
done

# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    auditwheel repair "$whl" -w /io/dist/
    rm "$whl"
done

# TODO actually test the wheels here
