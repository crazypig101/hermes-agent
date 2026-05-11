---
name: naus-role-specialization
description: Use this skill for role-specific Naus/NOUS Hermes Agent behavior, learning, research, skill proposal, and output quality improvements for gungnir.
metadata:
  short-description: Role-specific Naus Hermes upgrade
---

# Gungnir Entry Precision Upgrade

## Mission

Make entry scores learn from realized trade outcomes instead of static confluence.

## Learning Focus

- Record every GO/WAIT/ABORT score with symbol, side, inputs, regime, latency, and later outcome.
- Compare high-score losers and low-score winners to discover missing confluence factors.
- Keep score calibration separate for equities, crypto, event trades, and momentum trades.

## Skill Proposal Triggers

- Create entry-audit skills when recurring false positives share the same catalyst or technical pattern.
- Create event-intelligence skills only when they include source freshness and contradiction handling.

## Output Quality

- Entry scores with reason_codes, confidence, and explicit WAIT conditions.
- Calibration proposals for Prometheus when thresholds drift.

## Validation

Before claiming an improvement, provide at least one of: tool receipt, schema
validation, replay result, before/after metric, service health check, or
postmortem comparison. If validation is missing, leave the change as a proposal.
