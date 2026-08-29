# Onecut

Professional agent for a messy workday.

Onecut reads a day log, keeps exactly one next action, and defers everything else. It does not chat. It does not emit a plan.

Built for Amazon Agents for Humans 2026, Professional track, with the Strands Agents SDK.

This is new contest work. It is not a Closeout reskin. Closeout overnight-operates CI and GitHub issues. Onecut cuts a founder's scattered day down to one physical next step.

## Quick start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m onecut.cli run --fixture fixtures/scattered.json
```

## Demo loop

- Cut a scattered day: leftover promise wins because interrupts already broke the day.
- Protect deep work: if the calendar already named deep work and nothing is leftover, keep that block.
- Ask for a full plan: Strands calls `refuse_full_plan`, then still returns one cut.

The live demo runs a real Strands Agent loop. The local model is scripted so the demo does not need Bedrock. Policy remains deterministic.

Synthetic fixtures only. No live user history.

## License

MIT
