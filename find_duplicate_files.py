#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, islink


def get_arguments():
    parser = ArgumentParser(prog='Duplicate Files Finder')
    parser.add_argument('-p', '--path', help='A root directory path')
    return parser.parse_args()


def scan_files(path):
    file_path_names = []
    for root, _, files in walk(path):
        for file_name in files:
            file_path = join(root, file_name)
            if not islink(file_path):
                file_path_names.append(file_path)
    return file_path_names


def main():
    args = get_arguments()
    print(scan_files(args.path))


if __name__ == '__main__':
    main()
