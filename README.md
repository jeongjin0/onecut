# Onecut

Professional agent for a messy workday.

Onecut reads a day log, keeps exactly one next action, and defers everything else. It does not chat. It does not emit a plan.

Built for Amazon Agents for Humans 2026, Professional track, with the Strands Agents SDK.

This is new contest work. It is not a Closeout reskin. Closeout overnight-operates CI and GitHub issues. Onecut cuts a founder's scattered day down to one physical next step.

## Quick start

python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m onecut.cli run --fixture fixtures/scattered.json

## Demo loop

- Cut a scattered day: leftover promise wins because interrupts already broke the day.
- Protect deep work: if the calendar already named deep work and nothing is leftover, keep that block.

Synthetic fixtures only. No live user history.

## License

MIT
