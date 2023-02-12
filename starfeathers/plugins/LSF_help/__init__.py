from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP, PRIVATE_FRIEND
from nonebot.matcher import Matcher
from nonebot.typing import T_State
import httpx


menu = on_command(
    cmd='menu',
    aliases={"菜单", "帮助"},
    permission=GROUP | PRIVATE_FRIEND,
    priority=10,
    block=True,
)

api = "https://0sf-database.vercel.app/support"
api_support = api + "/main.json"
docs = "https://0sf.yokinanya.icu"
docs_mirror = "https://mirrors.0sf.yokinanya.icu/"


@menu.handle()
async def menu(bot: Bot, event: MessageEvent, matcher: Matcher, state: T_State):
    try:
        with httpx.Client(proxies="http://127.0.0.1:7890") as client:
            response = client.get(url=api_support)
        version = response.json()["version"]
        tittle = response.json()["tittle"]
        raw = response.json()["raw"]
        announcement = response.json()["announcement"]
        docs_text = f"{tittle}\n{announcement}{raw}\n当前版本：{version}"
    except:
        docs_text = f"※ 铃星羽 ※\n\n帮助文档：\n{docs}\n镜像地址：\n{docs_mirror}\n当前版本：无法获取"
    await bot.send(event=event, message=docs_text)
