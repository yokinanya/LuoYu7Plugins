from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Message, ActionFailed, NetworkError, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.typing import T_State
from .utils import isNum, get_suit, zip_suit

getsuit = on_command('getsuit', aliases={'获取装扮', '装扮'}, permission=GROUP, priority=50, block=True)


@getsuit.handle()
async def handle_first_receive(state: T_State, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if isNum(plain_text):
        state.update({'suit_id': plain_text})


@getsuit.got('suit_id', prompt='请输入你要下载的装扮id：')
async def handle_city(event: GroupMessageEvent, suitid: str = ArgStr('suit_id')):
    if not isNum(suitid):
        getsuit.reject_arg(key='suit_id', prompt='你输入的似乎不是数字，请重新输入')
    else:
        suit_name, final_status = get_suit(suit_id=suitid)
        if not final_status == 0:
            SAVEFILE = zip_suit(suit_name)
            bot = get_bot("3147892066")
            await getsuit.send(f"装扮【{suit_name}】下载成功，正在上传，这可能需要几分钟")
            try:
                await bot.call_api(
                    "upload_group_file",
                    group_id=event.group_id,
                    file=SAVEFILE,
                    name=f'{suit_name}.zip',
                )
            except (ActionFailed, NetworkError) as e:
                if isinstance(e, ActionFailed) and e.info["wording"] == "server" \
                                                                        " requires unsupported ftn upload":
                    await getsuit.finish(message=Message(MessageSegment.text(
                        "[ERROR]  文件上传失败\r\n[原因]  机器人缺少上传文件的权限\r\n[解决办法]"
                        "请将机器人设置为管理员或者允许群员上传文件")))
                elif isinstance(e, NetworkError):
                    pass
                    # await getsuit.finish(message=Message(MessageSegment.text("[ERROR]  文件上传失败\r\n[原因]  上传超时")))
        else:
            await getsuit.finish(f'{suit_name} 下载失败')
