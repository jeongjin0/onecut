from __future__ import annotations

from onecut.config import load_settings
from onecut.engine import load_day, run_deterministic
from onecut.policy import REFUSED_CHAT, REFUSED_MULTITASK, REFUSED_PLAN, cut_from_day


INSTRUCTION = """You are Onecut, a professional agent for a solo founder.

You do not chat. You do not emit a day plan. You return exactly one next action.

On every request:
1. Call collect_day_log.
2. Call cut_to_one_action.
3. Stop.

If the user asks for a full plan, refuse and still return one cut.
"""


def collect_day_log() -> dict:
    """Collect yesterday/today's messy work log.

    In fixtures mode this reads a synthetic founder day, not live user data.
    """
    settings = load_settings()
    day = load_day(settings.onecut_fixture_path)
    return day.model_dump(mode="json")


def cut_to_one_action() -> dict:
    """Choose exactly one next action and defer everything else."""
    settings = load_settings()
    day = load_day(settings.onecut_fixture_path)
    cut = cut_from_day(day)
    return cut.model_dump(mode="json")


def refuse_full_plan() -> dict:
    """Refuse multi-item plans and chatty coaching."""
    return {
        "allowed": False,
        "reason": " ".join([REFUSED_CHAT, REFUSED_PLAN, REFUSED_MULTITASK]),
    }


def build_strands_agent():
    from strands import Agent, tool

    @tool
    def collect_day_log_tool() -> dict:
        """Collect yesterday/today's messy work log."""
        return collect_day_log()

    @tool
    def cut_to_one_action_tool() -> dict:
        """Choose exactly one next action and defer everything else."""
        return cut_to_one_action()

    @tool
    def refuse_full_plan_tool() -> dict:
        """Refuse multi-item plans and chatty coaching."""
        return refuse_full_plan()

    return Agent(
        name="onecut",
        system_prompt=INSTRUCTION,
        tools=[collect_day_log_tool, cut_to_one_action_tool, refuse_full_plan_tool],
    )
