# Onecut architecture

HTTP POST /run or CLI -> day-log fixture -> policy.cut_from_day -> exactly one Cut -> receipt JSON + demo UI

Strands Agents SDK wraps collect_day_log, cut_to_one_action, refuse_full_plan. Deterministic policy is the source of truth.
