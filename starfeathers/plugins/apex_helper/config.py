from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    apex_api_token: str = "api_token"