import random
import nonebot
from nonebot import CommandGroup, logger, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from .utils import At

su = nonebot.get_driver().config.superusers


ban = on_command(
    "ban",
    aliases={"禁言"},
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER,
    priority=10,
    block=True,
)


@ban.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = str(event.get_message())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if len(msg.split()) == 2:
            try:
                for sb in sb:
                    if int(sb) in su or str(sb) in su:
                        logger.info("SUPERUSER无法被禁言")
                    else:
                        await bot.set_group_ban(
                            group_id=gid,
                            user_id=sb,
                            duration=int(msg.split()[-1:][0]),
                        )
            except ActionFailed:
                await ban.finish("权限不足")
            else:
                logger.info(f"禁言操作成功")
        else:
            try:
                for sb in sb:
                    if int(sb) in su or str(sb) in su:
                        logger.info("SUPERUSER无法被禁言")
                    else:
                        await bot.set_group_ban(
                            group_id=gid,
                            user_id=sb,
                            duration=random.randint(1, 2591999),
                        )
            except ActionFailed:
                await ban.finish("权限不足")
            else:
                logger.info(f"禁言操作成功")
    else:
        pass


change = on_command(
    "change",
    aliases={"改名"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
)


@change.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = str(event.get_message())
    logger.info(msg.split())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if len(msg.split()) == 2:
            try:
                await bot.set_group_card(group_id=gid, user_id=int(sb[0]), card=msg.split()[-1:][0])
            except ActionFailed:
                await change.finish("权限不足")
            else:
                logger.info("改名片操作成功")
        else:
            await change.finish("一次仅可更改一位群员的昵称")


kick = on_command(
    "kick",
    aliases={"kick", "踢人"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
)


@kick.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = str(event.get_message())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if "all" not in sb:
            try:
                for qq in sb:
                    await bot.set_group_kick(group_id=gid, user_id=int(qq), reject_add_request=False)
            except ActionFailed:
                await kick.finish("权限不足")
            else:
                await bot.send(message="踢人操作成功", event=event)
                logger.info(f"踢人操作成功")
        else:
            await kick.finish("不能含有@全体成员")
