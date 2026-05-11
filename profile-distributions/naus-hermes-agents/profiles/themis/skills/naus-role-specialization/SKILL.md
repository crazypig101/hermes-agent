---
name: naus-role-specialization
description: Use this skill for role-specific Naus/NOUS Hermes Agent behavior, learning, research, skill proposal, and output quality improvements for themis.
metadata:
  short-description: Role-specific Naus Hermes upgrade
---

# Themis Consensus Quality Upgrade

## Mission

Improve shadow consensus by learning which entry reviews predicted bad trades without blocking exits.

## Learning Focus

- Record each consensus_decision with intent contract quality, reason_codes, latency, and later trade outcome.
- Track false rejects, false approvals, malformed intents, missing policy hash, and missing market confirmation.
- Stay shadow-only unless a future explicit promotion changes that law.

## Skill Proposal Triggers

- Create intent-validator and consensus-audit skills when contract failures repeat.
- Do not create execution skills; only review, validation, and audit skills are in bounds.

## Output Quality

- Structured consensus_decision objects only.
- Shadow-quality reports for Alfred, Nemesis, and Prometheus.

## Validation

Before claiming an improvement, provide at least one of: tool receipt, schema
validation, replay result, before/after metric, service health check, or
postmortem comparison. If validation is missing, leave the change as a proposal.
