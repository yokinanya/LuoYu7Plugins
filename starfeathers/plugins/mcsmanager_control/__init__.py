from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher

from .utils import *
from .config import global_config, plugin_config

mcsm = on_startswith("!!mcsm", priority=1, block=True, permission=GROUP)

mcsm_help = "MCSManager Control\n!!mcsm <操作选项> <实例别名>\n!!mcsm status <实例别名>\n!!mcsm help\n\n操作选项包括：\nopen, stop, kill, restart\n实例别名是插件配置文件中的实例别名，不是MCSManager的实例名"

react_group_id = plugin_config.react_group_id
react_user_id = plugin_config.react_user_id

@mcsm.handle()
async def get_default(event: GroupMessageEvent, matcher: Matcher):
    plaintext = event.get_plaintext()
    args = plaintext.strip().split(" ")
    group_id = event.group_id
    user_id = event.user_id
    operating_options_l = ["open", "stop", "kill", "restart"]
    if group_id == react_group_id:
        try:
            if args[1] in operating_options_l:
                if user_id in react_user_id:
                    operating_options = args[1]
                    if len(args) <= 2:
                        server_status_all = instance_controller_all(operating_options)
                        await mcsm.finish(server_status_all)
                    else:
                        server_status_one = instance_controller_one(operating_options, args[2])
                        await mcsm.finish(server_status_one)
                else:
                    mcsm.finish("你想屁吃")
            elif args[1] == "status":
                if len(args) <= 2:
                    server_status_all = check_instance_all()
                    await mcsm.finish(server_status_all)
                else:
                    server_status_one = check_instance_one(args[2])
                    await mcsm.finish(server_status_one)
            else:
                await mcsm.finish(mcsm_help)
        except Exception as e:
            pass
