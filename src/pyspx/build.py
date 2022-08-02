from cffi import FFI
import glob
import re
import os
import shutil
from pathlib import Path

PARAM_DIR_NAME = "params"

SOURCES = [
    "address.c",
    "randombytes.c", 
    "merkle.c",
    "wots.c",
    "wotsx1.c",
    "utils.c",
    "utilsx1.c", 
    "fors.c",
    "sign.c"
]

HEADERS = [
    "address.h",
    "randombytes.h",
    "merkle.h",
    "wots.h",
    "wotsx1.h",
    "utils.h",
    "utilsx1.h",
    "fors.h",
    "api.h",
    "hash.h",
    "thash.h",
    "context.h"
]

PARAM_SETS_SOURCES = {
    "sha2": {
        "sources": ["sha2.c", "hash_sha2.c", "thash_sha2_robust.c"],
        "headers": ["sha2.h", "sha2_offsets.h"],
    },
    "shake":  {
        "sources": ["fips202.c", "hash_shake.c", "thash_shake_robust.c"],
        "headers": ["fips202.h", "shake_offsets.h"],
    },
    "haraka":  {
        "sources": ["haraka.c", "hash_haraka.c", "thash_haraka_robust.c"],
        "headers": ["haraka.h", "haraka_offsets.h"],
    },
}

spx_ref_dir = Path("src", "sphincsplus", "ref")
spx_inst_dir = Path("src", "sphincsplus-instances")


def paramsets():
    pattern = "params-sphincs-([a-zA-Z-][a-zA-Z0-9-]*).h"
    paramfiles = os.listdir(spx_ref_dir / "params")

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
    with open(spx_ref_dir / "api.h", "r") as f:
        # This is specific to api.h in the sphincsplus reference code
        for line in f.readlines():
            if line.startswith('#'):
                continue  # we ignore all C preprocessor macros
            api_contents.append(line)
    api_contents = '\n'.join(api_contents)
    ffi.cdef(api_contents)

    sources = SOURCES.copy()
    headers = HEADERS.copy()
    libraries = []

    for hash_algo, files in PARAM_SETS_SOURCES.items():
        if hash_algo in paramset:
            sources += files["sources"]
            headers += files["headers"]

    # we need to move everything to an instance-specific directory, as the code
    # contains references to params.h, and the content of that file needs to
    # differ for each instance. We cannot hot-swap params.h in the ref/
    # directory, as the source files are first all collected by cffi before
    # any compilation is started.
    inst_dir = spx_inst_dir / paramset
    inst_param_dir = inst_dir / PARAM_DIR_NAME

    try:
        os.makedirs(inst_dir, exist_ok=True)
        os.mkdir(inst_param_dir)
    except FileExistsError:
        pass
    
    for source_file in sources + headers:
        shutil.copy(spx_ref_dir / source_file, inst_dir)
    
    shutil.copy(spx_ref_dir / "params" / paramfile, inst_param_dir /  "params.h")
    
    # We add a params header that includes the instance-specific 
    # params header. This is a trick to keep the relative includes
    # in the SPHINCS headers working.
    with open(inst_dir / "params.h", "w") as f:
        f.write('#include "params/params.h"')

    inst_sources = glob.glob(os.path.join(inst_dir, "*.c"))

    ffi.set_source("_spx_{}".format(paramset), api_contents,
                   sources=inst_sources, libraries=libraries)

    return ffi


for paramset, paramfile in paramsets():
    globals()[paramset] = make_ffi(paramset, paramfile)
