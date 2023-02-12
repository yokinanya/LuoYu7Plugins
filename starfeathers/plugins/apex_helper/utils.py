import json
import os
import requests
import httpx
from nonebot import get_driver
from .config import Config

apexApi = Config.parse_obj(get_driver().config).apex_api_token
botapi = "https://0sf-database.vercel.app/apex"
vtuber_data = f"{botapi}/vtuber.json"


def lang(langode: str):
    lang = os.path.abspath(os.path.join(os.path.dirname(__file__), f"{botapi}/{langode}.json"))
    with open(lang, "r", encoding="utf-8") as lang:
        langs = json.load(lang)
        maps = langs["map"]
        crafts = langs["craft"]
        raritys = langs["rarity"]
        rank = langs["rank"]
        legends = langs["legends"]
        event = langs["event"]
        lang.close()
    return maps, crafts, raritys, rank, legends, event


maps, crafts, raritys, rank, legends, event = lang("zh_cn")


def vtuver():
    with httpx.Client() as client:
        response = client.get(url=vtuber_data)
    vtbdata = response.json()
    
    return vtbdatas


def read_userdata(qqid: int):
    userdata = os.path.abspath(os.path.join(os.path.dirname(__file__), r"userdata.json"))
    with open(userdata, "r", encoding="utf-8") as userdata:
        userdatas = json.load(userdata)
        username = userdatas[str(qqid)]["username"]
        platform = userdatas[str(qqid)]["platform"]
        uid = userdatas[str(qqid)]["uid"]
        userdata.close()
    return username, platform, uid


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


def NametoUid(sname: str, platform: str):
    URL = f"https://api.mozambiquehe.re/nametouid?auth={apexApi}&player={sname}&platform={platform}"
    jsonobj = requests.get(URL).json()
    try:
        uid = jsonobj["uid"]
    except:
        uid = None
    return uid

def statusID(platform: str, uid: int):
    URL = f"https://api.mozambiquehe.re/bridge?auth={apexApi}&uid={uid}&platform={platform}"
    jsonobj = requests.get(URL).json()
    try:
        name = jsonobj["global"]["name"]  # 昵称
        level = jsonobj["global"]["level"]  # 等级
        rankscore = jsonobj["global"]["rank"]["rankScore"]  # 排名分
        rankname = jsonobj["global"]["rank"]["rankName"]  # 段位
        predatorrank = jsonobj["global"]["rank"]["ladderPosPlatform"]  # 猎杀排名
        state, selectedLegend = get_state(jsonobj)  # 当前状态
        if rankname in rank.keys():
            rankname = rank[rankname]
        if predatorrank == -1:
            predatorrank = "未上榜"
        msg = f"\n昵称：{name}\n等级：{level}\n排名分：{rankscore}\n段位：{rankname}\n猎杀排名：{predatorrank}\n当前状态：{state}\n所选传奇：{selectedLegend}"
    except Exception:
        msg = "查询失败，请检查用户名是否正确然后重试，steam平台请输入orginid"
    return msg


def status(sname: str, platform: str, player: int):
    URL = f"https://api.mozambiquehe.re/bridge?auth={apexApi}&player={player}&platform={platform}"
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


def update_map():
    map_URL = f"https://api.mozambiquehe.re/maprotation?auth={apexApi}&version=2"
    map_jsonobj = requests.get(map_URL).json()
    return map_jsonobj


def get_map(type: str, jsonobj):
    try:
        mapremaintime = jsonobj[type]["current"]["remainingTimer"]
    except:
        mapremaintime = "查询失败"
    try:
        mapcode = jsonobj[type]["current"]["code"]
    except:
        mapcode = "查询失败"
    try:
        nextcode = jsonobj[type]["next"]["code"]
    except:
        nextcode = "查询失败"
    if mapcode in maps.keys():
        mapcode = maps[mapcode]
    if nextcode in maps.keys():
        nextcode = maps[nextcode]
    name = "当前地图：" + mapcode
    remainingTimer = "剩余时间：" + mapremaintime
    next = "下一个地图：" + nextcode
    info = f"{name}\n{remainingTimer}\n{next}"
    return info


def get_map_ltm(jsonobj):
    isActive = jsonobj["ltm"]["current"]["isActive"]
    eventName = jsonobj["ltm"]["current"]["eventName"]
    mapremaintime = jsonobj["ltm"]["current"]["remainingTimer"]
    mapcode = jsonobj["ltm"]["current"]["code"]
    nextcode = jsonobj["ltm"]["next"]["code"]
    if mapcode in maps.keys():
        mapcode = maps[mapcode]
    if nextcode in maps.keys():
        nextcode = maps[nextcode]
    if eventName in event.keys():
        eventName = event[eventName]
    name = "当前地图：" + mapcode
    remainingTimer = "剩余时间：" + mapremaintime
    next = "下一个地图：" + nextcode
    info = f"{eventName}：\n{name}\n{remainingTimer}\n{next}"
    if isActive != True:
        info = "暂无活动"
    return info
