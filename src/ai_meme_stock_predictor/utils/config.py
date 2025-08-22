import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

class Settings(BaseSettings):
    alphavantage_api_key: str = Field(default="", env="ALPHAVANTAGE_API_KEY")
    reddit_client_id: str = Field(default="", env="REDDIT_CLIENT_ID")
    reddit_client_secret: str = Field(default="", env="REDDIT_CLIENT_SECRET")
    reddit_user_agent: str = Field(default="meme-stock-agent", env="REDDIT_USER_AGENT")
    twitter_bearer_token: str = Field(default="", env="TWITTER_BEARER_TOKEN")
    portia_api_key: str = Field(default="", env="PORTIA_API_KEY")
    env: str = Field(default="dev", env="ENV")

    class Config:
        case_sensitive = False

settings = Settings()
