/*
This code some COMBINATORIC functions that use GMP, a C library for working
with large integers.
*/

/* Standard imports. */
#include <stdio.h>
#include <stdlib.h>

/* Non-standard imports. */
#include <gmp.h>

/* Local constants. */
#define BASE 10

/***************************
 ** FOR INTERNAL USE ONLY **
 **************************/

/* Calculates n!, and sends the result to the second parameter. */
void _factorial(mpz_t result, int n) {
    mpz_fac_ui(result, (unsigned long int) n);
}

/*************
 ** EXPORTS **
 ************/

/* Reassure an external user that they can indeed access this library. */
void make_contact(int integer) {
    printf("Congratulations! You've hit the COMBINATORICS library.\n");
    printf("This is the integer you gave me: %d\n", integer);
}

/* Calculates n!, and returns the result as a string. */
char *factorial(int n) {
    char *result;
    mpz_t result_mpz;

    mpz_init(result_mpz);
    _factorial(result_mpz, n);
    result = mpz_get_str(NULL, BASE, result_mpz);
    mpz_clear(result_mpz);

    return result;
}

/* Ronseal. */
void free_string(char *str_ptr) {
    free(str_ptr);
}

/*****************
 ** ENTRY POINT **
 ****************/

/* The entry-point function. */
int main(void) {
    return 0;
}
