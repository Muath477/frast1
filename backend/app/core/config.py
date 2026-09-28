from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    rootiq_mode: str = "sim"
    database_url: str = "postgresql+psycopg://rootiq:rootiq@localhost:5432/rootiq"
    topology_path: str = "../configs/topology.json"
    layout_path: str = "../configs/layout.json"
    ingest_token: str = "change-me-ingest"
    lab_agent_url: str = "http://127.0.0.1:9000"
    lab_agent_token: str = "change-me-agent"
    record_events: bool = False
    llm_enabled: bool = False
    anthropic_api_key: str = ""
    llm_model: str = "claude-haiku-4-5-20251001"


settings = Settings()
