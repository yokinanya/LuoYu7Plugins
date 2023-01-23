from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP, PRIVATE_FRIEND
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from starfeathers.utils.hitokoto import hitokoto_raw


menu = on_command(
    cmd='menu',
    aliases={"菜单", "帮助"},  # type: ignore
    permission=GROUP | PRIVATE_FRIEND,
    priority=10,
    block=True,
)

docs_url = "https://0sf.yokinanya.icu"
docs_url_mirror = "https://mirrors.0sf.yokinanya.icu/"


@menu.handle()  # type: ignore
async def menu(bot: Bot, event: MessageEvent, matcher: Matcher, state: T_State):
    hitokoto_type = ["a", "b", "c"]
    hitokoto = hitokoto_raw(c=hitokoto_type)
    docs_text = f"※ 铃星羽 ※\n\n帮助文档：\n{docs_url}\n镜像地址：\n{docs_url_mirror}\n当前版本：v3.3"
    await bot.send(event=event, message=docs_text)
