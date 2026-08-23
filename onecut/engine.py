from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from onecut.config import Settings
from onecut.models import DayLog, RunReceipt
from onecut.policy import cut_from_day


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_day(path: Path) -> DayLog:
    return DayLog.model_validate_json(Path(path).read_text())


def save_receipt(settings: Settings, receipt: RunReceipt) -> Path:
    path = settings.receipts_dir / f"{receipt.run_id}.json"
    payload = json.dumps(receipt.model_dump(mode="json"), indent=2) + chr(10)
    path.write_text(payload)
    (settings.receipts_dir / "latest.json").write_text(path.read_text())
    return path


def run_deterministic(settings: Settings, day: DayLog | None = None) -> RunReceipt:
    started = utc_now()
    if day is None:
        day = load_day(settings.onecut_fixture_path)
    cut = cut_from_day(day)
    receipt = RunReceipt(
        run_id=utc_now().replace(":", "").replace("-", "") + "-" + uuid.uuid4().hex[:8],
        started_at=started,
        finished_at=utc_now(),
        mode=settings.onecut_mode,
        day=day,
        cut=cut,
        status="ok",
    )
    save_receipt(settings, receipt)
    return receipt
