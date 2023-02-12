import nonebot
from nonebot import logger, on_command, on_request, on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed, GroupRequestEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.typing import T_State
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


group_apply = on_request()
agree_apply = on_regex(pattern=r'^同意$', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
disagree_apply = on_regex(pattern=r'^拒绝(：|:|,|，|.)?', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
enable_group = [1128216585, 466432629, 1067555292]


# 入群申请消息
@group_apply.handle()
async def apply_msg(bot: Bot, event: GroupRequestEvent, state: T_State):
    if event.group_id in enable_group:
        global apply_id
        apply_id = event.user_id
        message = event.comment  # 获取验证信息
        global flag_id
        flag_id = event.flag  # 申请进群的flag
        global type_id
        type_id = event.sub_type  # 请求信息的类型
        await group_apply.finish(message=f'收到进群申请\nQQ:{apply_id}\n验证消息:{message}\n【同意/拒绝】')
    else:
        logger.info(f'群{event.group_id}收到进群申请，但未启用Bot处理')


# 同意申请入群
@agree_apply.handle()
async def agree(bot: Bot, event: GroupMessageEvent, state: T_State):
    try:
        await bot.set_group_add_request(flag=flag_id, sub_type=type_id, approve=True)
        await agree_apply.finish(message=f'{apply_id}的入群申请已处理')
    except ActionFailed:
        await agree_apply.finish("权限不足，或已处理")


# 拒绝入群
@disagree_apply.handle()
async def sn(bot: Bot, event: GroupMessageEvent, state: T_State):
    raw_msg = event.raw_message
    reason='机器人自动审批，如有误判请联系群主或其他管理员'
    split_word = [":", ",", "：", "，", "."]
    for word in split_word:
        if word in raw_msg:
            raw_msg = raw_msg.replace(word, ":")
            break
    if raw_msg.find(":") != -1:
        reason = raw_msg.split(":")[-1]
    else:
        reason = reason
    await bot.set_group_add_request(flag=flag_id, sub_type=type_id, approve=False, reason=reason)
    await agree_apply.finish(message=f'{apply_id}的入群申请已处理')
