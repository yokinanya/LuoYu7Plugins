from nonebot import get_driver
from .config import Config
from webdav4.client import Client


webdav_url = Config.parse_obj(get_driver().config).webdav_url
webdav_username = Config.parse_obj(get_driver().config).webdav_username
webdav_token = Config.parse_obj(get_driver().config).webdav_token

client = Client(base_url=webdav_url, auth=(webdav_username, webdav_token))


def check_exists(cloudpath, detail: bool = False):
    if not client.exists(path=cloudpath):
        client.mkdir(path=cloudpath)
    client.ls(path=cloudpath, detail=detail)


def upload(localpath, cloudpath):
    check_exists(cloudpath)
    client.upload_file(from_path=localpath, to_path=cloudpath, overwrite=True)
