#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, islink, getsize, abspath
from hashlib import md5
from json import dumps


def get_arguments():
    parser = ArgumentParser(prog='Duplicate Files Finder')
    parser.add_argument('-p', '--path', help='specify the absolute path '
                                             'where to find duplicate files')
    return parser.parse_args()


def scan_files(path):
    file_path_names = []
    for root, _, files in walk(path):
        for file_name in files:
            file_path = join(root, file_name)
            if not islink(file_path):
                file_path_names.append(abspath(file_path))
    return file_path_names


def get_file_checksum(file_path):
    try:
        with open(file_path, 'rb') as file:
            return md5(file.read()).hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def group_files(file_path_names, function):
    groups = {}
    for file_path in file_path_names:
        file_key = function(file_path)
        if file_key:
            groups.setdefault(file_key, []).append(file_path)
    return [group for group in groups.values() if len(group) > 1]


def group_files_by_size(file_path_names):
    return group_files(file_path_names, getsize)


def group_files_by_checksum(file_path_names):
    return group_files(file_path_names, get_file_checksum)


def find_duplicate_files(file_path_names):
    groups = []
    for group in group_files_by_size(file_path_names):
        groups += group_files_by_checksum(group)
    return groups


def print_output(output):
    if output:
        print(dumps(output, separators=(',\n', '')))


def main():
    args = get_arguments()
    print_output(find_duplicate_files(scan_files(args.path)))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
