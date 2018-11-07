from cffi import FFI
import glob
import re
import os

spx_ref_dir = os.path.join("src", "sphincsplus", "ref")


def paramsets():
    pattern = "params-sphincs-([a-zA-Z-][a-zA-Z0-9-]*).h"
    paramfiles = os.listdir(os.path.join(spx_ref_dir, "params"))
    for paramset in paramfiles:
        try:
            yield re.search(pattern, paramset).group(1).replace('-', '_')
        except AttributeError:
            raise Exception("Cannot parse name of parameter set {}"
                            .format(paramset))


def make_ffi(paramset):
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

    if 'haraka' not in paramset:
        sources.remove(os.path.join(spx_ref_dir, "hash_haraka.c"))
    if 'sha256' not in paramset:
        sources.remove(os.path.join(spx_ref_dir, "hash_sha256.c"))
    if 'shake256' not in paramset:
        sources.remove(os.path.join(spx_ref_dir, "hash_shake256.c"))

    sources.remove(os.path.join(spx_ref_dir, "PQCgenKAT_sign.c"))
    sources.remove(os.path.join(spx_ref_dir, "rng.c"))

    ffi.set_source("_spx_{}".format(paramset), api_contents, sources=sources)

    return ffi


for paramset in paramsets():
    globals()[paramset] = make_ffi(paramset)
