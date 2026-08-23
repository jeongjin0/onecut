from __future__ import annotations

from onecut.models import Cut, DayLog

REFUSED_CHAT = "Onecut does not chat. It returns exactly one next action."
REFUSED_PLAN = "Onecut does not emit a full day plan. Everything else is deferred."
REFUSED_MULTITASK = "Onecut never assigns two next actions."


def _interrupt_count(day: DayLog) -> int:
    return sum(1 for block in day.blocks if block.kind == "interrupt")


def _open_deep_work(day: DayLog) -> bool:
    return any(block.kind == "deep_work" for block in day.blocks)


def cut_from_day(day: DayLog) -> Cut:
    interrupts = _interrupt_count(day)
    leftovers = list(day.leftover_promises)
    if leftovers and interrupts >= 2:
        chosen = leftovers[0]
        deferred = leftovers[1:] + [
            block.title for block in day.blocks if block.kind in {"admin", "interrupt"}
        ]
        return Cut(
            title=chosen,
            why_this_one=(
                f"{interrupts} interrupts already broke the day. "
                "The first leftover promise is the only action that restores trust."
            ),
            first_physical_step=f"Open a 25-minute timer and do only: {chosen}",
            deferred=deferred,
            refused=[REFUSED_CHAT, REFUSED_PLAN, REFUSED_MULTITASK],
        )
    if leftovers:
        chosen = leftovers[0]
        return Cut(
            title=chosen,
            why_this_one="A promised leftover is still open. Finish that before starting new work.",
            first_physical_step=f"Write the first sentence or first failing test for: {chosen}",
            deferred=leftovers[1:] or ["No second action."],
            refused=[REFUSED_CHAT, REFUSED_PLAN, REFUSED_MULTITASK],
        )
    if _open_deep_work(day):
        deep = next(block for block in day.blocks if block.kind == "deep_work")
        return Cut(
            title=f"Protect {deep.title}",
            why_this_one="The calendar already named deep work. The cut is to keep it, not add more.",
            first_physical_step=f"Silence notifications until {deep.end} and stay on {deep.title}.",
            deferred=[block.title for block in day.blocks if block.kind != "deep_work"],
            refused=[REFUSED_CHAT, REFUSED_PLAN, REFUSED_MULTITASK],
        )
    return Cut(
        title="Stop adding work",
        why_this_one="No leftover promise and no deep-work block. The useful action is to stop.",
        first_physical_step="Close the inbox. Do not start a new thread.",
        deferred=[block.title for block in day.blocks],
        refused=[REFUSED_CHAT, REFUSED_PLAN, REFUSED_MULTITASK],
    )
