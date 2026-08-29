# Onecut architecture

```
HTTP POST /run or CLI
  -> Strands Agent (OnecutLocalModel or Bedrock)
  -> tools: collect_day_log, refuse_full_plan, cut_to_one_action
  -> deterministic policy.cut_from_day
  -> one Cut + receipt JSON + demo UI
```

The Strands loop is the required contest surface. The policy is still the source of truth: leftover promises beat new work, a broken day keeps the first promise, and a protected calendar block is kept instead of adding more.

The local model is a scripted Strands `Model` so the demo can run without Bedrock credits. It still emits real tool-use events and the Agent executes the tools. Swap `ONECUT_MODEL=bedrock` when AWS credits land.

Synthetic fixtures only. No live user history.
