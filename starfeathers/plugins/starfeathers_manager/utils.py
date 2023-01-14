# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/1/16 10:15
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : utils.py
# @Software: PyCharm
import asyncio
import base64
import datetime
import json
import os
import random
import re
from typing import Union, Optional

import httpx
import nonebot
from nonebot import logger
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, ActionFailed, Bot
from nonebot.matcher import Matcher

from .config import plugin_config, global_config
from .path import *

su = global_config.superusers
cb_notice = plugin_config.callback_notice


def At(data: str) -> Union[list[str], list[int], list]:
    """
    检测at了谁，返回[qq, qq, qq,...]
    包含全体成员直接返回['all']
    如果没有at任何人，返回[]
    :param data: event.json
    :return: list
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data['message']:
            if msg['type'] == 'at':
                if 'all' not in str(msg):
                    qq_list.append(int(msg['data']['qq']))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []


def MsgText(data: str):
    """
    返回消息文本段内容(即去除 cq 码后的内容)
    :param data: event.json()
    :return: str
    """
    try:
        data = json.loads(data)
        # 过滤出类型为 text 的【并且过滤内容为空的】
        msg_text_list = filter(lambda x: x['type'] == 'text' and x['data']['text'].replace(' ', '') != '', data['message'])
        # 拼接成字符串并且去除两端空格
        msg_text = ' '.join(map(lambda x: x['data']['text'].strip(), msg_text_list)).strip()
        return msg_text
    except:
        return ''



async def banSb(gid: int, ban_list: list, time: int = None, scope: list = None):
    """
    构造禁言
    :param gid: 群号
    :param time: 时间（s)
    :param ban_list: at列表
    :param scope: 用于被动检测禁言的时间范围
    :return:禁言操作
    """
    if 'all' in ban_list:
        yield nonebot.get_bot().set_group_whole_ban(
            group_id=gid,
            enable=True
        )
    else:
        if time is None:
            if scope is None:
                time = random.randint(plugin_config.ban_rand_time_min, plugin_config.ban_rand_time_max)
            else:
                time = random.randint(scope[0], scope[1])
        for qq in ban_list:
            if int(qq) in su or str(qq) in su:
                logger.info(f"SUPERUSER无法被禁言, {qq}")
                # if cb_notice:
                #     await nonebot.get_bot().send_group_msg(group_id = gid, message = 'SUPERUSER无法被禁言')
            else:
                yield nonebot.get_bot().set_group_ban(
                    group_id=gid,
                    user_id=qq,
                    duration=time,
                )


async def change_s_title(bot: Bot, matcher: Matcher, gid: int, uid: int, s_title: Optional[str]):
    """
    改头衔
    :param bot: bot
    :param matcher: matcher
    :param gid: 群号
    :param uid: 用户号
    :param s_title: 头衔
    """
    try:
        await bot.set_group_special_title(
            group_id=gid,
            user_id=uid,
            special_title=s_title,
            duration=-1,
        )
        await log_fi(matcher, f"头衔操作成功:{s_title}")
    except ActionFailed:
        logger.info('权限不足')


async def sd(cmd: Matcher, msg, at=False) -> None:
    if cb_notice:
        await cmd.send(msg, at_sender=at)


async def log_sd(cmd: Matcher, msg, log: str = None, at=False, err=False) -> None:
    (logger.error if err else logger.info)(log if log else msg)
    await sd(cmd, msg, at)


async def fi(cmd: Matcher, msg) -> None:
    await cmd.finish(msg if cb_notice else None)


async def log_fi(cmd: Matcher, msg, log: str = None, err=False) -> None:
    (logger.error if err else logger.info)(log if log else msg)
    await fi(cmd, msg)
