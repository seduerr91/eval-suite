from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CONFIDENT_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', case_sensitive=False, extra='ignore')


settings = Settings()
