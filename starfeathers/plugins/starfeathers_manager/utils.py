import re
import json
import random
import nonebot
from pathlib import Path
from nonebot import logger

config_path = Path() / "config"
config_json = config_path / "admin.json"
config_group = config_path / "group_admin.json"
word_path = config_path / "word_config.txt"
words_path = Path() / "config" / "words"
res_path = Path() / "resource"
re_img_path = Path() / "resource" / "imgs"
ttf_name = Path() / "resource" / "msyhblod.ttf"

su = nonebot.get_driver().config.superusers


def At(data: str):
    """
    检测at了谁
    :param data: event.json
    :return: list
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                if 'all' not in str(msg):
                    qq_list.append(int(msg["data"]["qq"]))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []


async def banSb(gid: int, ban_list: list, **time: int):
    """
    构造禁言
    :param gid: 群号
    :param time: 时间（s)
    :param ban_list: at列表
    :return:禁言操作
    """
    if 'all' in ban_list:
        yield nonebot.get_bot().set_group_whole_ban(
            group_id=gid,
            enable=True
        )
    else:
        if not time:
            time = random.randint(1, 2591999)
        else:
            time = time['time']
        for qq in ban_list:
            if int(qq) in su or str(qq) in su:
                logger.info(f"SUPERUSER无法被禁言")
            else:
                yield nonebot.get_bot().set_group_ban(
                    group_id=gid,
                    user_id=qq,
                    duration=time,
                )


async def replace_tmr(msg: str) -> str:
    """
    原始消息简单处理
    :param msg: 消息字符串
    :return: 去除cq码,链接等
    """
    find_cq = re.compile(r"(\[CQ:.*])")
    find_link = re.compile("(https?://.*[^\u4e00-\u9fa5])")
    cq_code = re.findall(find_cq, msg)
    for cq in cq_code:
        msg = msg.replace(cq, "")
    links = re.findall(find_link, msg)
    for link in links:
        msg = msg.replace(link, "链接")
    return msg
