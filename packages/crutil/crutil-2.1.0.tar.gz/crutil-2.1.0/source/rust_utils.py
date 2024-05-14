"""
This code defines some functions for working with Rust directly.
"""

# Standard imports.
import subprocess
import warnings
from ctypes import CDLL
from pathlib import Path

# Local constants.
PATH_OBJ_TO_RUST_PACKAGES_DIR = Path(__file__).parent/"rust"
MANIFEST_FILENAME = "Cargo.toml"
BITS = 32
MAX_I32 = (2**31)-1

###########
# CLASSES #
###########

class RUtilTypeMismatch(Exception):
    """ A custom exception. """

class RUtilBadBooleanInteger(Exception):
    """ A custom exception. """

#############
# FUNCTIONS #
#############

def compile_rust_package(path_to_manifest):
    """ Compile the Rust package for the given package. """
    args = [
        "cargo",
        "build",
        "--manifest-path",
        path_to_manifest,
        "--release"
    ]
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        warnings.warn(
            "There was a problem compiling the Rust package with manifest: "+
            path_to_manifest
        )
        return False
    return True

def compile_rust_packages():
    """ Create executables from the source code. """
    for path_obj in PATH_OBJ_TO_RUST_PACKAGES_DIR.glob("*"):
        if path_obj.is_dir():
            path_to_manifest = str(path_obj/MANIFEST_FILENAME)
            if not compile_rust_package(path_to_manifest):
                return False
    return True

def get_local_rust_library(package_name):
    """ Return a Rust library in a form which Python can use. """
    path_obj_to_package = PATH_OBJ_TO_RUST_PACKAGES_DIR/package_name
    so_filename = "lib"+package_name+".so"
    path_to_so_file = str(path_obj_to_package/"target"/"release"/so_filename)
    try:
        result = CDLL(path_to_so_file)
    except:
        warnings.warn(
            "There was a problem importing the Rust library with .so file: "+
            path_to_so_file
        )
        return None
    return result

def rusticate_int(integer: int) -> tuple[list[int], bool]:
    """ Convert a Python integer into a form that Rust can use. """
    is_non_negative = True
    if integer < 0:
        is_non_negative = False
        integer = integer*-1
    result = []
    bin_string = format(integer, "b")
    right_index = len(bin_string)
    left_index = right_index-BITS
    while left_index >= 0:
        digit_bin_string = bin_string[left_index:right_index]
        result.append(int(digit_bin_string, 2))
        left_index -= BITS
        right_index -= BITS
    if right_index > 0:
        digit_bin_string = bin_string[0:right_index]
        result.append(int(digit_bin_string, 2))
    return result, is_non_negative
