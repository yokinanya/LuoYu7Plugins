import requests
import time
from nonebot import on_command, get_driver
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgStr
from nonebot.typing import T_State
from .config import Config
from .utils import lang, vtuver, read_userdata, read_data, write_userdata, NametoUid, status, update_map, get_map, statusID


apexApi = Config.parse_obj(get_driver().config).apex_api_token


inquire = on_command("inquire", aliases={"apex查询", "Apex查询"}, priority=50, block=True)
inquire_vtb = on_command("inquire", aliases={"apexvtb", "ApexVtb"}, priority=50, block=True)
connect = on_command("connect", aliases={"apex绑定", "Apex绑定"}, priority=50, block=True)
crafting = on_command("craft", aliases={"apex复制器", "Apex复制器"}, priority=50, block=True)
map = on_command("map", aliases={"apex地图", "Apex地图"}, priority=50, block=True)

maps, crafts, raritys, rank, legends, event = lang("zh_cn")


@inquire.handle()
async def handle_first_receive(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    qqid = event.user_id
    try:
        username, platform, uid = read_userdata(qqid)
        if plain_text == "":
            plain_text = uid
    except Exception:
        pass
    if plain_text:
        state.update({'Name': plain_text})


@inquire.got("Name", prompt="你想查询谁的战绩呢?")
async def handle_city(event: MessageEvent, uname: str = ArgStr('Name')):
    if uname.isnumeric() == True:
        uid = uname
        msg = statusID(platform="PC", uid=uid)
    else:
        msg = status(sname=uname, platform="PC", player=uname)
    await inquire.finish(msg, at_sender=True)

@inquire_vtb.handle()
async def handle_first_receive(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({'vtb': plain_text})


@inquire_vtb.got("vtb", prompt="你想查询谁的战绩呢?")
async def handle_city(event: MessageEvent, vtb: str = ArgStr('vtb')):
    vtbdatas = vtuver()
    if vtb in vtbdatas.keys():
        vtbid = vtbdatas[vtb]
        msg = statusID(platform="PC", uid=vtbid)
    else:
        msg = '该vtuber的游戏信息未收录'
    await inquire.finish(msg, at_sender=False)

@connect.handle()
async def handle_first_connect(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        if plain_text.isnumeric() == True:
            state.update({'uuid': int(plain_text)})
            state.update({'uPlatform': "PC"})
        else:
            state.update({'uName': plain_text})
            state.update({'uPlatform': "PC"})


@connect.got("uName", prompt="你想查询谁的战绩呢?")
@connect.got("uPlatform", prompt="你想查询的是哪个平台的呢？\n【PC\PS\Xbox】")
async def handle_city(event: MessageEvent, uname: str = ArgStr('uName'), uplatform: str = ArgStr('uPlatform')):
    win_platform = ["PC", "Origin", "Steam"]
    ps_platform = ["PS4", "PS5", "PS", "Playstation"]
    if uplatform in win_platform:
        uplatform = "PC"
    elif uplatform in ps_platform:
        uplatform = "PS4"
    elif uplatform == "Xbox":
        uplatform = "Xbox"
    else:
        connect.reject_arg(key="uPlatform", prompt="你输入的平台不对哦~请注意大小写~\n\n【PC\PS\Xbox】")
    if uname.isnumeric() == True:
        uid = int(uname)
    else:
        uid = NametoUid(sname=uname, platform=uplatform)
        time.sleep(3)
        if uid is None:
            await connect.finish(msg="绑定失败，请检查用户名是否正确然后重试，steam平台请输入orginid", at_sender=True)
        else:
            uid = int(uid)
    qqid = event.user_id
    userdatas = read_data()
    userdatas[str(qqid)] = {"username": uname, "platform": uplatform, "uid": uid}
    msg = statusID(sname=uname, platform=uplatform, uid=uid)
    if "查询失败" in msg:
        pass
    else:
        write_userdata(userdatas)
        msg = "绑定成功\n" + msg
    await connect.finish(msg, at_sender=True)


@crafting.handle()
async def craft_handle(bot: Bot, event: Event):
    await crafting.send("正在查询今日制造轮换，请稍候", at_sender=False)
    URL = f"https://api.mozambiquehe.re/crafting?auth={apexApi}"
    jsonobj = requests.get(URL).json()
    daily = jsonobj[0]
    weekly = jsonobj[1]
    dailycraft: list = []
    weeklycraft: list = []
    for num in range(2):
        craft = daily["bundleContent"][num]["itemType"]["name"]
        rarity = daily["bundleContent"][num]["itemType"]["rarity"]
        if craft in crafts.keys():
            craft = crafts[craft]
        if rarity in raritys.keys():
            rarity = raritys[rarity]
        craft_data = f"[{rarity}]{craft}"
        dailycraft.append(craft_data)
    dailycraft = f"{dailycraft[0]} , {dailycraft[1]}"
    for num in range(2):
        craft = weekly["bundleContent"][num]["itemType"]["name"]
        rarity = weekly["bundleContent"][num]["itemType"]["rarity"]
        if craft in crafts.keys():
            craft = crafts[craft]
        if rarity in raritys.keys():
            rarity = raritys[rarity]
        craft_data = f"[{rarity}]{craft}"
        weeklycraft.append(craft_data)
    weeklycraft = f"{weeklycraft[0]} , {weeklycraft[1]}"
    msg = f"今日轮换制造：{dailycraft}\n本周轮换制造：{weeklycraft}"
    await crafting.send(msg)


@map.handle()
async def map_handle(bot: Bot, event: Event):
    await map.send("查询地图轮换中,请稍后", at_sender=False)
    # battle_royale
    map_jsonobj = update_map()
    battle_royale = "大逃杀：\n" + get_map("battle_royale", map_jsonobj)
    # ranked
    ranked = "积分联赛：\n" + get_map("ranked", map_jsonobj)
    # arenas
    arenas = "竞技场：\n" + get_map("arenas", map_jsonobj)
    # arenasRanked
    arenasRanked = "竞技场排位：\n" + get_map("arenasRanked", map_jsonobj)
    # try:
    #     # ltm
    #     ltm = get_map_ltm(map_jsonobj)
    #     msg = f"{battle_royale}\n{ranked}\n{arenas}\n{arenasRanked}\n{ltm}"
    # except:
    msg = f"{battle_royale}\n{ranked}\n{arenas}\n{arenasRanked}"
    await map.send(msg)
