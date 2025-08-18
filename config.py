"""Config and Secrets"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class YoutubeAPISettings(BaseSettings):
    key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="YOUTUBE_API_",
    )


class Settings(BaseSettings):
    youtube: YoutubeAPISettings = YoutubeAPISettings() # type: ignore

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

SETTINGS = Settings()

if __name__ == "__main__":
    settings = Settings()
    print(settings.youtube.key)  