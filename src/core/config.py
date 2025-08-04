from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CONFIDENT_API_KEY: str

    # LLM model settings
    GENERATION_LLM: str = "gpt-4.1"  # model to be tested for generation
    EVALUATION_LLM: str = "gpt-4.1"  # evaluation model

    # Prompt settings
    PROMPT_VERSION: str = "v2"  # version of the prompt to use for generation

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
