from datetime import datetime
from fnmatch import filter as py_filter
from glob import glob
from os import listdir, chdir, getcwd, pathsep, mkdir, makedirs, remove
from os import rename as py_rename
from os.path import abspath, basename, dirname, isabs, isdir, isfile, splitext, pathsep, getctime
from os.path import exists as py_exists
from os.path import join as py_join
from shutil import copyfile, copytree, rmtree

from shared.utils.data import not_comment
from shared.utils.first import IsFirst
from shared.utils.strings import not_blank


# Utils ####################################################

def iif(condition, true_value, false_value=None):
    if condition:
        return true_value
    return false_value


# File Names ###############################################

def absolute_path(path):
    return abspath(path)


def absolute_path_or_join(root, path):
    if is_absolute_path(path):
        return path
    return join(root, path)


def absolute_path_or_join_to_parent(root, path):
    if is_absolute_path(path):
        return path
    return join_to_parent(root, path)


def append_name(path, append):
    return to_path_no_extension(path) + append + extension(path)


def base_name(path):
    """ Returns the base name of a file name (filename.ext = filename).
    """
    return splitext(file_name(path))[0]


def directory(path):
    """ Return the directory portion of a file name (dir/dir/filename.ext -> dir/dir)
    """
    return dirname(path)


def extension(path):
    """ Returns the file extension (dir/filename.ext = ext)
    """
    base_name, extension = splitext(path)
    return extension


def file_base_name(path):
    return base_name(path)


def file_dir(path):
    return directory(path)


def file_directory(path):
    return directory(path)


def file_extension(path):
    return extension(path)


def file_name(path):
    """ Returns the full file name from the path (dir/filename.ext -> filename.ext)
    """
    return basename(path)


def file_separator():
    return pathsep


def includes_directory(path):
    """
    Returns true if the file path contains a direcory component.
    dir1/filename = True
    filename = False
    """
    return path != file_name(path)


def join(path, *sub_paths):
    return py_join(path, *sub_paths)


def join_list(root, paths):
    return [join(root, path) for path in paths]


def join_path(path, *sub_paths):
    return py_join(path, *sub_paths)


def join_to_parent(root, path):
    return join(directory(root), path)


def path_separator():
    return pathsep


def prepend_current_directory(name):
    return join(getcwd(), name)


def prepend_cwd(name):
    return prepend_current_directory(name)


def prepend_name(path, prepend):
    return join(to_parent(path), prepend + to_base_name(path))


def replace(path, search, replacement):
    return join(to_parent(path), to_base_name(path).replace(search, replacement))


def set_extension(path, extension):
    return to_path_no_extension(path) + '.' + extension


def strip_extension(path):
    return splitext(path)[0]


def strip_root(path, root):
    if root is None:
        return path

    if root.endswith(file_separator()):
        return path[len(root) + 2:]

    return path[len(root) + 1:]


def strip_roots(paths, root):
    return [strip_root(path, root) for path in paths]


def to_base_name(path):
    return base_name(path)


def to_directory(path):
    return directory(path)


def to_extension(path):
    return extension(path)


def to_file_name(path):
    return file_name(path)


def to_parent(path):
    return directory(path)


def to_path_no_extension(path):
    return strip_extension(path)


# Read Directory ###########################################

def created_date(path):
    return datetime.fromtimestamp(getctime(path))


def current_directory():
    return getcwd()


def dir_exists(dir_path):
    """ Tests if the directory exists and is in fact a directory
    """
    return isdir(dir_path)


def directories_only(path, files):
    return [file for file in files if isdir(join(path, file))]


def directory_paths_only(files):
    return [file for file in files if isdir(file)]


def exists(path):
    return py_exists(path)


def file_exists(path):
    return exists(path)


def files_only(path, files):
    return [file for file in files if isfile(join(path, file))]


def file_paths_only(files):
    return [file for file in files if isfile(file)]


def is_absolute_path(path):
    return isabs(path)


def is_directory(path):
    return isdir(path)


def is_file(path):
    return isfile(path)


def is_relative_path(path):
    return not isabs(path)


def not_directory(path):
    return not dir_exists(path)


def not_file(path):
    return not file_exists(path)


def read_all(path, filter=None):
    """
    Reads all filed and directories in the path.
    Returns the file names.
    """
    if filter:
        return py_filter(listdir(path), filter)
    return listdir(path)


def read_all_paths_recursively(path, filter=None):
    """
    Returns all files recursively.
    Returns the full file paths.
    """
    if filter is None:
        filter = "*"
    return glob(join(path, "**", filter), recursive=True)


def read_all_recursively(path, filter=None):
    return strip_roots(read_all_paths_recursively(path, filter), path)


def read_directories(path, filter=None):
    """
    Return directory names only.
    """
    return directories_only(path, read_all(path, filter))


def read_directory(path, filter=None):
    """ Returns all files and directory names.
    """
    return read_all(path, filter)


def read_directory_names(path, filter=None):
    """ Return directory names only.
    """
    return read_directories(path, filter)


def read_directory_paths(path, filter=None):
    """ Read directories only and return their full paths.
    """
    return join_list(path, read_directories(path, filter))


def read_files(path, filter=None):
    """ Return directory file only.
    """
    return files_only(path, read_all(path, filter))


def read_file_names(path, filter=None):
    """ Return directory files only.
    """
    return read_files(path, filter)


def read_file_paths(path, filter=None):
    """ Read directory files only and return their full paths.
    """
    return join_list(path, read_files(path, filter))


def read_latest_file(path, filter=None):
    """ Returns the file with the latest time-stamp.
    """
    return file_name(
        max(read_file_paths(path, filter), key=getctime))


# File IO ##################################################

def change_directory(path):
    chdir(path)


def read_lines(path):
    with open(path, 'r') as file:
        return [line.rstrip('\n') for line in file]


def read_lines_ignore_blanks_comments(path):
    return [line for line in read_lines(path)
            if not_comment(line) and not_blank(line)]


def read_text(path):
    with open(path, 'r') as file:
        return file.read()


def write_empty_file(path):
    with open(path, 'w') as file:
        pass


def write_lines(path, lines):
    with open(path, 'w') as file:

        first = IsFirst()

        for line in lines:

            if first.not_first():
                file.write('\n')

            file.write(line)


def write_text(path, text):
    with open(path, 'w') as file:
        file.write(text)


# File Operations ##########################################

def create_directory(path):
    mkdir(path)


def create_path(path):
    makedirs(path, exist_ok=True)


def copy(source, destination):
    if is_directory(source):
        copytree(source, destination)
    else:
        copyfile(source, destination)


def delete(path, filter=None):
    """ No fuss file / dir delete command.
		Wouldn't throw an error if it does not exist.
		Will delete it no matter what it is.
	"""
    if filter:
        [delete(join(path, file)) for file in read_all(path, filter)]

    elif file_exists(path):
        if is_directory(path):
            rmtree(path)
        else:
            remove(path)


def delete_directory(path):
    if file_exists(path):
        rmtree(path)


def delete_file(path):
    if file_exists(path):
        remove(path)


def move(source, destination):
    py_rename(source, destination)


def rename(current, new):
    py_rename(current, new)
