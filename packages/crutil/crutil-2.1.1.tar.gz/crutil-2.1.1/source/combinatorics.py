"""
This code interfaces with the "combinatorics" C library.
"""

# Standard import.
from ctypes import c_void_p, c_char_p, c_int32, cast

# Local imports.
from .utils import make_contact_template, refine_ffunc
from .c_utils import get_local_c_library

# Local constants.
CLIB = get_local_c_library("combinatorics")

#############
# FUNCTIONS #
#############

def make_contact():
    """ Prove that you can access this library. """
    return make_contact_template(CLIB)

def free_string(string_pointer: c_char_p):
    """ Calling this, after having called a C function which returns a string,
    prevents memory leaks. """
    cfunc = refine_ffunc(CLIB.free_string, [c_char_p], None)
    cfunc(string_pointer)

def factorial(num: int) -> int:
    """ Return num!. """
    cfunc = refine_ffunc(CLIB.factorial, [c_int32], c_void_p)
    raw_pointer = cfunc(num)
    string_pointer = cast(raw_pointer, c_char_p)
    result = int(string_pointer.value.decode())
    free_string(string_pointer)
    return result
