import os
from nonebot import on_command, get_driver
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.typing import T_State

from .utils import get_ip, mcstate, read_data, write_data, get_favicon, decode_image

mc_state = on_command("mcstate", aliases={"服务器状态", "mcstate"}, priority=50, block=True)
serverip = os.path.abspath(os.path.join(os.path.dirname(__file__), r"serverip.json"))
su = get_driver().config.superusers


@mc_state.handle()
async def handle_first_receive(state: T_State, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    groupid = event.group_id
    try:
        ip = get_ip(groupid, serverip)
        if plain_text == "":
            plain_text = ip.strip()
    except Exception:
        pass
    if plain_text:
        state.update({'IP': plain_text})


@mc_state.got("IP", prompt="请输入服务器IP地址")
async def handle_city(bot: Bot, event: GroupMessageEvent, ip: str = ArgStr('IP')):
    groupid = event.group_id
    ipdata = read_data(serverip)
    ipdata[str(groupid)] = ip
    try:
        img_base64 = get_favicon(ip)
        img_url = r"file://" + decode_image(img_base64)
        print(img_url)
        img_seg = MessageSegment.image(img_url)
        msg = img_seg + "\n" + mcstate(ip)
    except:
        msg = mcstate(ip)
    if "离线" in msg:
        pass
    else:
        write_data(ipdata, serverip)
    await mc_state.finish(msg, at_sender=False)
