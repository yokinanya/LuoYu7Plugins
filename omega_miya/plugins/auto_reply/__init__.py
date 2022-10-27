import re
import os
from nonebot import on_regex, on_endswith, logger
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.adapters.onebot.v11.message import MessageSegment
from omega_miya.service import init_processor_state
from .resources import data_voices, data_images


# 文字回复
# 事件响应器
regular = {
    r'^mua(~)?$': "呸呸呸",
    r'[\s\S]*桃井最中Monaka的直播间开播啦[\s\S]*': "哈哈，雏萌的消息真不灵通啊"
}
regular_rule = {
    r'^mua(~)?$': [''],
    r'[\s\S]*桃井最中Monaka的直播间开播啦[\s\S]*': ['816950992']
}
reply_pattern = ''
for key in regular:
    reply_pattern = key + '|' + reply_pattern
reply_pattern = reply_pattern[0:-1]

reply = on_regex(
    reply_pattern,
    state=init_processor_state(name="reply", level=10, echo_processor_result=False),
    permission=GROUP,
    priority=50,
    block=True
)


@reply.handle()
async def handle_dydy(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    message = event.raw_message
    groupid = event.group_id
    logger.info(message, groupid)
    for key in regular:
        try:
            if re.match(key, message):
                if str(groupid) in regular_rule[key] or regular_rule[key] == ['']:
                    reply_msg = regular[key]
                    await reply.send(reply_msg)
                    break
        except Exception:
            pass
            continue


# 语音图片回复
# 全局变量
disable_group = [816950992]

# 事件响应器
dydy = on_endswith(
    msg="对呀对呀",
    state=init_processor_state(name="dydy", level=10, echo_processor_result=False),
    permission=GROUP,
    priority=50,
    block=False
)

circle = on_regex(
    pattern=r'^转圈圈$',
    state=init_processor_state(name="circle", level=10, echo_processor_result=False),
    permission=GROUP,
    priority=50,
    block=False
)


@dydy.handle()
async def handle_dydy(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    group_id = event.group_id
    if group_id in disable_group:
        pass
    else:
        voice = str("对呀对呀")
        voice_file = data_voices.get_voice(keyword=voice)
        if not os.path.exists(voice_file):
            pass
        else:
            msg = MessageSegment.record(file=f"file:///{voice_file}")
            await dydy.send(msg)


@circle.handle()
async def handle_dydy(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    group_id = event.group_id
    if group_id in disable_group:
        pass
    else:
        image = str("转圈圈")
        image_file = data_images.get_image(keyword=image)
        if not os.path.exists(image_file):
            pass
        else:
            msg = MessageSegment.image(file=f"file:///{image_file}")
            await circle.send(msg)
