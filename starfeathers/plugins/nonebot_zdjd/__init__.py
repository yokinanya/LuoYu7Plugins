import base64
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.permission import GROUP, PRIVATE_FRIEND
from nonebot.exception import ParserExit
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg, Depends
from nonebot.rule import ArgumentParser
from nonebot.typing import T_State

import base64

b64 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/="

left_eye = ["o", "0", "O", "Ö"]
mouse = ["w", "v", ".", "_"]
right_eye = ["o", "0", "O", "Ö"]
table = []

separator = " "


def make_table():
    for i in range(4):
        for j in range(4):
            for k in range(4):
                table.append(left_eye[i] + mouse[j] + right_eye[k])


make_table()


def add_calls(t):
    return t


def human2zdjd(t):
    t = base64.b64encode(t.encode()).decode()
    length = len(t)
    arr = []

    for i in range(length):
        c = t[i]
        if not c == "=":
            n = b64.index(c)
            arr.append(table[n])

    data = separator.join(arr)
    return add_calls(data)


def zdjd2human(t):
    arr = t.split(separator)
    length = len(arr)
    result_arr = []

    for i in range(length):
        c = arr[i]
        if not c:
            continue
        n = table.index(c)
        if n < 0:
            raise ValueError("Invalid zdjd code")
        result_arr.append(b64[n])

    t = "".join(result_arr)
    padding = length % 4
    if padding > 0:
        t += "=" * (4 - padding)
    t = base64.b64decode(t.encode()).decode()
    return t


def isZdjd(t):
    try:
        zdjd2human(t)
        return True
    except:
        return False


def zdjd(t: str, mode: str):
    callback = {"result":""}
    if mode == "zdjd2human":
        callback["isZdjd"] = bool(isZdjd(t))
        if bool(isZdjd(t)) is True:
            human = zdjd2human(t)
            callback["result"] = human
        else:
            callback["result"] = "你输入的是假嘟语，请重新输入"
        return callback
    elif mode == "human2zdjd":
        callback["isZdjd"] = bool(isZdjd(t))
        zdjd = human2zdjd(t)
        callback["result"] = zdjd
        return callback
    elif mode == "auto":
        callback["isZdjd"] = bool(isZdjd(t))
        if isZdjd(t) is True:
            human = zdjd2human(t)
            callback["result"] = human
        else:
            zdjd = human2zdjd(t)
            callback["result"] = zdjd
        return callback
    else:
        return callback


Zdjd = on_command(
    "Zdjd",
    aliases={"尊嘟假嘟", "zdjd"},
    permission=GROUP | PRIVATE_FRIEND,
    priority=20,
    block=True,
)


def source_target_parser() -> ArgumentParser:
    """argument parser"""
    parser = ArgumentParser(
        prog="Translate arguments parser", description="Parse translate arguments"
    )
    parser.add_argument("-m", "--mode", type=str, default="auto")
    parser.add_argument("word", nargs="*")
    return parser


@Depends
async def parse_translate_args(
    matcher: Matcher, state: T_State, cmd_arg: Message = CommandArg()
):
    args = cmd_arg.extract_plain_text().strip().split()
    try:
        parse_result = source_target_parser().parse_args(args=args)
        state.update(
            {
                "mode": parse_result.mode,
                "word": " ".join(parse_result.word),
            }
        )
    except ParserExit:
        await matcher.finish("无效的翻译参数QAQ")


@Zdjd.handle(parameterless=[parse_translate_args])
async def handle_parse_expression(state: T_State):
    """首次运行时解析命令参数"""
    word = state.get("word", "")
    if not word.strip():
        state.pop("word")


@Zdjd.got("word", prompt="请发送需要翻译的内容:")
async def handle_translate(
    matcher: Matcher, state: T_State, word: str = ArgStr("word")
):
    mode: str = state.get("mode")
    word = word.strip()
    if not word:
        await matcher.reject(f"你没有发送任何内容呢, 请重新发送你想要翻译的内容:")

    translate = zdjd(t=word, mode=mode)
    translate_result = translate["result"]
    await matcher.finish(f"翻译结果:\n\n{translate_result}")
