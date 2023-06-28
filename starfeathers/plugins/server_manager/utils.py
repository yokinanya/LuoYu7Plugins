import pathlib
import sys
import os


def delete_folder(folder: str):
    path = get_path(folder)
    del_cmd = f"rm -r {path}"
    os.system(del_cmd)


def get_folder_info(folder: str):
    path = get_path(folder)
    os.chdir(path)
    subinfo_cmd = f'du -h --max-depth=1'  # 查看目录下的子目录的大小
    subinfo = os.popen(subinfo_cmd).read()
    return subinfo


def get_path(folder: str):
    path = pathlib.Path(os.path.abspath(sys.path[0])).joinpath(folder)
    if not path.exists():
        path.mkdir()
    return path
