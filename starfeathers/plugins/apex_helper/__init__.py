import json
import os
import requests
from nonebot import on_command, get_driver
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgStr
from nonebot.typing import T_State
from .config import Config


apexApi = Config.parse_obj(get_driver().config).apex_api_token


inquire = on_command("inquire", aliases={"查询"}, priority=50, block=True)
connect = on_command("connect", aliases={"绑定"}, priority=50, block=True)
crafting = on_command("craft", aliases={"复制器"}, priority=50, block=True)
help = on_command("apexhelp", aliases={"apex帮助", "Apex帮助"}, priority=50, block=True)
map = on_command("map", aliases={"地图"}, priority=50, block=True)


def lang(langode: str):
    lang = os.path.abspath(os.path.join(os.path.dirname(__file__), f"{langode}.json"))
    with open(lang, "r", encoding="utf-8") as lang:
        langs = json.load(lang)
        maps = langs["map"]
        crafts = langs["craft"]
        raritys = langs["rarity"]
        rank = langs["rank"]
        legends = langs["legends"]
        lang.close()
        return maps, crafts, raritys, rank, legends


maps, crafts, raritys, rank, legends = lang("zh_cn")


def read_userdata(qqid: int):
    userdata = os.path.abspath(os.path.join(os.path.dirname(__file__), r"userdata.json"))
    with open(userdata, "r", encoding="utf-8") as userdata:
        userdatas = json.load(userdata)
        username = userdatas[str(qqid)]["username"]
        platform = userdatas[str(qqid)]["platform"]
        userdata.close()
    return username, platform


def read_data():
    userdata = os.path.abspath(os.path.join(os.path.dirname(__file__), r"userdata.json"))
    with open(userdata, "r", encoding="utf-8") as userdata:
        userdatas = json.load(userdata)
        userdata.close()
    return userdatas


def write_userdata(userdatas: dict):
    userdata = os.path.abspath(os.path.join(os.path.dirname(__file__), r"userdata.json"))
    with open(userdata, "w", encoding="utf-8") as userdata:
        json.dump(userdatas, userdata)
        userdata.close()


def get_state(jsonobj):
    pstate = jsonobj["realtime"]  # 状态jsonobj
    online = pstate["isOnline"]  # 在线状态
    inGame = pstate["isInGame"]  # 游戏状态
    selectedLegend = pstate["selectedLegend"]  # 当前所选传奇
    if selectedLegend in legends.keys():
        selectedLegend = legends[selectedLegend]
    if online == 1:
        if inGame == 1:
            state = "游戏中"
        else:
            state = "在线中"
    else:
        state = "离线中"
    return state, selectedLegend


def stat(sname: str, platform: str):
    URL = f"https://api.mozambiquehe.re/bridge?auth={apexApi}&player={sname}&platform={platform}"
    jsonobj = requests.get(URL).json()
    try:
        name = jsonobj["global"]["name"]  # 昵称
        level = jsonobj["global"]["level"]  # 等级
        rankscore = jsonobj["global"]["rank"]["rankScore"]  # 排名分
        rankname = jsonobj["global"]["rank"]["rankName"]  # 段位
        predatorrank = jsonobj["global"]["rank"]["ladderPosPlatform"]  # 猎杀排名
        state, selectedLegend = get_state(jsonobj)  # 当前状态
        if name == "":
            name = sname
        if rankname in rank.keys():
            rankname = rank[rankname]
        if predatorrank == -1:
            predatorrank = "未上榜"
        msg = f"\n昵称：{name}\n等级：{level}\n排名分：{rankscore}\n段位：{rankname}\n猎杀排名：{predatorrank}\n当前状态：{state}\n所选传奇：{selectedLegend}"
    except Exception:
        msg = "查询失败，请检查用户名是否正确然后重试，steam平台请输入orginid"
    return msg


@inquire.handle()
async def handle_first_receive(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    qqid = event.user_id
    try:
        username, platform = read_userdata(qqid)
        if plain_text == "":
            plain_text = username.strip()
    except Exception:
        pass
    if plain_text:
        state.update({'Name': plain_text})


@inquire.got("Name", prompt="你想查询谁的战绩呢?")
async def handle_city(event: MessageEvent, uname: str = ArgStr('Name')):
    qqid = event.user_id
    userdatas = read_data()
    userdatas[str(qqid)] = {"username": uname, "platform": "PC"}
    msg = stat(sname=uname, platform="PC")
    await inquire.finish(msg, at_sender=True)


@connect.handle()
async def handle_first_connect(state: T_State, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    qqid = event.user_id
    if plain_text:
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
    qqid = event.user_id
    userdatas = read_data()
    userdatas[str(qqid)] = {"username": uname, "platform": uplatform}
    msg = stat(sname=uname, platform=uplatform)
    if "查询失败" in msg:
        pass
    else:
        write_userdata(userdatas)
        msg = "绑定成功\n" + msg
    await inquire.finish(msg, at_sender=True)


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


@help.handle()
async def help_handle(bot: Bot, event: Event):
    msg = "Apex助手\n查询地图轮换：#地图\n查询制造器轮换：#复制器\n查询战绩：#查询 <id>\n查看当前列表：#Apex帮助"
    await help.send(msg, at_sender=False)


@map.handle()
async def map_handle(bot: Bot, event: Event):
    await map.send("查询地图轮换中,请稍后", at_sender=False)
    URL = f"https://api.mozambiquehe.re/maprotation?auth={apexApi}&version=2"
    jsonobj = requests.get(URL).json()

    def get_map(type: str):
        mapremaintime = jsonobj[type]["current"]["remainingTimer"]
        mapcode = jsonobj[type]["current"]["code"]
        nextcode = jsonobj[type]["next"]["code"]
        if mapcode in maps.keys():
            mapcode = maps[mapcode]
        if nextcode in maps.keys():
            nextcode = maps[nextcode]
        name = "当前地图：" + mapcode
        remainingTimer = "剩余时间：" + mapremaintime
        next = "下一个地图：" + nextcode
        info = f"{name}\n{remainingTimer}\n{next}"
        return info

    # battle_royale
    battle_royale = "大逃杀：\n" + get_map("battle_royale")
    # ranked
    ranked = "积分联赛：\n" + get_map("ranked")
    # arenas
    arenas = "竞技场：\n" + get_map("arenas")
    # arenasRanked
    arenasRanked = "竞技场排位：\n" + get_map("arenasRanked")
    # control
    # control = "控制：\n"+ get_map("control")
    msg = f"{battle_royale}\n{ranked}\n{arenas}\n{arenasRanked}"
    await map.send(msg)
