"""
CLI DocString Stub

homework - 3 sub parsers in stdlib_cli.py - commands to move, delete, rename
3 new functions in file_ops.py
use standard libraries for file operations

"""

import argparse

import file_ops

def process_user_input() -> argparse.Namespace:
    """
    blah blah

    """
    parser = argparse.ArgumentParser(
        prog="Advanced Arg Parser",
        description="Tim Wilsons Advanced Argument Parsing Routine",
        epilog="TSW END")

    subcommand_parser = parser.add_subparsers (
        title="Available Commands",
        description="The following sub-commands are available",
        dest="command")
    subcommand_parser.required = True

    copy_parser = subcommand_parser.add_parser(name='copy', help="Copy files.")

    copy_parser.add_argument(
        "-i","--infile",
        nargs="+",
        metavar="In File",
        required=True,
        help="Name or names of file(s) to copy")

    copy_parser.add_argument(
        "-d","--destination",
        metavar="Destination Directory",
        required=True,
        help="Destination to which file(s) are to be copied")

    move_parser = subcommand_parser.add_parser(name='move', help="Move files.")

    move_parser.add_argument(
        "-i","--infile",
        nargs="+",
        metavar="In File",
        required=True,
        help="Name or names of file(s) to move")

    move_parser.add_argument(
        "-d","--destination",
        metavar="Destination Directory",
        required=True,
        help="Destination to which file(s) are to be moved")

    delete_parser = subcommand_parser.add_parser(name='delete', help="Delete files.")

    delete_parser.add_argument(
        "-f","--file",
        nargs="+",
        metavar="File Name",
        required=True,
        help="Name or names of file(s) to be deleted")

#    delete_parser.add_argument(
#        "-d","--directory",
#        metavar="Directory where file(s) are to be deleted",
#        required=True,
#        help="Directory in which file(s) are to be deleted")

    return parser.parse_args()

if __name__ == '__main__':
    program_arguments = process_user_input()

    if program_arguments.command == 'copy':
        file_ops.copy_files(
            program_arguments.infile,
            program_arguments.destination)

    if program_arguments.command == 'move':
        file_ops.move_files (
            program_arguments.infile,
            program_arguments.destination)

    if program_arguments.command == 'delete':
        file_ops.delete_files (
            program_arguments.file)
