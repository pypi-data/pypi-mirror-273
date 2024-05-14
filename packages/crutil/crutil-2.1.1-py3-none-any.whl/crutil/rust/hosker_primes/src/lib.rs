/// This library defines some utility functions for working with primes.

// Standard imports.
use std::ffi::CString;

// Non-standard imports.
use libc::{c_char, c_void};
use num_bigint_dig::BigUint;
use num_bigint_dig::prime::probably_prime as is_big_prime;
use num_prime::nt_funcs::{
    is_prime64 as is_little_prime,
    nth_prime as _nth_prime
};

// Local constants.
const MAX_DIGITS: usize = 100;
const STANDARD_RADIX: u32 = 10;
const PSEUDORANDOMLY_CHOSEN_BASES: usize = 32;
const TRUE_INT: i32 = 1;
const FALSE_INT: i32 = 0;
const MAX_PRIME_ORDINAL_I32: i32 = 105097565;

/***************************
 ** FOR INTERNAL USE ONLY **
 **************************/

/// Determine whether an arbitrarily large integer is prime.
fn _is_prime_bigint(potential_prime: BigUint) -> bool {
    let result = is_big_prime(&potential_prime, PSEUDORANDOMLY_CHOSEN_BASES);

    return result;
}

/***************
 ** MIDDLEMEN **
 **************/

/// Receive a big integer from outside Rust.
unsafe fn import_bigint(digit_list: PortableDigitList) -> BigUint {
    let digits = Vec::from(*digit_list.array);
    let result = BigUint::new(digits);

    return result;
}

/// Convert a big integer into an exportable form outside Rust.
fn export_bigint(n: BigUint) -> *mut c_char {
    let result_str = n.to_str_radix(STANDARD_RADIX);
    let result = CString::new(result_str).unwrap().into_raw();

    return result;
}

/// Convert a boolean into an integer representation of the same.
fn bool_to_int(boolean: bool) -> i32 {
    if boolean {
        return TRUE_INT;
    }

    return FALSE_INT;
}

/****************
 ** FOR EXPORT **
 ***************/

/// A portable representation of a large integer.
#[repr(C)]
pub struct PortableDigitList {
    array: *const [u32; MAX_DIGITS]
}

/// Reassure an external user that they can indeed access this library.
#[no_mangle]
pub extern fn make_contact(int: i32) {
    println!("Congratulations! You have made contact with the PRIMES library.");
    println!("This is the integer you gave me: {}", int);
}

/// Receive a big integer from outside Rust, and send it back.
#[no_mangle]
pub unsafe extern fn echo_big_integer(
    digit_list: PortableDigitList
) -> *mut c_char {
    let big_integer = import_bigint(digit_list);

    println!("Received big integer: {:?}. Sending it back...", big_integer);

    return export_bigint(big_integer);
}

/// Prevent a memory leak from sending a reference to a C string outside Rust.
#[no_mangle]
pub unsafe extern fn free_string(pointer: *mut c_void) {
    let _ = CString::from_raw(pointer as *mut c_char);
}

/// A wrapper for the similarly-named function above.
#[no_mangle]
pub extern fn is_prime_i32(n: i32) -> i32 {
    return bool_to_int(is_little_prime(n.try_into().unwrap()));
}

/// A wrapper for the similarly-named function above.
#[no_mangle]
pub unsafe extern fn is_prime_bigint(digit_list: PortableDigitList) -> i32 {
    let big_integer = import_bigint(digit_list);

    return bool_to_int(_is_prime_bigint(big_integer));
}

/// A wrapper for the similarly-named function above.
#[no_mangle]
pub extern fn nth_prime_i32(n: i32) -> i32 {
    if n > MAX_PRIME_ORDINAL_I32 {
        println!(
            "WARNING: Prime with ordinal {} cannot be represented in 32 bits.", 
            n
        );

        return 0;
    }

    return _nth_prime(n.try_into().unwrap()) as i32;
}
