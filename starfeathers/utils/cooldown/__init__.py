import pathlib
import os
import sys
import json
import time
import nonebot
from nonebot.log import logger
su = nonebot.get_driver().config.superusers

__all__ = ["check_cooldown"]

lsf_data = pathlib.Path(os.path.abspath(sys.path[0])).joinpath('starfeathers/data')
cooldown = os.path.join(lsf_data, 'cooldown.json')
if not os.path.exists(cooldown):
    with open(cooldown, 'w', encoding='utf-8') as f:
        cooldown_data = {}
        json.dump(cooldown_data, f)
        f.close()


def get_cooldown(plugin: str):
    '''
    获取冷却时间
    plugin (string) : plugin name
    '''
    cooldown_data = {}
    try:
        with open(cooldown, 'r', encoding='utf-8') as cooldown_json:
            cooldown_data = json.load(cooldown_json)
    except KeyError:
        with open(cooldown, 'w', encoding='utf-8') as cooldown_json:
            cooldown_data[plugin] = int(time.time())
            json.dump(cooldown_data, cooldown_json)
    cooldown_time = cooldown_data[plugin]
    return cooldown_time


def check_cooldown(plugin: str, qq_id: str, addtime: int, suaddtime: int = 0):
    '''
    判断是否还在冷却
    plugin (string) : plugin name
    '''
    cooldown_data = {}
    cooldown_time = get_cooldown(plugin)
    cooldown_local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cooldown_time))
    nowtick = int(time.time())
    if qq_id in su:
        coolstatus = False
        cooldown_time = nowtick + suaddtime
        logger.info(f"[{qq_id}]使用了插件[{plugin}]，冷却时间更新至{cooldown_time}[+{suaddtime}]")
    elif nowtick > cooldown_time:
        coolstatus = False
        cooldown_time = nowtick + addtime
        cooldown_data[plugin] = cooldown_time
        with open(cooldown, 'w', encoding='utf-8') as cooldown_json:
            json.dump(cooldown_data, cooldown_json)
        logger.info(f"[{qq_id}]使用了插件[{plugin}]，冷却时间更新至{cooldown_time}[+{addtime}]")
    else:
        coolstatus = True
        logger.info(f"[{qq_id}]使用了插件[{plugin}]，插件处于冷却中，冷却时间至{cooldown_time}")
    return coolstatus, cooldown_time, cooldown_local
