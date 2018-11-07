import os
import re
import glob

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.develop import develop as _develop
from distutils.command.clean import clean as _clean


def paramsets():
    pattern = "params-sphincs-([a-zA-Z-][a-zA-Z0-9-]*).h"
    pfiles = os.listdir(os.path.join("src", "sphincsplus", "ref", "params"))
    for paramset in pfiles:
        try:
            yield re.search(pattern, paramset).group(1).replace('-', '_')
        except AttributeError:
            raise Exception("Cannot parse name of parameter set {}"
                            .format(paramset))


def create_param_wrappers():
    for paramset in paramsets():
        with open(os.path.join("src", "pyspx", paramset + ".py"), 'w') as f:
            f.write(
                "from pyspx.bindings import PySPXBindings as _PySPXBindings\n"
                "from _spx_{} import ffi as _ffi, lib as _lib\n"
                "\n"
                "import sys\n"
                "\n"
                "sys.modules[__name__] = _PySPXBindings(_ffi, _lib)\n"
                .format(paramset)
            )


class build_py(_build_py):

    def run(self):
        create_param_wrappers()
        super().run()


class develop(_develop):

    def run(self):
        create_param_wrappers()
        super().run()


class clean(_clean):

    def run(self):
        for paramset in paramsets():
            os.remove(os.path.join("src", "pyspx", paramset + ".py"))
            os.remove(os.path.join("src", "_spx_{}.abi3.so".format(paramset)))
        super().run()


setup(
    name="PySPX",
    version="0.1.0",
    packages=['pyspx'],
    author="Joost Rijneveld, Peter Schwabe",
    author_email='contact@sphincs.org',
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
    ],
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    tests_require=["pytest", "cffi>=1.0.0"],
    cffi_modules=["src/pyspx/build.py:{}".format(x) for x in paramsets()],
    cmdclass={
        "build_py": build_py,
        "develop": develop,
        "clean": clean,
    },
    zip_safe=False,
)
