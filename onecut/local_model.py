"""Deterministic Strands model for the contest demo.

The policy is still the source of truth. This model exists so the live demo
path actually runs a Strands Agent loop: collect the day, cut to one action,
then stop. Bedrock is not required for the local/tailnet demo.
"""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator, AsyncIterable
from typing import Any, TypeVar
from uuid import uuid4

from pydantic import BaseModel
from strands.models.model import Model
from strands.types.content import Messages, SystemContentBlock
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolChoice, ToolSpec

T = TypeVar("T", bound=BaseModel)

COLLECT = "collect_day_log"
CUT = "cut_to_one_action"
REFUSE = "refuse_full_plan"


def _last_user_text(messages: Messages) -> str:
    for message in reversed(messages):
        if message.get("role") != "user":
            continue
        parts: list[str] = []
        for block in message.get("content", []):
            if "text" in block and block["text"]:
                parts.append(str(block["text"]))
        if parts:
            return " ".join(parts)
    return ""


def _tool_names(tool_specs: list[ToolSpec] | None) -> set[str]:
    return {spec["name"] for spec in (tool_specs or [])}


def _used_tool(messages: Messages, name: str) -> bool:
    for message in messages:
        if message.get("role") != "assistant":
            continue
        for block in message.get("content", []):
            tool = block.get("toolUse")
            if tool and tool.get("name") == name:
                return True
    return False


def _wants_plan(text: str) -> bool:
    lowered = text.lower()
    return any(
        token in lowered
        for token in ("full plan", "full day", "todo list", "to-do list", "every leftover")
    )


class OnecutLocalModel(Model):
    """Tiny scripted model that only knows the Onecut tool sequence."""

    def __init__(self) -> None:
        self.config: dict[str, Any] = {"model_id": "onecut-local", "context_window_limit": 8192}

    def update_config(self, **model_config: Any) -> None:
        self.config.update(model_config)

    def get_config(self) -> dict[str, Any]:
        return self.config

    def structured_output(
        self, output_model: type[T], prompt: Messages, system_prompt: str | None = None, **kwargs: Any
    ) -> AsyncGenerator[dict[str, T | Any], None]:
        raise NotImplementedError("OnecutLocalModel does not implement structured output.")

    async def stream(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
        *,
        tool_choice: ToolChoice | None = None,
        system_prompt_content: list[SystemContentBlock] | None = None,
        invocation_state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[StreamEvent]:
        names = _tool_names(tool_specs)
        prompt = _last_user_text(messages)
        collected = _used_tool(messages, COLLECT)
        cut = _used_tool(messages, CUT)
        refused = _used_tool(messages, REFUSE)

        yield {"messageStart": {"role": "assistant"}}

        if COLLECT in names and not collected:
            async for event in _tool_call(COLLECT, {}):
                yield event
            return

        if REFUSE in names and _wants_plan(prompt) and not refused:
            async for event in _tool_call(REFUSE, {}):
                yield event
            return

        if CUT in names and not cut:
            async for event in _tool_call(CUT, {}):
                yield event
            return

        text = "Cut complete. One next action. Everything else is deferred."
        yield {"contentBlockStart": {"start": {}}}
        yield {"contentBlockDelta": {"delta": {"text": text}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}
        yield {
            "metadata": {
                "usage": {"inputTokens": 1, "outputTokens": 1, "totalTokens": 2},
                "metrics": {"latencyMs": 1},
            }
        }


async def _tool_call(name: str, payload: dict[str, Any]) -> AsyncIterable[StreamEvent]:
    yield {
        "contentBlockStart": {
            "start": {"toolUse": {"name": name, "toolUseId": f"tooluse_{uuid4().hex[:24]}"}}
        }
    }
    yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps(payload)}}}}
    yield {"contentBlockStop": {}}
    yield {"messageStop": {"stopReason": "tool_use"}}
    yield {
        "metadata": {
            "usage": {"inputTokens": 1, "outputTokens": 1, "totalTokens": 2},
            "metrics": {"latencyMs": 1},
        }
    }
