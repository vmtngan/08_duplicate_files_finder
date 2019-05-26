#!/usr/bin/env python3
"""Duplicate Files Finder"""
from argparse import ArgumentParser
from hashlib import md5
from json import dumps
from os import walk
from os.path import join, islink, getsize, abspath, expanduser
from time import time

BUF_SIZE = 8 * 1024


def get_arguments():
    """Parse command-line options, arguments and sub-commands."""
    parser = ArgumentParser(prog='Duplicate Files Finder')
    parser.add_argument('-p', '--path', required=True,
                        help='specify the absolute path where to find '
                             'duplicate files')
    parser.add_argument('-f', '--fast', action='store_true',
                        help='use another method to find duplicate files')
    return parser.parse_args()


def scan_files(path):
    """Search for all the Files.

    @param path: An absolute path.
    @return: A flat list of files (scanned recursively) from the path.
    """
    file_path_names = []
    for root, _, files in walk(path):
        for file_name in files:
            file_path = join(root, file_name)
            # Ignore symbolic links:
            if not islink(file_path):
                file_path_names.append(abspath(file_path))
    return file_path_names


def get_file_checksum(file_path):
    """Generate a Hash Value for a File.

    @param file_path: Absolute path and name of the file.
    @return: The MD5 hash value of the content of this file.
    """
    try:
        with open(file_path, 'rb') as file:
            return md5(file.read()).hexdigest()
    except OSError:
        return None


def group_files(file_path_names, function):
    """Group Files according to a criterion.

    @param file_path_names: The flat list of absolute file path names.
    @param function: The criterion.
    @return: A list of groups (with at least two files) which have
             the same criterion.
    """
    groups = {}
    for file_path in file_path_names:
        file_key = function(file_path)
        if file_key:
            groups.setdefault(file_key, []).append(file_path)
    return [group for group in groups.values() if len(group) > 1]


def group_files_by_size(file_path_names):
    """Group Files by their Size.

    @param file_path_names: The flat list of absolute file path names.
    @return: A list of groups (with at least two files) which have
             the same size.
    """
    return group_files(file_path_names, getsize)


def group_files_by_checksum(file_path_names):
    """Group Files by their Checksum.

    @param file_path_names: The flat list of absolute file path names.
    @return: A list of groups (with at least two files) which have
             the same checksum.
    """
    return group_files(file_path_names, get_file_checksum)


def find_duplicate_files_by_hash(file_path_names):
    """Find all Duplicate Files by md5 hash algorithm.

    @param file_path_names: The list of absolute path and name of files.
    @return: A list of groups that contain duplicate files.
    """
    groups = []
    for group in group_files_by_size(file_path_names):
        groups += group_files_by_checksum(group)
    return groups


def compare_two_files(path_1, path_2):
    """Compare two files.

    @param path_1: First file path.
    @param path_2: Second file path.
    @return: True if the files are the same, False otherwise.
    """
    with open(path_1, 'rb') as file_1, open(path_2, 'rb') as file_2:
        while True:
            content_1 = file_1.read(BUF_SIZE)
            content_2 = file_2.read(BUF_SIZE)
            if content_1 != content_2:
                return False
            if not content_1:
                return True


def are_duplicate_files(path_1, path_2):
    """Check if two files are duplicate.

    @param path_1: First file path.
    @param path_2: Second file path.
    @return: True if the files are duplicate, False otherwise.
    """
    try:
        if getsize(path_1) == getsize(path_2) and getsize(path_1):
            return compare_two_files(path_1, path_2)
        return False
    except PermissionError:
        return False


def get_a_group(file_path_names):
    """Get a duplicate files group.

    @param file_path_names: The list of absolute path and name of files.
    @return: A group that contain duplicate files.
    """
    group = [file_path_names.pop(0)]
    index = 0
    while index < len(file_path_names):
        if not are_duplicate_files(group[0], file_path_names[index]):
            index += 1
            continue
        group.append(file_path_names.pop(index))
    return group, file_path_names


def find_duplicate_files_by_compare(file_path_names):
    """Find all Duplicate Files by comparing algorithm.

    @param file_path_names: The list of absolute path and name of files.
    @return: A list of groups that contain duplicate files.
    """
    groups = []
    while file_path_names:
        group, file_path_names = get_a_group(file_path_names)
        if len(group) > 1:
            groups.append(group)
    return groups


def find_duplicate_files(file_path_names, faster_mode=False):
    """Find all Duplicate Files.

    @param file_path_names: The list of absolute path and name of files.
    @param faster_mode: Use faster method, default is False.
    @return: A list of groups that contain duplicate files.
    """
    if faster_mode:
        return find_duplicate_files_by_compare(file_path_names)
    return find_duplicate_files_by_hash(file_path_names)


def print_output(output):
    """Output a JSON Expression."""
    if output:
        print(dumps(output, separators=(',\n', '')))


def main():
    """Main program."""
    start = time()
    args = get_arguments()
    print_output(
        find_duplicate_files(scan_files(expanduser(args.path)), args.fast))
    print(f'\nRuntime: {round(time() - start, 5)}s')


if __name__ == '__main__':
    try:
        main()
    except OSError as error:
        print(error)
