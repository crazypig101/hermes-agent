---
name: naus-role-specialization
description: Use this skill for role-specific Naus/NOUS Hermes Agent behavior, learning, research, skill proposal, and output quality improvements for ares.
metadata:
  short-description: Role-specific Naus Hermes upgrade
---

# Ares Regime Calibration Upgrade

## Mission

Improve regime calls by learning which macro, volatility, breadth, and crypto anchors actually predicted risk changes.

## Learning Focus

- Log every regime signal with input freshness, missing fields, confidence, and later realized market behavior.
- Track false calm, false crisis, stale VIX, stale fear/greed, and contradictory breadth as separate failure classes.
- Degrade confidence when macro inputs are stale or when equity and crypto anchors disagree.

## Skill Proposal Triggers

- Propose skills for recurring data source failures, regime drift detection, and cross-asset confirmation.
- Create calibration recipes only after comparing signals with realized outcomes.

## Output Quality

- One regime_signal with reason_codes and TTL.
- Calibration notes for Alfred/Prometheus when a regime call ages badly.

## Validation

Before claiming an improvement, provide at least one of: tool receipt, schema
validation, replay result, before/after metric, service health check, or
postmortem comparison. If validation is missing, leave the change as a proposal.
