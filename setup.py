from setuptools import setup, find_packages

# TODO figure out a nice way to build the sphincsplus shared object file here

setup(
    name="PySPX",
    version="0.1.0",
    packages=find_packages('src'),
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
    cffi_modules=[
        "src/pyspx/build.py:ffi",
    ],
)

