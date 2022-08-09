import os
import random
from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.typing import T_State

from omega_miya.service import init_processor_state
from omega_miya.service.gocqhttp_guild_patch.permission import GUILD

RESOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))


# 注册事件响应器
cave = on_command(
    'cave'
    state=init_processor_state(name='cave',level=10),
    aliases={"cave","回声洞"}
    permission= GROUP | GUILD,
    priority=10,
    block=True
)

# 获取回声洞内容
def getcave():
    data_path = os.path.join(RESOURCE_PATH, "cave.txt")
    # 检查文件是否存在
    if not os.path.exists(data_path):
        # 如果不存在，则创建文件
        with open(data_path, "w", encoding="utf-8") as f:
            f.write("QwQ")
    # 读取文件内容
    f = open(data_path, "r", encoding="utf-8")
    cave_data = f.readlines()
    return cave_data


# 随机获取回声洞内容
def getcave_random():
    cave_data = getcave()
    return cave_data[random.randint(0, len(cave_data) - 1)]

@cave.handle()
async def cave_handler(bot: Bot, event: GroupMessageEvent,state: T_State):
    cave_data = getcave_random()
    await bot.send(event, cave_data)
