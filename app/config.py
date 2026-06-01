from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic läser automatiskt dessa från .env filen
    openrouter_api_key: str
    openrouter_model: str = "openai/gpt-5.4-mini"
    bitcoin_data_path: str = "data/btcusd-daily.csv"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()