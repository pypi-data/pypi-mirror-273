/// This library defines some utility functions for anyone working with the
/// Collatz conjecture.

/***************************
 ** FOR INTERNAL USE ONLY **
 **************************/

/// Given an integer, return the next item in the Collatz sequence.
fn next_collatz(n: i64) -> i64 {
    let result: i64;

    if n%2 == 0 {
        result = n/2;
    } else {
        result = (3*n)+1;
    }

    return result;
}

/****************
 ** FOR EXPORT **
 ***************/

/// Reassure an external user that they can indeed access this library.
#[no_mangle]
pub extern fn make_contact(int: i32) {
    println!("Congratulations! You've made contact with the COLLATZ library.");
    println!("This is the integer you gave me: {}", int);
}

/// Count the number of Collatz steps required to reach 1, given a starting
/// point.
#[no_mangle]
pub extern fn count_collatz_steps(n: i32) -> i32 {
    let mut result: i32 = 0;
    let mut current: i64 = n.into();

    while current != 1 {
        result += 1;
        current = next_collatz(current);
    }

    return result;
}

/// Find the maximum number of Collatz steps required to reach 1, if one uses
/// all the numbers between 1 and a given limit (inclusive) as starting points.
#[no_mangle]
pub extern fn max_collatz_steps_under(limit: i32) -> i32 {
    let mut result: i32 = 0;
    let mut current_max: i32 = 0;
    let mut current_steps: i32;

    for n in 1..=limit {
        current_steps = count_collatz_steps(n);

        if current_steps > current_max {
            current_max = current_steps;
            result = n;
        }
    }

    return result;
}
