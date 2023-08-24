from nonebot import on_regex, on_command
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP, PRIVATE_FRIEND
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
import httpx
import random
import os

mnkbutton = "https://github.com/yokinanya/monaka-button/raw/master/setting/translate/01_voices.json"
mnkbutton_cn = "https://jsd.cdn.zzko.cn/gh/yokinanya/monaka-button@master/setting/translate/01_voices.json"
voice_header = "https://monaka-button.yokinanya.icu/voices"
local_resource = os.path.abspath("./omega_miya/local_resource/audio/button_voice/mnk_voice/")


def get_voice():
    with httpx.Client() as client:
        response = client.get(url=mnkbutton_cn)
    voice_json = response.json()
    voice_list = []
    voice_list_m = []
    for i in voice_json:
        if i["category"] == "唱歌":
            voice_list_m.append(i["name"])
        else:
            voice_list.append(i["name"])
    return voice_list, voice_list_m


def generate_voice(voice_name: str, voice: str):
    voice_url = voice + f"/{voice_name}.mp3"
    return voice_url


def download_voice(voice: str):
    voice_list, voice_list_m = get_voice()
    voice_list_download = []
    mnk_voices = os.listdir(local_resource)
    for i in voice_list:
        voice_path = i + '.mp3'
        if voice_path not in mnk_voices:
            voice_list_download.append(voice_path)
    num = 0
    fail_num = 0
    try:
        for voice_path in voice_list_download:
            voice_url = voice + f"/{voice_path}"
            try:
                f = httpx.get(voice_url)
                save_path = os.path.abspath(os.path.join(local_resource, voice_path))
                with open(save_path, "wb") as mnk:
                    mnk.write(f.content)
                num += 1
            except:
                fail_num += 1
        msg = f"成功获取到{num}个语音，失败{fail_num}个"
    except:
        msg = f"成功获取到{num}个语音，失败{fail_num}个"
    return msg


def get_cache(voice_name: str):
    mnk_voices = os.listdir(local_resource)
    voice_name = voice_name + '.mp3'
    if voice_name in mnk_voices:
        voice_path = os.path.abspath(os.path.join(local_resource, voice_name))
    else:
        voice_path = None
    return voice_path


refresh = on_command(
    'refresh_button',
    aliases={'更新mnk按钮'},
    priority=10,
    permission=GROUP | PRIVATE_FRIEND,
    block=True
)


@refresh.handle()
async def handle_request(bot: Bot, event: MessageEvent, matcher: Matcher):
    msg = download_voice(voice=voice_header)
    await matcher.finish(msg)


button = on_regex(
    pattern='^来个',
    priority=1,
    block=True,
    permission=GROUP | PRIVATE_FRIEND
)


@button.handle()
async def handle_mnk_button(bot: Bot, event: MessageEvent, matcher: Matcher, message: Message = EventMessage()):
    raw_msg = event.raw_message
    msg = raw_msg.replace("来个", "", 1)
    voice_list, voice_list_m = get_voice()
    if msg == "啥":
        voice = random.choice(voice_list)
    elif msg in voice_list:
        voice = msg
    elif msg in voice_list_m:
        voice = msg
    else:
        await matcher.finish("")
    voice_path = get_cache(voice_name=voice)
    if voice_path is None:
        voice_url = generate_voice(voice_name=voice, voice=voice_header)
    else:
        voice_url = "file://" + voice_path
    voice_msg = MessageSegment.record(file=voice_url)
    await matcher.finish(voice_msg)
