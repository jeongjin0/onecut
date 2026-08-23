from pathlib import Path
from onecut.config import Settings
from onecut.engine import run_deterministic, load_day
from onecut.policy import cut_from_day
ROOT = Path(__file__).resolve().parents[1]

def settings(tmp_path, fixture):
    return Settings(onecut_mode="fixtures", onecut_fixture_path=ROOT/"fixtures"/fixture, onecut_data_dir=tmp_path)

def test_scattered_day_keeps_first_promise(tmp_path):
    receipt = run_deterministic(settings(tmp_path, "scattered.json"))
    assert "one-page SemDS status" in receipt.cut.title
    assert any("never assigns two" in x.lower() or "exactly one next action" in x.lower() for x in receipt.cut.refused)

def test_protected_day_keeps_calendar_block(tmp_path):
    cut = cut_from_day(load_day(ROOT/"fixtures"/"protected.json"))
    assert "Protect" in cut.title
    receipt = run_deterministic(settings(tmp_path, "protected.json"))
    assert "Protect" in receipt.cut.title
