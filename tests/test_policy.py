from pathlib import Path
from onecut.config import Settings
from onecut.engine import run_cut, run_deterministic, load_day
from onecut.policy import cut_from_day
from onecut.agent import PLAN_PROMPT

ROOT = Path(__file__).resolve().parents[1]


def settings(tmp_path, fixture, runner="deterministic"):
    return Settings(
        onecut_mode="fixtures",
        onecut_fixture_path=ROOT / "fixtures" / fixture,
        onecut_data_dir=tmp_path,
        onecut_runner=runner,
        onecut_model="local",
    )


def test_scattered_day_keeps_first_promise(tmp_path):
    receipt = run_deterministic(settings(tmp_path, "scattered.json"))
    assert "one-page SemDS status" in receipt.cut.title
    assert any("never assigns two" in x.lower() or "exactly one next action" in x.lower() for x in receipt.cut.refused)


def test_protected_day_keeps_calendar_block(tmp_path):
    cut = cut_from_day(load_day(ROOT / "fixtures" / "protected.json"))
    assert "Protect" in cut.title
    receipt = run_deterministic(settings(tmp_path, "protected.json"))
    assert "Protect" in receipt.cut.title


def test_strands_loop_collects_then_cuts(tmp_path):
    receipt = run_cut(settings(tmp_path, "scattered.json", runner="agent"))
    assert receipt.status == "ok"
    assert receipt.runner == "strands"
    assert receipt.tool_trace[:2] == ["collect_day_log", "cut_to_one_action"]
    assert "one-page SemDS status" in receipt.cut.title
    assert receipt.cut.deferred


def test_strands_refuses_a_full_plan(tmp_path):
    receipt = run_cut(settings(tmp_path, "scattered.json", runner="agent"), prompt=PLAN_PROMPT)
    assert receipt.status == "ok"
    assert "refuse_full_plan" in receipt.tool_trace
    assert receipt.tool_trace[-1] == "cut_to_one_action"
    assert "one-page SemDS status" in receipt.cut.title
