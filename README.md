# Duplicate Files Finder
### Core
## Introduction
We often download or copy a lot of crap from different sources, and sometimes we accidentally store the same files multiple times in different folders on our computer.

This is where the mess begins.

```bash
> find . -name "*.jpg" -exec stat -f '%z %N' $PWD/{} \;
3083 /home/botnet/downloads/heobs/archive.csv
309753 /home/botnet/downloads/heobs/GL0625.jpg
483520 /home/botnet/downloads/heobs/GL0701.jpg
309753 /home/botnet/downloads/heobs/GL1240.jpg
309753 /home/botnet/downloads/heritagego/GL0625.jpg
483520 /home/botnet/downloads/heritagego/GL0701.jpg
627451 /home/botnet/downloads/heritagego/GL0803.jpg
309753 /home/botnet/downloads/heritagego/GL1240.jpg
```
Some files may have been copied several times in different locations with different names.

For instance:

```bash
309753 /home/botnet/downloads/heobs/GL0625.jpg
309753 /home/botnet/downloads/heobs/GL1240.jpg
309753 /home/botnet/downloads/heritagego/GL0625.jpg
309753 /home/botnet/downloads/heritagego/GL1240.jpg
```
We need to find duplicate files that have the same content but not necessarily the same name.

Your mission is to write a **Command-Line Interface (CLI)** (https://en.wikipedia.org/wiki/Command-line_interface) Python script that will output a list of duplicate files identified by their absolute path and name.

## Waypoint 1: Write a Python Script Skeleton
Write a minimal Python executable script `find_duplicate_files.py` that takes one mandatory argument `-p` or `--path` (which identifies the root directory) to start scanning for duplicate files.

#### Example
```bash
$ ./find_duplicate_files.py --path ~/whatever-directory
```

#### Note
You MUST use the Python standard module **argparse** (https://docs.python.org/3/library/argparse.html) to parse command-line options, arguments and sub-commands.

## Waypoint 2: Search for all the Files
Write a function `scan_files` that takes one argument `path` (which corresponds to an absolute path) and returns a flat list of files (scanned recursively) from the specified path.

Each file must be identified by its absolute path name.

#### Example
```bash
>>> scan_files('~/downloads')
['/home/botnet/downloads/heobs/archive.csv',
'/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heobs/GL0701.jpg',
'/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL0701.jpg',
'/home/botnet/downloads/heritagego/GL0803.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg]
```

#### Note
You MUST use the Python function **os.walk** (https://docs.python.org/3/library/os.html#os.walk) to retrieve the list of files in every directory of the tree root `path`.

_Note: the function **scan_files** MUST ignore symbolic links that resolve to directories and files._

## Waypoint 3: Group Files by their Size
Duplicate files have the same size.

Write a function `group_files_by_size` that takes one mandatory argument `file_path_names` (which corresponds to a flat list of absolute file path names) and returns a list of groups (with at least two files) which have the same size.

You MUST ignore empty files (i.e. `0` bytes).

#### Example
```bash
>>> file_path_names = [
'/home/botnet/downloads/heobs/archive.csv',
'/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heobs/GL0701.jpg',
'/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL0701.jpg',
'/home/botnet/downloads/heritagego/GL0803.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg']
>>> group_files_by_size(file_path_names)
[['/home/botnet/downloads/heobs/GL0701.jpg',
'/home/botnet/downloads/heritagego/GL0701.jpg'],
['/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg',
'/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg']]
```

## Waypoint 4: Generate a Hash Value for a File
The content of a file can be reduced to a **checksum** (https://en.wikipedia.org/wiki/Checksum) (hash), also known as a message digest.

The actual procedure which yields the checksum from the file's content is called a checksum function or **checksum algorithm** (https://en.wikipedia.org/wiki/Cryptographic_hash_function).

There are many cryptographic hash algorithms. The **MD5 message-digest algorithm** (https://en.wikipedia.org/wiki/MD5) is a widely used hash function that produces a 128-bit hash value. The MD5 algorithm can be used to generate a compact digital fingerprint of a file.

Files that have the same content are identified with the same hash value.

#### Note
It is very unlikely that any two non-identical files in the real world will have the same MD5 hash.

#### Example
Write a function `get_file_checksum` that takes one mandatory argument `file_path_name` (which corresponds to the absolute path and name of a file) and returns the MD5 hash value of the content of this file.

```bash
>>> get_file_checksum('/home/botnet/downloads/heobs/GL0625.jpg')
'dd23819ce306f0f1476522c9ce3e0a07'
```

#### Note
You MUST use the Python module **hashlib** (https://docs.python.org/3/library/hashlib.html) to generate the hash value of a file's content.

## Waypoint 5: Group Files by their Checksum
Write a function `group_files_by_checksum` that takes one argument `file_path_names` (which corresponds to a flat list of the absolute path and name of files) and returns a list of groups that contain duplicate files.

#### Example
This function `group_duplicate_files` MUST use the function `get_file_checksum` to detect duplicate files.

```bash
>>> file_path_names = [
'/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg',
'/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg']
>>> group_files_by_checksum(file_path_names)
[['/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg'],
['/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg']]
```

#### Note
Yes, this function will be passed a list of files of the same size (i.e., possible duplicate files). So, it would not be optimal to pass a list of files with different sizes.

## Waypoint 6: Find all Duplicate Files
Write a function `find_duplicate_files` that takes one mandatory argument `file_path_names` (which corresponds to a list of absolute path and name of files) and returns a list of groups that contain duplicate files.

#### Example
```bash
>>> file_path_names = ['/home/botnet/downloads/heobs/GL0701.jpg',
'/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heobs/archive.csv',
'/home/botnet/downloads/heritagego/GL0701.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL0803.jpg']
>>> find_duplicate_files(file_path_names)
[['/home/botnet/downloads/heobs/GL0701.jpg',
'/home/botnet/downloads/heritagego/GL0701.jpg'],
['/home/botnet/downloads/heobs/GL0625.jpg',
'/home/botnet/downloads/heritagego/GL0625.jpg'],
['/home/botnet/downloads/heobs/GL1240.jpg',
'/home/botnet/downloads/heritagego/GL1240.jpg']]
```

#### Note
This function `find_duplicate_files` MUST use the two previous functions `group_files_by_size` and `group_files_by_checksum`.

## Waypoint 7: Output a JSON Expression
Complete your Python script by writing, on the standard output, a JSON expression corresponding to the list of duplicate files.

#### Example
```bash
$ ./find_duplicate_files.py --path ~/downloads
[["/home/botnet/downloads/heobs/GL0701.jpg",
"/home/botnet/downloads/heritagego/GL0701.jpg"],
["/home/botnet/downloads/heobs/GL0625.jpg",
"/home/botnet/downloads/heritagego/GL0625.jpg"],
["/home/botnet/downloads/heobs/GL1240.jpg",
"/home/botnet/downloads/heritagego/GL1240.jpg"]]
```

#### Note
You MUST use the Python module **json** (https://docs.python.org/3/library/json.html) to serialize the list of duplicate files to a JSON formatted string.

---
### Bonus
## Waypoint 8: Performance Optimization (Bonus)
Find another method to find duplicate files that would be much faster than using a hash algorithm.

#### Note
You CANNOT directly use the **filecmp** (https://docs.python.org/3/library/filecmp.html) Python module – it would have been too easy! – but you are definitively allowed to be inspired by this module.

---
### TOOL - Duplicate Files Generator
#### Content
We provide a Python CLI script that generates duplicate files of random sizes to help you in testing your code.

This script supports several options. Type `-h` or `--help` to get a list of available options.

```bash
$ ./generate_duplicate_files.py --help
usage: generate_duplicate_files.py [-h] --file-count PATH [-p filename]
                                   [--directory-min-depth DIRECTORY_MIN_DEPTH]
                                   [--directory-max-depth DIRECTORY_MAX_DEPTH]
                                   [--duplicate-file-ratio DUPLICATE_FILE_RATIO]
                                   [--file-extensions FILE_EXTENSIONS]
                                   [--file-extension-min-length FILE_EXTENSION_MIN_LENGTH]
                                   [--file-extension-max-length FILE_EXTENSION_MAX_LENGTH]
                                   [--file-name-min-length FILE_NAME_MIN_LENGTH]
                                   [--file-name-max-length FILE_NAME_MAX_LENGTH]
                                   [--file-min-size FILE_MIN_SIZE]
                                   [--file-max-size FILE_MAX_SIZE]

Duplicate Files Generator

optional arguments:
  -h, --help            show this help message and exit
  --file-count PATH     specify the number of files to generate
  -p filename, --path filename
                        specify the absolute path where to generate files
  --directory-min-depth DIRECTORY_MIN_DEPTH
                        specify the maximum number of sub-directories to
                        generate a file from the specified root path
  --directory-max-depth DIRECTORY_MAX_DEPTH
                        specify the maximum number of sub-directories to
                        generate a file from the specified root path
  --duplicate-file-ratio DUPLICATE_FILE_RATIO
                        specify the ratio of duplicate files to be generated
  --file-extensions FILE_EXTENSIONS
                        specify a comma-separated values of file extension to
                        be used when generate files (e.g., "gif,jpg,mp3")
  --file-extension-min-length FILE_EXTENSION_MIN_LENGTH
                        specify the minimum length of a file extension to
                        randomly generate
  --file-extension-max-length FILE_EXTENSION_MAX_LENGTH
                        specify the maximum length of a file extension to
                        randomly generate
  --file-name-min-length FILE_NAME_MIN_LENGTH
                        specify the minimum length of a file name to randomly
                        generate
  --file-name-max-length FILE_NAME_MAX_LENGTH
                        specify the maximum length of a file name to randomly
                        generate
  --file-min-size FILE_MIN_SIZE
                        specify the minimum size of a file to randomly
                        generate
  --file-max-size FILE_MAX_SIZE
                        specify the maximum size of a file to randomly
                        generate
```

#### Example
For example, let's say you would like to generate 10,000 files in a root directory `test`, with 30% of these files duplicated, you simply need to enter the following command:
```bash
$ ./generate_duplicate_files.py --file-count 10000 --duplicate-file-ratio 0.3 --path test
```

:page_facing_up: [generate_duplicate_files.py](/generate_duplicate_files.py)
