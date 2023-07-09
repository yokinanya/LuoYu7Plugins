import json
import os

import requests
import urllib3

from .config import global_config, plugin_config

su = global_config.superusers
api_url = plugin_config.mcsm_api_url
api_key = plugin_config.mcsm_api_key
urllib3.disable_warnings()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

instances_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"instances.json")
)
with open(instances_path, "r") as file:
    # 读取文件内容
    instances = json.load(file)


def instance_controller(operating_options: str, uuid: str, remote_uuid: str):
    url = api_url + f"/api/protected_instance/" + operating_options
    params = {"uuid": uuid, "remote_uuid": remote_uuid, "apikey": api_key}
    req = requests.get(url, params=params, headers=headers, verify=False).json()
    status = req["status"]
    data = req["data"]
    if status == 200:
        operating_options_n = operating_options_name(operating_options)
        data = "实例" + operating_options_n + "成功"
    return status, data


def instance_controller_one(operating_options: str,nickname:str):
    try:
        uuid = instances[nickname]["uid"]
        remote_uuid = instances[nickname]["gid"]
        status, data = instance_controller(operating_options, uuid, remote_uuid)
        server_status_one = nickname + "：" + data
    except KeyError:
        server_status_one = nickname + "：找不到实例"
    except:
        server_status_one = nickname + "：出现未知错误"
    return server_status_one

def instance_controller_all(operating_options: str):
    server_status_all = ""
    for k, v in instances.items():
        nickname = k
        uuid = v["uid"]
        remote_uuid = v["gid"]
        status, data = instance_controller(operating_options, uuid, remote_uuid)
        return_msg = nickname + "：" + data + "\n"
        server_status_all += return_msg
    return server_status_all[:-1]


def check_instance(uuid: str, remote_uuid: str):
    url = api_url + f"/api/instance"
    params = {"uuid": uuid, "remote_uuid": remote_uuid, "apikey": api_key}
    req = requests.get(url, params=params, headers=headers, verify=False).json()
    status = req["status"]
    server_status = server_status_name(req["data"]["status"])
    return status, server_status

def check_instance_one(nickname:str):
    try:
        uuid = instances[nickname]["uid"]
        remote_uuid = instances[nickname]["gid"]
        status, server_status = check_instance(uuid, remote_uuid)
        server_status_one = nickname + "：" + server_status
    except KeyError:
        server_status_one = nickname + "：找不到实例"
    except:
        server_status_one = nickname + "：出现未知错误"
    return server_status_one


def check_instance_all():
    server_status_all = ""
    for k, v in instances.items():
        nickname = k
        uuid = v["uid"]
        remote_uuid = v["gid"]
        status, server_status = check_instance(uuid, remote_uuid)
        if status == 200:
            return_msg = nickname + "：" + server_status + "\n"
            server_status_all += return_msg
    return server_status_all[:-1]


def server_status_name(server_status):
    status_dict = {
        -1: "状态未知",
        0: "已停止",
        1: "正在停止",
        2: "正在启动",
        3: "正在运行",
    }
    if server_status in status_dict.keys():
        server_status = status_dict[server_status]
    return server_status

def operating_options_name(operating_options: str):
    operating_options_d = {"open": "开启", "stop": "关闭", "kill": "终止", "restart": "重启"}
    if operating_options in operating_options_d.keys():
        operating_options_n = operating_options_d[operating_options]
    return operating_options_n