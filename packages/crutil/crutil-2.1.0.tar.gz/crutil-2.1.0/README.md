# CRUtil: C and Rust Utilities for Python

This code defines a library of C and Rust functions, and a Python middleman from which to call those functions. It is modelled on the `shutil` module from the Python standard library.

## Installation

Note that this package is designed for Debian-based Linux platforms only. Some portions of it may well work on other platforms, but you do so at your own risk. The instructions below assume that your system already has the GNU C Compiler, and that you have access to the `gcc` command.

### Installing the Python Code

* ~~If you're installing remotely, **`pip install crutil`** should do the trick.~~
* If, on the other hand, you're installing locally, then use **`pip install .`** from this directory.

### Compiling the C and Rust Libraries

By installing the PIP package as described above, you will also have installed the commands `crutil-install` and `crutil-compile`. Run `crutil-install` first - this installs Cargo and GMP, but even if you already have these it shouldn't do any harm - then run `crutil-compile` - this compiles the C and Rust code into binaries which your machine can execute. Running those two commands completes the installation process.

## Examples

### Primes

This code should find whether a nine-digit number is prime or not - and do so far quicker than anything in pure Python:

```python
from crutil.primes import is_prime_i32

def run():
    print(is_prime_i32(188888881))

if __name__ == "__main__":
    run()
```
