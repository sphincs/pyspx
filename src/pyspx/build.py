from cffi import FFI
import glob
import re
import os
import shutil

spx_ref_dir = os.path.join("src", "sphincsplus", "ref")
spx_inst_dir = os.path.join("src", "sphincsplus-instances")


def paramsets():
    pattern = "params-sphincs-([a-zA-Z-][a-zA-Z0-9-]*).h"
    paramfiles = os.listdir(os.path.join(spx_ref_dir, "params"))
    for paramfile in paramfiles:
        try:
            yield (re.search(pattern, paramfile).group(1).replace('-', '_'),
                   paramfile)
        except AttributeError:
            raise Exception("Cannot parse name of parameter set {}"
                            .format(paramfile))


def make_ffi(paramset, paramfile):
    ffi = FFI()

    api_contents = []
    with open(os.path.join(spx_ref_dir, "api.h"), "r") as f:
        # This is specific to api.h in the sphincsplus reference code
        for line in f.readlines():
            if line.startswith('#'):
                continue  # we ignore all C preprocessor macros
            api_contents.append(line)
    api_contents = '\n'.join(api_contents)
    ffi.cdef(api_contents)

    sources = glob.glob(os.path.join(spx_ref_dir, "*.c"))
    headers = glob.glob(os.path.join(spx_ref_dir, "*.h"))
    libraries = []

    if 'haraka' not in paramset:
        sources.remove(os.path.join(spx_ref_dir, "hash_haraka.c"))
    if 'sha256' not in paramset:
        sources.remove(os.path.join(spx_ref_dir, "hash_sha256.c"))
    if 'shake256' not in paramset:
        sources.remove(os.path.join(spx_ref_dir, "hash_shake256.c"))

    if 'sha256' in paramset:
        libraries += ['crypto']

    sources.remove(os.path.join(spx_ref_dir, "PQCgenKAT_sign.c"))
    sources.remove(os.path.join(spx_ref_dir, "rng.c"))

    headers.remove(os.path.join(spx_ref_dir, "params.h"))
    headers.append(os.path.join(spx_ref_dir, "params", paramfile))

    # we need to move everything to an instance-specific directory, as the code
    # contains references to params.h, and the content of that file needs to
    # differ for each instance. We cannot hot-swap params.h in the ref/
    # directory, as the source files are first all collected by cffi before
    # any compilation is started.
    inst_dir = os.path.join(spx_inst_dir, paramset)

    try:
        os.makedirs(inst_dir)
    except OSError:  # raised if the leaf directory already exists
        pass

    for file in sources + headers:
        shutil.copy(file, inst_dir)
    shutil.move(os.path.join(inst_dir, paramfile),
                os.path.join(inst_dir, "params.h"))

    inst_sources = glob.glob(os.path.join(inst_dir, "*.c"))

    ffi.set_source("_spx_{}".format(paramset), api_contents,
                   sources=inst_sources, libraries=libraries)

    return ffi


for paramset, paramfile in paramsets():
    globals()[paramset] = make_ffi(paramset, paramfile)
