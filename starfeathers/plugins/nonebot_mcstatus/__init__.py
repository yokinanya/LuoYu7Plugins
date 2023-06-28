import os
from nonebot import on_command, get_driver
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11.permission import GROUP, PRIVATE_FRIEND, GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .utils import get_info, serverstatus, read_data, write_data, get_favicon, decode_image

status = on_command("mcstatus", permission=GROUP | PRIVATE_FRIEND, aliases={"服务器状态"}, priority=50, block=True)
setdefault = on_command("setmcdefault", permission=GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND | SUPERUSER, aliases={"设置默认服务器"}, priority=50, block=True)
default_group_ip = os.path.abspath(os.path.join(os.path.dirname(__file__), r"default_group_ip.json"))


@status.handle()
async def get_default(state: T_State, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip().split()
    gid = event.group_id
    if len(plain_text) == 0:
        try:
            ip, platform = get_info(gid, default_group_ip)
            ip = ip.strip()
            platform = platform.strip()
            state.update({'IP': ip, "Platform": platform})
        except Exception:
            pass
    elif len(plain_text) == 1:
        if "JE" not in plain_text[0] and "BE" not in plain_text[0]:
            ip = plain_text[0]
            state.update({'IP': ip})
        else:
            platform = plain_text[0]
            state.update({"Platform": platform})
    elif len(plain_text) == 2:
        ip = plain_text[0]
        platform = plain_text[1]
        state.update({'IP': ip, "Platform": platform})
    else:
        pass


@status.got("IP", prompt="请输入服务器IP地址")
@status.got("Platform", prompt="请输入服务器平台【JE/BE】")
async def check_server(bot: Bot, event: GroupMessageEvent, ip: str = ArgStr('IP'), platform: str = ArgStr('Platform')):
    try:
        img_base64 = get_favicon(ip)
        img_url = r"file://" + decode_image(img_base64)
        img_seg = MessageSegment.image(img_url)
        msg = img_seg + "\n" + serverstatus(ip, platform)
    except:
        msg = serverstatus(ip, platform)
    await status.finish(msg, at_sender=False)


@setdefault.handle()
async def get_default(state: T_State, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):

    plain_text = args.extract_plain_text().strip().split()
    if len(plain_text) == 1:
        if "JE" not in plain_text[0] and "BE" not in plain_text[0]:
            ip = plain_text[0]
            state.update({'IP': ip})
        else:
            platform = plain_text[0]
            state.update({"Platform": platform})
    elif len(plain_text) == 2:
        ip = plain_text[0]
        platform = plain_text[1]
        state.update({'IP': ip, "Platform": platform})
    else:
        pass


@setdefault.got("IP", prompt="请输入服务器IP地址")
@setdefault.got("Platform", prompt="请输入服务器平台【JE/BE】")
async def check_server(bot: Bot, event: GroupMessageEvent, ip: str = ArgStr('IP'), platform: str = ArgStr('Platform')):
    gid = event.group_id
    ipdata = read_data(default_group_ip)
    ipdata[str(gid)] = {}
    ipdata[str(gid)]["ip"] = ip
    ipdata[str(gid)]["platform"] = platform
    try:
        img_base64 = get_favicon(ip)
        img_url = r"file://" + decode_image(img_base64)
        img_seg = MessageSegment.image(img_url)
        msg = img_seg + "\n" + serverstatus(ip, platform)
    except:
        msg = serverstatus(ip, platform)
    write_data(ipdata, default_group_ip)
    await setdefault.send("服务器已保存", at_sender=False)
    await setdefault.finish(msg, at_sender=False)