import shutil
from pathlib import Path
from typing import List

from pyakri_de_utils.file_utils import create_directory


def copy_files_to_dir(files: List[str], dst_dir: str):
    for file in files:
        # file[1:] -> to get the file path without "/"
        dest_file_path = Path(dst_dir, *Path(file).parts[1:])

        create_directory(str(dest_file_path.parent))
        shutil.copy(file, dest_file_path)


def get_file_name_from_path(filepath: str) -> str:
    return Path(filepath).name


def concat_file_paths(*file_path_list) -> str:
    return str(Path(*file_path_list))
