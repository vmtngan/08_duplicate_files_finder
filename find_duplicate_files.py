#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, islink, getsize
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
                file_path_names.append(file_path)
    return file_path_names


def group_files_by_size(file_path_names):
    groups = {}
    for file_path in file_path_names:
        file_size = getsize(file_path)
        if file_size:
            groups.setdefault(file_size, []).append(file_path)
    return [group for group in groups.values() if len(group) > 1]


def get_file_checksum(file_path):
    try:
        with open(file_path, 'rb') as file:
            return md5(file.read()).hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def group_files_by_checksum(file_path_names):
    groups = {}
    for file_path in file_path_names:
        file_checksum = get_file_checksum(file_path)
        if file_checksum:
            groups.setdefault(file_checksum, []).append(file_path)
    return [group for group in groups.values() if len(group) > 1]


def find_duplicate_files(file_path_names):
    return [group_files_by_checksum(group)
            for group in group_files_by_size(file_path_names)]


def print_output(output):
    print(dumps(output, separators=(',\n', '')))


def main():
    args = get_arguments()
    print_output(find_duplicate_files(scan_files(args.path)))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
