"""
This package defines some utility functions, in Rust, which can be called from
Python.
"""

# Local imports.
from .collatz import count_collatz_steps, max_collatz_steps_under
from .combinatorics import factorial
from .primes import is_prime, nth_prime
