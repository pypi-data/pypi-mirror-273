import os
import urllib
import pathlib as paths
from maat_machine.pprint import displayitwell


def print_path_info(path: paths.Path, path_title: str = 'Path'):
    displayitwell(f"{path_title}: \"{path}\"; Absolute: \"{path.absolute()}\"", font_style='oblique', font_weight='bold')


def directory_exists(directory_path: paths.Path):
    return directory_path.exists() and directory_path.is_dir()


def make_directory(directory_path: paths.Path, print_info: bool = True, path_comment: str = ''):
    assert isinstance(directory_path, paths.Path)
    assert directory_path is not None
    if not directory_exists(directory_path):
        directory_path.mkdir(parents=True, exist_ok=True)
    if print_info:
        print_path_info(directory_path, path_comment)


def make_directories(directory_paths: list, print_info: bool = True, path_comment: str = ''):
    assert all(isinstance(path, paths.Path) for path in directory_paths)
    for directory_path in directory_paths:
        make_directory(directory_path, print_info=print_info, path_comment=path_comment)


def make_directories_in_parent(directory_paths: list, parent_directory: paths.Path, print_info: bool = True, path_comment: str = ''):
    assert all(isinstance(path, paths.PurePath) for path in directory_paths)
    assert isinstance(parent_directory, paths.Path)
    new_directory_full_paths = []
    for directory_path in directory_paths:
        new_directory_full_path = parent_directory.joinpath(directory_path)
        make_directory(new_directory_full_path, print_info=print_info, path_comment=path_comment)
        new_directory_full_paths.append(new_directory_full_path)
    return new_directory_full_paths


def list_directory(directory: paths.Path, list_paths: bool = False, sort: bool = True):
    assert directory.is_dir()
    file_list = [(item if list_paths else item.name) for item in directory.iterdir()]
    return sorted(file_list) if sort else file_list


def extract_file_info_from_url(url):
    parsed_url = urllib.parse.urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    file_name_without_extension, file_extension = os.path.splitext(file_name)
    return file_name, file_name_without_extension, file_extension
