# Onecut — Devpost submission draft

## Project name
Onecut

## Tagline
A professional agent that cuts a messy workday down to exactly one next action.

## Track
Professional Agents

## The problem
Solo founders and researchers do not fail from a lack of tasks. They fail because a broken day keeps sprouting new work. Chatbots make the pile longer. Calendar apps keep every block. The useful move is usually to keep one leftover promise and defer the rest.

## Who it is for
A solo founder or researcher who already knows the work, but cannot see the next physical step through Slack, inbox, meetings, and leftover promises.

## Why it matters
Judgment is the scarce resource. Onecut protects it. It reads a day log, refuses a plan, and returns one action with a first physical step. Everything else is named as deferred, not forgotten.

## How it works
1. A Strands Agent collects the day log.
2. If the user asked for a full plan, it calls `refuse_full_plan`.
3. It calls `cut_to_one_action`.
4. A deterministic policy chooses the cut: leftover promises beat new work; a broken day keeps the first promise; an intact deep-work block is protected.
5. The UI shows the day with KEEP / DEFER marks and the one remaining step.

The local demo uses a scripted Strands model so the loop can run without Bedrock. The Agent still emits and executes real tool calls. Swap `ONECUT_MODEL=bedrock` when AWS credits land. AgentCore is optional and not required for this submission.

## Built with
- AWS Strands Agents SDK
- FastAPI demo surface
- Deterministic policy + synthetic fixtures
- MIT license

## Links
- Repo: https://github.com/jeongjin0/onecut
- Live demo: http://macbookpro.tailb72f07.ts.net:8782/
- Architecture: docs/architecture.md

## AWS Builder ID
Paste the owner Builder ID at submit time.

## What this is not
Not Closeout. Not a chatbot. Not a day planner. Not live user data.
