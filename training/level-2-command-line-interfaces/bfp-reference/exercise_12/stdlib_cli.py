"""
This module provides a CLI allows users to perform a variety of
file related tasks.
"""
import argparse

import file_ops


def process_user_input() -> argparse.Namespace:
    """
    Process input from the command line and return the results.

    Returns:
        A argparse.Namespace object containing the
        results of parsing the command line input.
    """
    parser = argparse.ArgumentParser(
        prog="Who Needs Bash?",
        description="My cool program does a lot of cool things with files.",
        epilog="Thanks for using my cool program.")

    subcommand_parsers = parser.add_subparsers(
        title="Available Commands",
        description="The following sub-commands are available.",
        dest="command")
    subcommand_parsers.required = True

    # Copy Command Subparser
    copy_parser = subcommand_parsers.add_parser(name='copy', help="Copy Files")
    copy_parser.add_argument(
        "-f", "--filenames", nargs="+", metavar="FILENAME",
         required=True, help="Names of files to copy.")

    copy_parser.add_argument(
        '-d', '--destination', required=True,
        help='Location to copy files to.')

    # Move Command Subparser
    move_parser = subcommand_parsers.add_parser(name='move', help="Move Files")

    move_parser.add_argument(
        "-f", "--filenames", nargs="+", metavar="FILENAME",
        required=True, help="Names of files to move.")

    move_parser.add_argument(
        '-d', '--destination', required=True,
        help='Location to copy files to.')

    delete_parser = subcommand_parsers.add_parser(
        name='delete', help="Delete Files")
    delete_parser.add_argument(
        "-f", "--filenames", nargs="+", metavar="FILENAME",
        required=True, help="Names of files to delete.")

    rename_parser = subcommand_parsers.add_parser(
        name='rename', help="Rename Files")
    rename_parser.add_argument(
        "-f", "--filenames", nargs="+", metavar="FILENAME",
        required=True, help="Names of files to rename.")
    rename_parser.add_argument(
        "-n", "--new-filenames", nargs="+", metavar="NEW_FILENAME",
        required=True, help="New names for files.")

    return parser.parse_args()


if __name__ == '__main__':
    program_arguments = process_user_input()

    if program_arguments.command == 'copy':
        file_ops.copy_files(
            files=program_arguments.filenames,
            destination=program_arguments.destination)
    elif program_arguments.command == 'move':
        file_ops.move_files(
            filenames=program_arguments.filenames,
            destination=program_arguments.destination)




