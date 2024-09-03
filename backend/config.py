from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SERVER_PORT: int = Field(..., env="SERVER_PORT")
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    MONGODB_NAME: str = Field(..., env="MONGODB_NAME")


config = Config()
