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
        runner="deterministic",
        model="policy",
        tool_trace=["cut_from_day"],
    )
    save_receipt(settings, receipt)
    return receipt


def run_agent(settings: Settings, prompt: str | None = None) -> RunReceipt:
    from onecut.agent import run_strands
    from onecut.config import reset_settings, use_settings

    started = utc_now()
    day = load_day(settings.onecut_fixture_path)
    token = use_settings(settings)
    try:
        result = run_strands(settings, prompt=prompt)
        receipt = RunReceipt(
            run_id=utc_now().replace(":", "").replace("-", "") + "-" + uuid.uuid4().hex[:8],
            started_at=started,
            finished_at=utc_now(),
            mode=settings.onecut_mode,
            day=day,
            cut=result["cut"],
            status="ok",
            runner="strands",
            model=result["model"],
            tool_trace=result["tool_trace"],
            agent_text=result["agent_text"],
            prompt=prompt or "",
        )
    except Exception as exc:  # pragma: no cover - surfaced in the demo receipt
        receipt = RunReceipt(
            run_id=utc_now().replace(":", "").replace("-", "") + "-" + uuid.uuid4().hex[:8],
            started_at=started,
            finished_at=utc_now(),
            mode=settings.onecut_mode,
            day=day,
            cut=None,
            status="error",
            error=str(exc),
            runner="strands",
            model=settings.onecut_model,
            prompt=prompt or "",
        )
    finally:
        reset_settings(token)
    save_receipt(settings, receipt)
    return receipt


def run_cut(settings: Settings, prompt: str | None = None) -> RunReceipt:
    if settings.onecut_runner == "deterministic":
        return run_deterministic(settings)
    return run_agent(settings, prompt=prompt)
