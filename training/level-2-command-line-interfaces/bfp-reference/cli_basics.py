"""
Insert docstring here.
"""
import argparse
import subprocess


def process_user_input() -> argparse.Namespace:
    """
    Process input from the command line and return the results.

    Returns:
        argparse.Namespace: A dictionary-like object containing the
        results of parsing the command line input.
    """
    parser = argparse.ArgumentParser(description="This programs copies files.",
                                     epilog="This programs copies files in "
                                            "case you forgot.")

    parser.add_argument(dest='filenames', metavar='filename',
                        nargs='+', help="All the files to copy.")

    parser.add_argument('-d', '--destination', required=True,
                        dest='destination', help='Location to copy files to.')

    parser.add_argument('-n', '-newnames', dest='new_filenames',
                        metavar='new-filename', nargs='+',
                        help="New filenames for copied files.")

    return parser.parse_args()


def copy_files(files: list, destination: str, new_filenames: list=None):
    """
    Copy files to a given destination.

    First attempt to copy the file while maintaining current permissions.
    If this fails, it attempt to copy without maintaining permissions.

    """

    for file in files:

        if new_filenames is not None:
            try:
                file_destination = "{}/{}".format(
                    destination, new_filenames[files.index(file)])
            except IndexError:
                print("No matching new name found for file: {}".format(file))
                continue
        else:
            file_destination = destination

        operation_result = subprocess.check_output(
            args=['cp', '-vp', file, file_destination],
            stderr=subprocess.STDOUT)

        print(operation_result.decode('utf-8').strip('\n'))


if __name__ == "__main__":
    cli_arguments = process_user_input()
    copy_files(files=cli_arguments.filenames,
               destination=cli_arguments.destination,
               new_filenames=cli_arguments.new_filenames)