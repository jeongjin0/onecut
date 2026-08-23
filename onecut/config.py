from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    onecut_mode: str = "fixtures"
    onecut_fixture_path: Path = Path("fixtures/scattered.json")
    onecut_data_dir: Path = Path("data")
    onecut_bind: str = "127.0.0.1"
    port: int = 8782

    @property
    def receipts_dir(self) -> Path:
        path = self.onecut_data_dir / "receipts"
        path.mkdir(parents=True, exist_ok=True)
        return path


def load_settings() -> Settings:
    return Settings()
