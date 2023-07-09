# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    react_group_id: int # 响应群id
    react_user_id: list[int] # 响应用户id
    mcsm_api_url: str
    mcsm_api_key: str


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)



