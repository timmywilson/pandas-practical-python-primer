"""This module provides various functions for operating on files

Functions:
    copy_files: copy file(s) to a specified location

"""

import subprocess


def copy_files(files: list, destination: str):
    """
    Copy files to a given destination

    Args:
        files: a list of files to copy
        destination: a string designating the destination for the copied files
    """
    for file in files:
        try:
            result = subprocess.check_output(           # subprocess is a function of python
                args=['cp', '-vp', file, destination],  # defining the arguments
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            # source file does not exist
            if "cannot stat" in error.output.decode():
                print("Error: '{}' doesn't exist'".format(file))
            # trying to copy to non-existent directory
            elif "Not a directory" in error.output.decode():
                print("Error: Non-Existent Target Directory '{}' ".format(destination))
                #print("Error: '{destination}' does not exist ".format(
                #    file=file, directory=destination))
            # try to copy to directory w/o access rights
            elif "Permission denied" in error.output.decode():
                #print("Error: No Rights to Write to '{}' ".format(destination))
                print("Error: No Rights to Copy '{file}' to '{directory}' ".format(
                    file=file, directory=destination))
            # catchall
            else:
                print(error.output.decode())
                raise
        else:
            print(
                result.decode(
                    encoding='utf-8').rstrip())
        #finally:
        #    print("I get executed regardless of what happens")

def move_files(files: list, destination: str):
    """
    Move files to a given destination

    Args:
        files: a list of files to move
        destination: a string designating the destination for the moved files
    """
    for file in files:
        try:
            result = subprocess.check_output (           # subprocess is a function of python
                args=['mv', '-v', file, destination],  # defining the arguments
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            if "cannot stat" in error.output.decode():
                print("Error: '{}' doesn't exist'".format(file))
            elif "Not a directory" in error.output.decode():
                print("Error: Non-Existent Target Directory '{}' ".format(destination))
            elif "Permission denied" in error.output.decode():
                print("Error: No Rights to Move '{file}' to '{directory}' ".format(
                    file=file, directory=destination))
            else:
                print(error.output.decode())
                raise
        else:
            print(
                result.decode(
                    encoding='utf-8').rstrip())

#def delete_files(files: list, directory: str):
def delete_files(files: list):
    """
    Delete files

    Args:
        files: a list of files to be deleted
    """
    for file in files:
        try:
            result = subprocess.check_output (           # subprocess is a function of python
                args=['rm', '-v', file],  # defining the arguments
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            if "cannot stat" in error.output.decode():
#                print("Error: '{}' doesn't exist'".format(file))
#            elif "Not a directory" in error.output.decode():
                print("Error: Non-Existent File '{}' ".format(file))
            elif "Permission denied" in error.output.decode():
                print("Error: No Rights to Delete '{file}' ".format(
                    #file=file, directory=directory))
                    file=file))
            else:
                print(error.output.decode())
                raise
        else:
            print(
                result.decode(
                    encoding='utf-8').rstrip())

def parse_args():
    pass