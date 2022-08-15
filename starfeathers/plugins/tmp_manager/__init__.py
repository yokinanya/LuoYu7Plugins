from nonebot import on_command, get_driver
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from .utils import get_folder_info, get_path, delete_folder, get_log_path, cp_log


folder_info = on_command('folderinfo', aliases={'目录大小'}, permission=SUPERUSER, priority=10, block=True)
del_tmp = on_command('deltmp', aliases={'删除缓存'}, permission=SUPERUSER, priority=10, block=True)


@folder_info.handle()
async def handle_first_receive(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'Folder': plain_text})


@folder_info.got("Folder", prompt="请选择查询的目录：tmp，log")
async def handle_info(matcher: Matcher, bot: Bot, event: MessageEvent, folder: str = ArgStr('Folder')):
    if folder not in ["log", "tmp"]:
        await matcher.reject_arg('Folder', prompt=f"{folder}不是可查询目录，请重新输入")
    subinfo = get_folder_info(folder)
    msg = f"{folder}目录大小：\n{subinfo}"
    await folder_info.finish(msg)


@del_tmp.handle()
async def handle_first_receive(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'Folder': plain_text})


@del_tmp.got("Folder", prompt="请选择执行的目录：tmp，log")
async def handle_del(matcher: Matcher, bot: Bot, event: MessageEvent, folder: str = ArgStr('Folder')):
    if folder not in ["log", "tmp"]:
        await matcher.reject_arg('Folder', prompt=f"{folder}不是可执行目录，请重新输入")
    path = get_path(folder)
    await matcher.send(f'即将删除目录【{path}】')


@del_tmp.got('check', prompt='确认吗?\n【是/否】')
async def handle_del(matcher: Matcher, bot: Bot, event: MessageEvent, check: str = ArgStr('check'), folder: str = ArgStr('Folder')):
    check = check.strip()
    if check != '是':
        await matcher.finish('那就不删了哦')
    delete_folder(folder)
    await matcher.finish('删除成功')
