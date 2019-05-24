#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, islink, getsize
from hashlib import md5
from json import dumps
from time import time


def get_arguments():
    parser = ArgumentParser(prog='Duplicate Files Finder')
    parser.add_argument('-p', '--path', help='specify the absolute path '
                                             'where to find duplicate files')
    return parser.parse_args()


def scan_files(path):
    list_of_file_paths = []
    for root, _, files in walk(path):
        for file_name in files:
            file_path = join(root, file_name)
            if not islink(file_path):
                list_of_file_paths.append(file_path)
    return list_of_file_paths


def group_files_by_size(list_of_file_paths):
    groups = {}
    for file_path in list_of_file_paths:
        file_size = getsize(file_path)
        if not file_size:
            continue
        groups[file_size] = groups.get(file_size, []) + [file_path]
    return [group for group in groups.values() if len(group) > 1]


def get_file_checksum(file_path):
    try:
        with open(file_path, 'rb') as file:
            return md5(file.read()).hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def group_files_by_checksum(list_of_file_paths):
    groups = {}
    for file_path in list_of_file_paths:
        file_checksum = get_file_checksum(file_path)
        if not file_checksum:
            continue
        groups[file_checksum] = groups.get(file_checksum, []) + [file_path]
    return [group for group in groups.values() if len(group) > 1]


def find_duplicate_files(list_of_file_paths):
    return


def print_output(output):
    print(dumps(output, separators=(',\n', '')))


def main():
    args = get_arguments()
    list_of_file_paths = scan_files(args.path)
    groups_by_size = group_files_by_size(list_of_file_paths)
    groups_by_checksum = group_files_by_checksum(list_of_file_paths)


if __name__ == '__main__':
    start = time()
    main()
    print('\nRuntime: {}s'.format(round(time() - start, 5)))
