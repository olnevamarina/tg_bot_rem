from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # No hardcoded defaults! Pydantic raises an error on boot if these are missing in .env
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///./reminders.db"

    @property
    def telegram_api_url(self) -> str:
        return f"https://api.telegram.org/bot{self.bot_token}"

    # Pydantic v2 configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()