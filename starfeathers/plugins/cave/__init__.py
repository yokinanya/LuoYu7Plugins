import re
from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, MessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .utils import generate_cave, write_db


# 注册事件响应器
cave = on_regex(
    pattern=r"^(.|。)cave$",
    flags=re.I,
    permission=GROUP,
    priority=10,
    block=True,
)

addcave = on_command(
    cmd='addcave',
    permission=SUPERUSER,
    priority=10,
    block=True,
)


@cave.handle()
async def cave_handler(bot: Bot, event: GroupMessageEvent, state: T_State):
    message = generate_cave()
    await bot.send(event, message)


@addcave.handle()
async def handle_first_receive(state: T_State, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'cave_msg': plain_text, 'uploader': "匿名投稿"})


@addcave.got('cave_msg', prompt='请输入回声洞投稿文本：')
@addcave.got('uploader', prompt='请输入回声洞投稿人用户名：')
async def add_cave(matcher: Matcher, bot: Bot, event: MessageEvent, cave_msg: str = ArgStr('cave_msg'), uploader: str = ArgStr('uploader')):
    if cave_msg == "pass" or cave_msg == "跳过":
        cave_msg = ""
    if uploader == "pass" or uploader == "跳过":
        uploader = ""
    return_msg = write_db(cave_msg, uploader)
    msg =  f"{cave_msg}\n{uploader}\n{return_msg}"
    await addcave.finish(return_msg)
