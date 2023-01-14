import nonebot
from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from .utils import At, MsgText, banSb, change_s_title, fi, log_fi, sd

su = nonebot.get_driver().config.superusers


ban = on_command("ban", aliases={"禁言"}, priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@ban.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    #禁言 @user 禁言
    """
    try:
        msg = MsgText(event.json()).replace(' ', '').replace('禁言', '')
        time = int(''.join(map(str, list(map(lambda x: int(x), filter(lambda x: x.isdigit(), msg))))))
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
            await log_fi(matcher, '禁言操作成功' if time is not None else '用户已被禁言随机时')
        except ActionFailed:
            await fi(matcher, '权限不足')


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
                    group_id=gid,
                    user_id=int(user_),
                    card=msg.split()[-1:][0]
                )
            await log_fi(matcher, '改名片操作成功')
        except ActionFailed:
            await fi(matcher, '权限不足')

title = on_command('头衔', priority=1, block=True)


@title.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    #头衔 @user  xxx  给某人头衔
    """
    # msg = str(event.get_message())
    msg = MsgText(event.json())
    s_title = msg.replace(' ', '').replace('头衔', '', 1)
    sb = At(event.json())
    gid = event.group_id
    uid = event.user_id
    if not sb or (len(sb) == 1 and sb[0] == uid):
        await change_s_title(bot, matcher, gid, uid, s_title)
    elif sb:
        if 'all' not in sb:
            if uid in su or (str(uid) in su):
                for qq in sb:
                    await change_s_title(bot, matcher, gid, int(qq), s_title)
            else:
                await fi(matcher, '管理才可以更改他人头衔，更改自己头衔请直接使用【头衔 xxx】')
        else:
            await fi(matcher, '不能含有@全体成员')

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
        if 'all' not in sb:
            try:
                for qq in sb:
                    if qq == event.user_id:
                        await sd(matcher, '你在玩一种很新的东西，不能踢自己!')
                        continue
                    if qq in su or (str(qq) in su):
                        await sd(matcher, '超级用户不能被踢')
                        continue
                    await bot.set_group_kick(
                        group_id=gid,
                        user_id=int(qq),
                        reject_add_request=False
                    )
                await log_fi(matcher, '踢人操作执行完毕')
            except ActionFailed:
                await fi(matcher, '权限不足')
        await fi(matcher, '不能含有@全体成员')
