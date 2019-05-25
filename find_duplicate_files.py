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


def find_duplicate_files(file_path_names):
    groups = []
    for group in group_files_by_size(file_path_names):
        groups += group_files_by_checksum(group)
    return groups


def compare_two_files(path_1, path_2):
    try:
        buf_size = BUF_SIZE
        with open(path_1, 'rb') as file_1, open(path_2, 'rb') as file_2:
            while True:
                content_1 = file_1.read(buf_size)
                content_2 = file_2.read(buf_size)
                if content_1 != content_2:
                    return False
                if not content_1:
                    return True
    except PermissionError:
        return False


def are_duplicate_files(first_path, second_path):
    if getsize(first_path) == getsize(second_path) and getsize(first_path):
        return compare_two_files(first_path, second_path)
    return False


def find_duplicate_files_faster(file_path_names):
    groups = {}
    while file_path_names:
        temp = file_path_names.pop(0)
        if temp not in groups:
            groups[temp] = [temp]
        length = len(file_path_names)
        index = 0
        while index < length:
            if are_duplicate_files(temp, file_path_names[index]):
                groups[temp].append(file_path_names.pop(index))
                length -= 1
                continue
            index += 1
    return [group for group in groups.values() if len(group) > 1]


def print_output(output):
    if output:
        print(dumps(output, separators=(',\n', '')))


def main():
    start = time()
    args = get_arguments()
    if args.fast:
        print_output(find_duplicate_files_faster(scan_files(args.path)))
    else:
        print_output(find_duplicate_files(scan_files(args.path)))
    print('\nRuntime: {}s'.format(round(time() - start, 5)))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
