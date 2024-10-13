from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SERVER_PORT: int = Field(..., env="SERVER_PORT")
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    MONGODB_NAME: str = Field(..., env="MONGODB_NAME")

    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(..., env="OPENAI_MODEL")
    OPENAI_TEMPERATURE: str = Field(..., env="OPENAI_TEMPERATURE")
    OPENAI_MAX_OUTPUT_TOKEN: str = Field(..., env="OPENAI_MAX_OUTPUT_TOKEN")

    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(..., env="ANTHROPIC_MODEL")
    ANTHROPIC_TEMPERATURE: str = Field(..., env="ANTHROPIC_TEMPERATURE")
    ANTHROPIC_MAX_OUTPUT_TOKEN: str = Field(..., env="ANTHROPIC_MAX_OUTPUT_TOKEN")


config = Config()
