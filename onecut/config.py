from pathlib import Path
from contextvars import ContextVar

from pydantic_settings import BaseSettings, SettingsConfigDict

_ACTIVE: ContextVar["Settings | None"] = ContextVar("onecut_settings", default=None)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    onecut_mode: str = "fixtures"
    onecut_fixture_path: Path = Path("fixtures/scattered.json")
    onecut_data_dir: Path = Path("data")
    onecut_bind: str = "127.0.0.1"
    port: int = 8782
    onecut_runner: str = "agent"
    onecut_model: str = "local"

    @property
    def receipts_dir(self) -> Path:
        path = self.onecut_data_dir / "receipts"
        path.mkdir(parents=True, exist_ok=True)
        return path


def load_settings() -> Settings:
    return _ACTIVE.get() or Settings()


def use_settings(settings: Settings):
    return _ACTIVE.set(settings)


def reset_settings(token) -> None:
    _ACTIVE.reset(token)
