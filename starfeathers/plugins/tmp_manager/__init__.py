from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import ArgStr
from nonebot.permission import SUPERUSER
from .utils import get_folder_info, get_path, delete_folder


folder_info = on_command('tmpinfo', aliases={'缓存大小'}, permission=SUPERUSER, priority=10, block=True)
del_tmp = on_command('deltmp', aliases={'删除缓存'}, permission=SUPERUSER, priority=10, block=True)


@folder_info.handle()
async def handle_info(matcher: Matcher, bot: Bot, event: MessageEvent):
    subinfo = get_folder_info("tmp")
    msg = f"缓存目录大小：\n{subinfo}"
    await folder_info.finish(msg)


@del_tmp.handle()
async def handle_del(matcher: Matcher, bot: Bot, event: MessageEvent):
    path = get_path("tmp")
    await matcher.send(f'即将删除目录【{path}】')


@del_tmp.got('check', prompt='确认吗?\n【是/否】')
async def handle_del(matcher: Matcher, bot: Bot, event: MessageEvent, check: str = ArgStr('check')):
    check = check.strip()
    if check != '是':
        await matcher.finish('那就不删了哦')
    delete_folder("tmp")
    await matcher.finish('删除成功')
