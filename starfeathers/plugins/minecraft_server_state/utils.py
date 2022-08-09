import json
from mcstatus import JavaServer
import base64
import re
import uuid
import os
import pathlib
import sys

_local_tmp_resource_folder = pathlib.Path(os.path.abspath(sys.path[0])).joinpath('tmp/mcstate')
if not _local_tmp_resource_folder.exists():
    _local_tmp_resource_folder.mkdir()

def decode_image(src):
    # 1、信息提取
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        pass
    # 2、base64解码
    img = base64.urlsafe_b64decode(data)
    # 3、二进制文件保存
    filename = str(_local_tmp_resource_folder) + "/{}.{}".format(uuid.uuid4(), ext)
    with open(filename, "wb") as f:
        f.write(img)
    return filename


def mcstate(address: str):
    server = JavaServer.lookup(address)
    info = f"IP/域名：{address}\n"
    try:
        status = server.status()
        info = info + f"兼容游戏版本：{status.version.name}\n可容纳最大玩家数:{status.players.max}\n在线玩家数：{status.players.online}"
    except:
        try:
            query = server.query()
            hostip = query.raw["hostip"]
            hostport = query.raw["hostport"]
            info = info + f"主机IP：{hostip}\n端口：{hostport}\nMOTD：{query.motd}\n兼容游戏版本：{query.software.version}\n服务器使用的软件或核心：{query.software.brand}\n可容纳最大玩家数:{query.players.max}\n在线玩家数：{query.players.online}"
        except:
            info = "服务器状态：离线"
    try:
        players = status.raw["players"]["sample"]
        list = []
        for i in players:
            list.append(i["name"])
        list = ', '.join(list)
        info = info + f"\n当前在线玩家：\n{list}"
    except:
        try:
            info = info + f"\n当前在线玩家：\n{', '.join(query.players.names)}"
        except:
            pass
    return info


def get_favicon(address: str):
    server = JavaServer.lookup(address)
    favicon = server.status().favicon
    return favicon

def get_ip(groupid: int, serverip: str):
    with open(serverip, "r", encoding="utf-8") as serverips:
        ipdata = json.load(serverips)
        ip = ipdata[str(groupid)]
        serverips.close()
    return ip


def read_data(serverip: str):
    with open(serverip, "r", encoding="utf-8") as serverips:
        ipdata = json.load(serverips)
        serverips.close()
    return ipdata


def write_data(ipdata: dict, serverip: str):
    with open(serverip, "w", encoding="utf-8") as serverips:
        json.dump(ipdata, serverips)
        serverips.close()
