from cffi import FFI

ffi = FFI()

api_contents = []
with open("src/sphincsplus/libspx.h", "r") as apifile:
    # This is very specific to api.h in the sphincsplus reference code
    for line in apifile.readlines():
        if line.startswith('#'):
            continue  # we ignore all C preprocessor macros
        api_contents.append(line)
api_contents =  '\n'.join(api_contents)
ffi.cdef(api_contents)

extra_objects = ["src/sphincsplus/libspx.so"]
ffi.set_source("_spx", api_contents, extra_objects=extra_objects)
