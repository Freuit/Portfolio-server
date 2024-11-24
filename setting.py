from pydantic_settings import BaseSettings, SettingsConfigDict
import sys

class Settings(BaseSettings):
    WORKSPACE: str

    NOTION_KEY: str
    NOTION_PROJECT_KEY: str
    NOTION_SKILL_KEY: str
    isdev: bool = sys.argv[1] == 'dev'

    model_config = SettingsConfigDict(env_file="./.env.dev" if isdev else "./.env.prod")


setting = Settings()