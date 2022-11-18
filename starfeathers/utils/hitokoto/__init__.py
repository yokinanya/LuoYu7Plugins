import requests

HITOKOTO_API = "https://v1.hitokoto.cn"


def hitokoto_raw(c: list = ["a"], encode: str = "json", charset: str = "utf-8",  min_length: int = 0, max_length: int = 30):
    HITOKOTO_PARAMS = {"c": c, "encode": encode, "charset": charset, "min_length": min_length, "max_length": max_length}
    jsonobj = requests.get(HITOKOTO_API, params=HITOKOTO_PARAMS).json()
    try:
        hitokoto = jsonobj["hitokoto"]
        from_where = jsonobj["from"]
        from_who = jsonobj["from_who"]
        if from_where is None:
            from_raw = f"——{from_who}"
        elif from_who is None:
            from_raw = f"——{from_where}"
        else:
            from_raw = f"——{from_who} / {from_where}"
        hitokoto_raw = f"{hitokoto}\n{from_raw}"
    except:
        hitokoto_raw = "读取数据失败了的说……_(:з」∠)_"
    return hitokoto_raw
