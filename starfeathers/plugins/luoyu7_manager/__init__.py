import requests
from nonebot import get_driver, logger, on_command, on_notice
from nonebot.adapters.onebot.v11 import ActionFailed, Bot, GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.event import (
    GroupIncreaseNoticeEvent,
    GroupMessageEvent,
)
from nonebot.adapters.onebot.v11.permission import GROUP, GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .config import plugin_config
from .utils import At, MsgText, banSb, change_s_title, fi, log_fi, sd

su = get_driver().config.superusers
checkban_enabled = plugin_config.checkban_enable

ban = on_command(
    "ban",
    aliases={"禁言"},
    priority=1,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
)


@ban.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    #禁言 @user 禁言
    """
    try:
        msg = MsgText(event.json()).replace(" ", "").replace("禁言", "")
        time = int(
            "".join(
                map(
                    str, list(map(lambda x: int(x), filter(lambda x: x.isdigit(), msg)))
                )
            )
        )
        # 提取消息中所有数字作为禁言时间
    except ValueError:
        time = None
    sb = At(event.json())
    gid = event.group_id
    if sb:
        baning = banSb(gid, ban_list=sb, time=time)
        try:
            async for baned in baning:
                if baned:
                    await baned
            await log_fi(matcher, "禁言操作成功" if time is not None else "用户已被禁言随机时")
        except ActionFailed:
            await fi(matcher, "权限不足")


change = on_command(
    "change",
    aliases={"改名"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
)


@change.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    #改名 @user xxx 改群昵称
    """
    msg = str(event.get_message())
    logger.info(msg.split())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        try:
            for user_ in sb:
                await bot.set_group_card(
                    group_id=gid, user_id=int(user_), card=msg.split()[-1:][0]
                )
            await log_fi(matcher, "改名片操作成功")
        except ActionFailed:
            await fi(matcher, "权限不足")


title = on_command("头衔", priority=1, block=True)


@title.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    #头衔 @user  xxx  给某人头衔
    """
    # msg = str(event.get_message())
    msg = MsgText(event.json())
    s_title = msg.replace(" ", "").replace("头衔", "", 1)
    sb = At(event.json())
    gid = event.group_id
    uid = event.user_id
    if not sb or (len(sb) == 1 and sb[0] == uid):
        await change_s_title(bot, matcher, gid, uid, s_title)
    elif sb:
        if "all" not in sb:
            if uid in su or (str(uid) in su):
                for qq in sb:
                    await change_s_title(bot, matcher, gid, int(qq), s_title)
            else:
                await fi(matcher, "管理才可以更改他人头衔，更改自己头衔请直接使用【头衔 xxx】")
        else:
            await fi(matcher, "不能含有@全体成员")


kick = on_command(
    "kick",
    aliases={"踢人"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
)


@kick.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    #踢人 @user 踢出某人
    """
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if "all" not in sb:
            try:
                for qq in sb:
                    if qq == event.user_id:
                        await sd(matcher, "你在玩一种很新的东西，不能踢自己!")
                        continue
                    if qq in su or (str(qq) in su):
                        await sd(matcher, "超级用户不能被踢")
                        continue
                    await bot.set_group_kick(
                        group_id=gid, user_id=int(qq), reject_add_request=False
                    )
                await log_fi(matcher, "踢人操作执行完毕")
            except ActionFailed:
                await fi(matcher, "权限不足")
        await fi(matcher, "不能含有@全体成员")


check_isban = on_notice(priority=90, block=False)

checkban_enable = [1067555292, 1030902782, 1128216585, 553717146]


@check_isban.handle()
async def handle_group_increase(
    bot: Bot, matcher: Matcher, event: GroupIncreaseNoticeEvent
):
    user_id = event.user_id
    group_id = event.group_id
    api = "https://api.yokinanya.icu/qqban/"
    if group_id in checkban_enable:
        url = api + user_id
        result = requests.get(url).json()
        if result["status"] == 200:
            reason = result["reason"]
            type = result["type"]
            msg = f"新成员 {user_id} 处于黑名单中\n拉黑理由：{reason}\n标签：{type}"
            await check_isban.finish(msg)
        elif result["status"] == 404:
            pass


check_isban_c = on_command(
    "checkisban",
    aliases={"云黑查询"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
)


@check_isban_c.handle()
async def handle_first_receive(
    state: T_State,
    event: GroupMessageEvent,
    matcher: Matcher,
    args: Message = CommandArg(),
):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        state.update({"qqid": plain_text})


@check_isban_c.got("qqid", prompt="请输入你要查询的QQ号")
async def handle_check(bot: Bot, event: GroupMessageEvent, qqid: str = ArgStr("qqid")):
    api = "https://api.yokinanya.icu/qqban/"
    if qqid.isdigit() == False:
        check_isban_c.reject("你输入的不是数字，请重新输入")
    url = api + qqid
    result = requests.get(url).json()
    if result["status"] == 200:
        reason = result["reason"]
        type = result["type"]
        msg = f"查询的 {qqid} 处于黑名单中\n拉黑理由：{reason}\n标签：{type}"
        await check_isban.finish(msg)
    elif result["status"] == 404:
        reason = result["reason"]
        type = result["type"]
        msg = f"查询的 {qqid} 不处于黑名单中\n标签：{type}"
        await check_isban.finish(msg)
