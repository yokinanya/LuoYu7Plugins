from nonebot import get_driver
from .config import Config
from webdav4.client import Client


webdav_url = Config.parse_obj(get_driver().config).webdav_url
webdav_username = Config.parse_obj(get_driver().config).webdav_username
webdav_token = Config.parse_obj(get_driver().config).webdav_token

client = Client(base_url=webdav_url, auth=(webdav_username, webdav_token))


def ls_folder(t2path: str, detail: bool = False):
    if not client.exists(path=f'/Nonebot/{t2path}'):
        client.mkdir(path=f'/Nonebot/{t2path}')
    client.ls(path=f'/Nonebot/{t2path}', detail=detail)


def upload_file(path, t2path: str, filename: str):
    ls_folder(t2path)
    client.upload_file(from_path=path, to_path=f'/Nonebot/{t2path}/{filename}', overwrite=True)


def download_file(path: str, t2path: str, filename: str):
    client.download_file(from_path=f'/Nonebot/{t2path}/{filename}', to_path=path)


def remove_file(t2path: str, filename: str):
    client.remove(f'/Nonebot/{t2path}/{filename}')
