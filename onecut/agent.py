from __future__ import annotations

from onecut.config import Settings, load_settings
from onecut.engine import load_day
from onecut.models import Cut
from onecut.policy import REFUSED_CHAT, REFUSED_MULTITASK, REFUSED_PLAN, cut_from_day


DEFAULT_PROMPT = "Cut this messy workday down to exactly one next action. Do not emit a plan."
PLAN_PROMPT = "Give me a full day plan with every leftover on the calendar."

INSTRUCTION = """You are Onecut, a professional agent for a solo founder.

You do not chat. You do not emit a day plan. You return exactly one next action.

On every request:
1. Call collect_day_log.
2. If the user asked for a full plan, call refuse_full_plan.
3. Call cut_to_one_action.
4. Stop.

Never invent a second action.
"""


_TRACE: list[str] = []
_LAST_CUT: Cut | None = None


def reset_run_state() -> None:
    _TRACE.clear()
    global _LAST_CUT
    _LAST_CUT = None


def collect_day_log() -> dict:
    """Collect yesterday/today's messy work log.

    In fixtures mode this reads a synthetic founder day, not live user data.
    """
    settings = load_settings()
    day = load_day(settings.onecut_fixture_path)
    _TRACE.append("collect_day_log")
    return day.model_dump(mode="json")


def cut_to_one_action() -> dict:
    """Choose exactly one next action and defer everything else."""
    settings = load_settings()
    day = load_day(settings.onecut_fixture_path)
    cut = cut_from_day(day)
    global _LAST_CUT
    _LAST_CUT = cut
    _TRACE.append("cut_to_one_action")
    return cut.model_dump(mode="json")


def refuse_full_plan() -> dict:
    """Refuse multi-item plans and chatty coaching."""
    _TRACE.append("refuse_full_plan")
    return {
        "allowed": False,
        "reason": " ".join([REFUSED_CHAT, REFUSED_PLAN, REFUSED_MULTITASK]),
    }


def build_strands_agent(model=None):
    from strands import Agent, tool
    from strands.handlers.callback_handler import null_callback_handler

    @tool(name="collect_day_log")
    def collect_day_log_tool() -> dict:
        """Collect yesterday/today's messy work log."""
        return collect_day_log()

    @tool(name="cut_to_one_action")
    def cut_to_one_action_tool() -> dict:
        """Choose exactly one next action and defer everything else."""
        return cut_to_one_action()

    @tool(name="refuse_full_plan")
    def refuse_full_plan_tool() -> dict:
        """Refuse multi-item plans and chatty coaching."""
        return refuse_full_plan()

    return Agent(
        name="onecut",
        system_prompt=INSTRUCTION,
        tools=[collect_day_log_tool, cut_to_one_action_tool, refuse_full_plan_tool],
        model=model,
        callback_handler=null_callback_handler,
    )


def _select_model(settings: Settings):
    if settings.onecut_model in {"local", "fixtures", "policy"}:
        from onecut.local_model import OnecutLocalModel

        return OnecutLocalModel()
    from strands.models.bedrock import BedrockModel

    return BedrockModel()


def run_strands(settings: Settings, prompt: str | None = None) -> dict:
    reset_run_state()
    model = _select_model(settings)
    agent = build_strands_agent(model=model)
    result = agent(prompt or DEFAULT_PROMPT)
    if _LAST_CUT is None:
        raise RuntimeError("Strands agent finished without calling cut_to_one_action.")
    return {
        "cut": _LAST_CUT,
        "tool_trace": list(_TRACE),
        "agent_text": str(result).strip(),
        "model": getattr(model, "config", {}).get("model_id", settings.onecut_model),
    }
