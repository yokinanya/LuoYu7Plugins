from nonebot import on_command, get_driver
from nonebot.plugin import CommandGroup
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgStr
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .utils import game_code, game_code_writer

gamecode = on_command("gamecode", aliases={"兑换码"}, priority=50, block=True)


@gamecode.handle()
async def handle_first_receive(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'Game': plain_text})


@gamecode.got("Game", prompt="请输入你要查询的游戏：\n【明日方舟|原神|崩坏3】")
async def handle(event: MessageEvent, game: str = ArgStr('Game')):
    arknights = ["明日方舟", "舟", "舟舟", "方舟"]
    genshin_impact = ["原神", "原", "O"]
    honkai_impact_3 = ["崩坏3", "BBB", "崩崩崩", "三蹦子"]
    if game in arknights:
        game = "arknights"
        gamecodes = game_code(game)
    elif game in genshin_impact:
        game = "genshin"
        gamecodes = game_code(game)
    elif game in honkai_impact_3:
        game = "bh3"
        gamecodes = game_code(game)
    else:
        await gamecode.reject_arg(key="Game", prompt="你输入的游戏名有误或数据库内未收录该游戏的兑换码")
    if gamecodes == "":
        gamecodes = "没有找到相关兑换码"
    await gamecode.finish(gamecodes)


codeeditor = CommandGroup(
    'code',
    permission=SUPERUSER,
    priority=10,
    block=True
)

add_code = codeeditor.command('add', aliases={"添加兑换码"})
del_code = codeeditor.command('del', aliases={"删除兑换码"})
edit_code = codeeditor.command('edit', aliases={"编辑兑换码"})


@add_code.handle()
async def handle_first_connect(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'Game': plain_text})


@add_code.got("Game", prompt="游戏名：")
@add_code.got("Code", prompt="兑换码：")
@add_code.got("Description", prompt="兑换码描述：")
async def handel_add_code(event: MessageEvent, game: str = ArgStr('Game'), code: str = ArgStr('Code'), description: str = ArgStr('Description')):
    arknights = ["明日方舟", "舟", "舟舟", "方舟"]
    genshin_impact = ["原神", "原", "O"]
    honkai_impact_3 = ["崩坏3", "BBB", "崩崩崩", "三蹦子"]
    if game in arknights:
        game = "arknights"
        status = game_code_writer(game, code, description, operation="add")
    elif game in genshin_impact:
        game = "genshin"
        status = game_code_writer(game, code, description, operation="add")
    elif game in honkai_impact_3:
        game = "bh3"
        status = game_code_writer(game, code, description, operation="add")
    else:
        await gamecode.reject_arg(key="Game", prompt="游戏名错误")
    await add_code.finish(message="执行操作完成(但不一定成功)")


@del_code.handle()
async def handle_first_connect(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'Game': plain_text})


@del_code.got("Game", prompt="游戏名：")
@del_code.got("Code", prompt="兑换码：")
async def handel_add_code(event: MessageEvent, game: str = ArgStr('Game'), code: str = ArgStr('Code')):
    arknights = ["明日方舟", "舟", "舟舟", "方舟"]
    genshin_impact = ["原神", "原", "O"]
    honkai_impact_3 = ["崩坏3", "BBB", "崩崩崩", "三蹦子"]
    description = ""
    if game in arknights:
        game = "arknights"
        status = game_code_writer(game, code, description, operation="del")
    elif game in genshin_impact:
        game = "genshin"
        status = game_code_writer(game, code, description, operation="del")
    elif game in honkai_impact_3:
        game = "bh3"
        status = game_code_writer(game, code, description, operation="del")
    else:
        await gamecode.reject_arg(key="Game", prompt="游戏名错误")
    await del_code.finish(message="执行操作完成(但不一定成功)")


@edit_code.handle()
async def handle_first_connect(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'Game': plain_text})


@edit_code.got("Game", prompt="游戏名：")
@edit_code.got("Code", prompt="兑换码：")
@edit_code.got("Description", prompt="兑换码描述：")
async def handel_add_code(event: MessageEvent, game: str = ArgStr('Game'), code: str = ArgStr('Code'), description: str = ArgStr('Description')):
    arknights = ["明日方舟", "舟", "舟舟", "方舟"]
    genshin_impact = ["原神", "原", "O"]
    honkai_impact_3 = ["崩坏3", "BBB", "崩崩崩", "三蹦子"]
    if game in arknights:
        game = "arknights"
        status =game_code_writer(game, code, description, operation="edit")
    elif game in genshin_impact:
        game = "genshin"
        status = game_code_writer(game, code, description, operation="edit")
    elif game in honkai_impact_3:
        game = "bh3"
        status = game_code_writer(game, code, description, operation="edit")
    else:
        await gamecode.reject_arg(key="Game", prompt="游戏名错误")
    await edit_code.finish(message="执行操作完成(但不一定成功)")
