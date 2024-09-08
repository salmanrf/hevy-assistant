from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SERVER_PORT: int = Field(..., env="SERVER_PORT")
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    MONGODB_NAME: str = Field(..., env="MONGODB_NAME")

    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(..., env="OPENAI_MODEL")
    OPENAI_TEMPERATURE: str = Field(..., env="OPENAI_TEMPERATURE")


config = Config()
