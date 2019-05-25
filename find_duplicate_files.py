#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, islink, getsize, abspath
from hashlib import md5
from json import dumps
from time import time
BUF_SIZE = 8 * 1024


def get_arguments():
    parser = ArgumentParser(prog='Duplicate Files Finder')
    parser.add_argument('-p', '--path', help='specify the absolute path '
                                             'where to find duplicate files')
    parser.add_argument('-f', '--fast', action='store_true',
                        help='use another method to find duplicate files')
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


def find_duplicate_files_by_hash(file_path_names):
    groups = []
    for group in group_files_by_size(file_path_names):
        groups += group_files_by_checksum(group)
    return groups


def compare_two_files(path_1, path_2):
    with open(path_1, 'rb') as file_1, open(path_2, 'rb') as file_2:
        while True:
            content_1 = file_1.read(BUF_SIZE)
            content_2 = file_2.read(BUF_SIZE)
            if content_1 != content_2:
                return False
            if not content_1:
                return True


def are_duplicate_files(path_1, path_2):
    try:
        if getsize(path_1) == getsize(path_2) and getsize(path_1):
            return compare_two_files(path_1, path_2)
        return False
    except PermissionError:
        return False


def get_one_group(file_path_names):
    group = [file_path_names.pop(0)]
    index = 0
    while index < len(file_path_names):
        if not are_duplicate_files(group[0], file_path_names[index]):
            index += 1
            continue
        group.append(file_path_names.pop(index))
    return group, file_path_names


def find_duplicate_files_by_compare(file_path_names):
    groups = []
    while file_path_names:
        group, file_path_names = get_one_group(file_path_names)
        if len(group) > 1:
            groups.append(group)
    return groups


def find_duplicate_files(file_path_names, faster_mode=False):
    if faster_mode:
        return find_duplicate_files_by_compare(file_path_names)
    return find_duplicate_files_by_hash(file_path_names)


def print_output(output):
    if output:
        print(dumps(output, separators=(',\n', '')))


def main():
    start = time()
    args = get_arguments()
    print_output(find_duplicate_files(scan_files(args.path), args.fast))
    print(f'\nRuntime: {round(time() - start, 5)}s')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
