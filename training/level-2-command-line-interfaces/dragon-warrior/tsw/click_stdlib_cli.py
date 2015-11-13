"""
CLI DocString Stub

homework - 3 sub parsers in stdlib_cli.py - commands to move, delete, rename
3 new functions in file_ops.py
use standard libraries for file operations

"""

import click

import file_ops


@click.command()
@click.argument('infile',nargs=-1)
@click.argument('destination',nargs=1)
def _copy_files(infile, destination):
    file_ops.copy_files(infile, destination)
    """
    blah blah

    """

def _move_files(infile, destination):
    file_ops.move_files(infile, destination)
    """
    blah blah

    """


if __name__ == '__main__':
    _copy_files()

    _move_files()
