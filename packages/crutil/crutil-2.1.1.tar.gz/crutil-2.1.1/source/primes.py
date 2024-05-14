"""
This code interfaces with the "primes" Rust library.
"""

# Standard imports.
import warnings
from ctypes import c_char_p, c_int32, c_void_p, cast

# Non-standard imports.
import sympy

# Local imports.
from .utils import make_contact_template, int_to_bool, refine_ffunc
from .rust_utils import get_local_rust_library, rusticate_int, MAX_I32

# Local constants.
RUST_LIB = get_local_rust_library("hosker_primes")
MAX_DIGITS = 100
BIGINT_DIGIT_LIST_C_TYPE = c_int32*MAX_DIGITS
MAX_PRIME_ORDINAL_I32 = 105097565

#############
# FUNCTIONS #
#############

def make_contact():
    """ Prove that you can access this library. """
    return make_contact_template(RUST_LIB)

def is_prime_i32(number: int) -> bool:
    """ Determine whether a given 32-bit integer is prime. """
    rust_func = refine_ffunc(RUST_LIB.is_prime_i32, [c_int32], c_int32)
    rust_result = rust_func(number)
    result = int_to_bool(rust_result)
    return result

def is_prime_bigint_rust(number: int) -> bool:
    """
    Determine whether an arbitrarily large number is prime, where that
    arbitrarily large number is represented by a list of "digits", and where
    each of those "digits" represents a power of 2**32, rather than of 10.

    IMPORTANT: This function is SLOWER than sympy.isprime(n).
    """
    bigint_digit_list, _ = rusticate_int(number)
    c_array = BIGINT_DIGIT_LIST_C_TYPE(*bigint_digit_list)
    rust_func = \
        refine_ffunc(
            RUST_LIB.is_prime_bigint,
            [BIGINT_DIGIT_LIST_C_TYPE],
            c_int32
        )
    rust_result = rust_func(c_array)
    result = int_to_bool(rust_result)
    return result

def is_prime(number: int) -> bool:
    """ Combine the i32 and BigInt methods into one. """
    if number < MAX_I32:
        return is_prime_i32(number)
    return sympy.isprime(number)

def free_string(string_pointer: c_char_p):
    """ Calling this, after having called a Rust function which returns a
    string, prevents memory leaks. """
    rust_func = refine_ffunc(RUST_LIB.free_string, [c_char_p], None)
    rust_func(string_pointer)

def echo_big_integer(big_integer: int) -> int:
    """
    This function passes an arbitrarily large integer to Rust, and then receives
    exactly the same integer back from Rust, and returns that integer.

    Obviously, on its own this serves no earthly purpose, but it might
    demonstrate one means of passing an arbitrarily large integer from Rust
    to Python, which is not straightforward.
    """
    bigint_digit_list, _ = rusticate_int(big_integer)
    c_array = BIGINT_DIGIT_LIST_C_TYPE(*bigint_digit_list)
    rust_func = \
        refine_ffunc(
            RUST_LIB.echo_big_integer,
            [BIGINT_DIGIT_LIST_C_TYPE],
            c_void_p
        )
    raw_pointer = rust_func(c_array)
    string_pointer = cast(raw_pointer, c_char_p)
    result = int(string_pointer.value.decode())
    free_string(string_pointer)
    return result

def nth_prime_i32(ordinal: int) -> int:
    """ Find the nth prime number, provided that it can be represented as in 32
    bits. """
    if ordinal > MAX_PRIME_ORDINAL_I32:
        warnings.warn(
            f"The prime with {ordinal} cannot be represented in 32 bits. "+
            f"The largest prime representable in 32 bits is {MAX_I32}, with "+
            f"ordinal {MAX_PRIME_ORDINAL_I32}."
        )
        return None
    rust_func = refine_ffunc(RUST_LIB.nth_prime_i32, [c_int32], c_int32)
    result = rust_func(ordinal)
    return result

def nth_prime(ordinal: int) -> int:
    """ As above, but for an arbitrarily large ordinal. """
    if ordinal < MAX_PRIME_ORDINAL_I32:
        return nth_prime_i32(ordinal)
    return sympy.ntheory.generate.prime(ordinal)
