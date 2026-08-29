# Onecut 5-minute demo script

English voiceover. Screen recording only. No camera.

0:00-0:25 Problem.
A solo founder wakes up to Slack, inbox, a professor promise, and three leftovers. Chatbots add a plan. Onecut cuts the day to one physical next step.

0:25-0:50 Who and why.
For people who already know the work. The scarce resource is judgment, not more tasks. Track: Professional Agents.

0:50-1:20 Architecture.
Strands Agent. Tools: collect_day_log, refuse_full_plan, cut_to_one_action. Deterministic policy is the source of truth. Local model runs the same loop without Bedrock.

1:20-2:40 Live cut.
Open http://macbookpro.tailb72f07.ts.net:8782/
Click "Cut the scattered day".
Show KEEP on the professor promise, DEFER on Slack/inbox/intern/Steam copy.
Read the first physical step: open a 25-minute timer and send the one-page SemDS status.
Show the tool trace: collect_day_log → cut_to_one_action.

2:40-3:20 Protect.
Click "Protect deep work".
The calendar already named the block. The cut is to keep it, not add more.

3:20-4:10 Refuse a plan.
Click "Ask for a full plan".
Show refuse_full_plan in the trace, then still one cut. No second action.

4:10-4:50 Why it matters / close.
One leftover promise restores trust. A plan would hide that. Public MIT repo, synthetic fixtures, no live user history.
