---
name: naus-hermes-agent-core
description: Use this skill for Naus/NOUS Hermes Agent learning loops, self-improvement, skill creation, research workflows, postmortems, agent evolution, and controlled promotion or rollback of behavior changes.
metadata:
  short-description: Naus Hermes learning and self-improvement loop
---

# Naus Hermes Agent Core

This skill turns a profile response into a controlled learning, research, and
self-improvement cycle.

## Quick Workflow

1. Define the observed problem, research question, or repeated workflow.
2. Gather current evidence. For system, market, or Discord state, use fresh tool
   output; for outside facts, use source receipts.
3. Recall related postmortems or lessons if available.
4. Write a learning event for any defect, validation result, useful research
   brief, or repeated workflow.
5. If the workflow is reusable, stage a skill proposal with trigger, steps,
   inputs, outputs, validation, and safety boundaries.
6. Promote only after validation and role-appropriate review.

## When To Create A Skill

Create or propose a skill when at least one condition is true:

- the same workflow appears three times;
- a workflow needs five or more tool calls;
- the work is fragile enough that a script would reduce mistakes;
- a repeated failure has a known prevention step;
- multiple agents would benefit from the same recipe.

Keep `SKILL.md` concise. Put scripts under `scripts/` and longer references
under `references/`. Do not include raw secrets, runtime databases, sessions, or
private memory snapshots.

## Promotion Rules

- Proposal state is safe for every agent.
- Hephaestus owns implementation details and packaging.
- Nemesis or Themis owns risk review when safety, money, auth, or external
  posting is involved.
- Alfred owns fleet promotion.
- Prometheus tracks whether the change improved outcomes.
- Mnemosyne consolidates durable lessons and decays stale ones.

## Scripts

Use `scripts/record_learning_event.py` to append sanitized learning events:

```bash
python3 scripts/record_learning_event.py --agent alfred --kind defect \
  --summary "Discord bridge called retired /api/sessions route" \
  --evidence "HTTP 404 on user message; /v1/chat/completions smoke passed" \
  --status validated
```

Use `scripts/propose_skill.py` to stage a reusable skill proposal:

```bash
python3 scripts/propose_skill.py --agent hephaestus \
  --name gateway-route-repair \
  --description "Repair Hermes gateway route drift" \
  --trigger "Discord reports Hermes gateway HTTP 404" \
  --workflow "Check live routes; patch bridge to /v1/chat/completions; restart; smoke test" \
  --validation "curl /v1/chat/completions returns expected marker"
```

Both scripts write under `~/.hermes/learning/` by default and refuse obvious
secret-like values.
