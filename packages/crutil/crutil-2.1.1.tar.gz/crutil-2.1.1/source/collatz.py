"""
This code interfaces with the "collatz" Rust library.
"""

# Standard imports.
from ctypes import c_int32

# Local imports.
from .utils import make_contact_template, refine_ffunc
from .rust_utils import get_local_rust_library, MAX_I32

# Local constants.
RUST_LIB = get_local_rust_library("hosker_collatz")

#############
# FUNCTIONS #
#############

def make_contact():
    """ Prove that you can access this library. """
    return make_contact_template(RUST_LIB)

def next_collatz_python(num: int) -> int:
    """ Like the similarly-named Rust function, but suitable for large
    integers. """
    if num%2 == 0:
        result = num/2
    else:
        result = (3*num)+1
    return result

def count_collatz_steps_large(num: int) -> int:
    """ As below, but suitable for large integers. """
    result = 0
    while num != 1:
        result += 1
        num = next_collatz_python(num)
    return result

def count_collatz_steps(num: int) -> int:
    """ Count the number of Collatz steps required to reach 1, given a starting
    point. """
    if num > MAX_I32:
        return count_collatz_steps_large(num)
    rust_func = refine_ffunc(RUST_LIB.count_collatz_steps, [c_int32], c_int32)
    result = rust_func(num)
    return result

def max_collatz_steps_under_large(limit: int) -> int:
    """ As below, but suitable for large integers. """
    result = 1
    current_max = 0
    current = 0
    for num in range(1, limit+1):
        current = count_collatz_steps(num)
        if current > current_max:
            result = num
            current_max = current
    return result

def max_collatz_steps_under(limit: int) -> int:
    """ Find the maximum number of Collatz steps required to reach 1, if one
    uses all the numbers between 1 and a given limit (inclusive) as starting
    points. """
    if limit > MAX_I32:
        return max_collatz_steps_under_large(limit)
    rust_func = \
        refine_ffunc(RUST_LIB.max_collatz_steps_under, [c_int32], c_int32)
    result = rust_func(limit)
    return result
