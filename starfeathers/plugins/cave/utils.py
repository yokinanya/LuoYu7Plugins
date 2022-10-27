import os
import sys
import pathlib
import random
import sqlite3
from nonebot.adapters.onebot.v11.message import Message

db_dir = pathlib.Path(os.path.abspath(sys.path[0])).joinpath('starfeathers/data')
cave_db = os.path.join(db_dir, "cave.db")


def get_cave():
    conn = sqlite3.connect(cave_db)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM cave')
        values = random.choice(cursor.fetchall())
        id = values[0]
        cave_msg = values[1]
        uploader = values[2]
        if uploader == None:
            uploader = "匿名投稿"
    except:
        id = 0
        cave_msg = "暂无回声洞数据\n[CQ:image,file=https://s2.loli.net/2022/09/09/OkrCoWV8nbQpL9d.png]"
        uploader = "铃星羽"
    cursor.close()
    conn.close()
    return id, cave_msg, uploader


def write_db(cave_msg: str, uploader: str):
    conn = sqlite3.connect(cave_db)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO cave (cave_msg, uploader) VALUES('{cave_msg}', '{uploader}');")
        conn.commit()
        return_msg = "数据存储成功"
    except:
        return_msg = "数据存储失败"
    cursor.close()
    conn.close()
    return return_msg


def generate_cave():
    id, cave_msg, uploader = get_cave()
    message = Message(
        f'【{id}】回声洞\
        \n{cave_msg}\
        \n—— {uploader}'
    )
    return message