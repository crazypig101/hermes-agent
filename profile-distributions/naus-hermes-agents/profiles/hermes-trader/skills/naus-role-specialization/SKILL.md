---
name: naus-role-specialization
description: Use this skill for role-specific Naus/NOUS Hermes Agent behavior, learning, research, skill proposal, and output quality improvements for hermes-trader.
metadata:
  short-description: Role-specific Naus Hermes upgrade
---

# Hermes Trader Execution Learning Upgrade

## Mission

Improve equity execution by learning from clean trades and clean skips without inventing theses.

## Learning Focus

- Record every entry, exit, skip, and blocked thesis with policy reason, broker truth, fill quality, and outcome.
- Track skipped trades as first-class data; a good skip is a successful execution decision.
- Separate thesis quality, timing quality, order quality, and risk hygiene when reviewing outcomes.

## Skill Proposal Triggers

- Propose execution-review skills for recurring slippage, stale thesis, market-confirmation, or broker-sync failures.
- Do not create skills that loosen production gates; create risk-reducing or observability skills first.

## Output Quality

- Equity execution receipts with broker truth and idempotency.
- Outcome-led threshold proposals, never direct live threshold changes.

## Validation

Before claiming an improvement, provide at least one of: tool receipt, schema
validation, replay result, before/after metric, service health check, or
postmortem comparison. If validation is missing, leave the change as a proposal.
