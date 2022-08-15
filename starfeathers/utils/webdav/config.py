from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    webdav_url: str = "api_url"
    webdav_username: str = "api_username"
    webdav_token: str = "api_token"