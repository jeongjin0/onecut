from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Block(BaseModel):
    start: str
    end: str
    title: str
    kind: Literal["deep_work", "meeting", "admin", "interrupt", "break"]
    note: str = ""


class DayLog(BaseModel):
    as_of: str
    person: str
    role: str
    calendar_window: str
    blocks: list[Block] = Field(default_factory=list)
    leftover_promises: list[str] = Field(default_factory=list)


class Cut(BaseModel):
    title: str
    why_this_one: str
    first_physical_step: str
    deferred: list[str] = Field(default_factory=list)
    refused: list[str] = Field(default_factory=list)
    kept_titles: list[str] = Field(default_factory=list)
    rule: str = ""


class RunReceipt(BaseModel):
    run_id: str
    started_at: str
    finished_at: str
    mode: str
    day: DayLog
    cut: Cut | None = None
    status: Literal["ok", "error"] = "ok"
    error: str = ""
    runner: str = "deterministic"
    model: str = "policy"
    tool_trace: list[str] = Field(default_factory=list)
    agent_text: str = ""
    prompt: str = ""
