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
    llm_provider: str = "anthropic"  # anthropic | gemini | groq
    llm_model: str = ""  # empty -> provider default (see app/llm/client.py)
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    sim_paused: bool = False
    # Multi-agent layer
    rootiq_execution_enabled: bool = True  # False -> live-lab remediation becomes a dry run
    agent_timeout_s: float = 8.0
    guardrail_max_executions: int = 5  # per 5 minutes
    verify_grace_s: float = 30.0  # after the 15 s recovery clock, wait up to this long for the playbook criteria
    rag_min_score: float = 0.10
    kb_root: str = ""  # folder holding docs/ and lab/configs (auto-detected when empty)


settings = Settings()
