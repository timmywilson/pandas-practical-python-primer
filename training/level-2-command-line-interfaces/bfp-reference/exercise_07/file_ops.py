<<<<<<< HEAD:training/level-2-command-line-interfaces/bfp-reference/exercise_7/file_ops.py
"""
This modules provides various functions for operating on files.

Functions:
    copy_files: Copy file(s) to a specified location.
"""

import subprocess


def copy_files(files: list, destination: str):
    """
    Copy files to a given destination.

    Args:
        files: A list of files to copy.
        destination: A str specifying the destination for copied
            files.
    """

    for file in files:
        operation_result = subprocess.check_output(
            args=['cp', '-vp', file, destination],
            stderr=subprocess.STDOUT)

        print(operation_result)
=======
"""
This modules provides various functions for operating on files.

Functions:
    copy_files: Copy file(s) to a specified location.
"""

import subprocess


def copy_files(files: list, destination: str):
    """
    Copy files to a given destination.

    Args:
        files: A list of files to copy.
        destination: A str specifying the destination for copied
            files.
    """

    for file in files:
        operation_result = subprocess.check_output(
            args=['cp', '-vp', file, destination],
            stderr=subprocess.STDOUT)

        print(operation_result)
>>>>>>> upstream/master:training/level-2-command-line-interfaces/bfp-reference/exercise_07/file_ops.py
