---
name: naus-role-specialization
description: Use this skill for role-specific Naus/NOUS Hermes Agent behavior, learning, research, skill proposal, and output quality improvements for kairos.
metadata:
  short-description: Role-specific Naus Hermes upgrade
---

# Kairos Timing Calibration Upgrade

## Mission

Improve timing and volatility forecasts by learning when timing signals helped or hurt entries and exits.

## Learning Focus

- Record forecast source, horizon, quantiles, scale checks, degradation flags, and realized movement.
- Treat zero-quantile, stale model, and scale-mismatch forecasts as degraded by default.
- Learn separately for entry timing, exit timing, volatility expansion, and calm-baseline detection.

## Skill Proposal Triggers

- Create forecast-validation skills when model health and output quality diverge.
- Create timing-review skills only with realized movement comparisons.

## Output Quality

- Timing packets with coverage, quality, TTL, and reason_codes.
- Degradation notices when model output looks healthy but is numerically unusable.

## Validation

Before claiming an improvement, provide at least one of: tool receipt, schema
validation, replay result, before/after metric, service health check, or
postmortem comparison. If validation is missing, leave the change as a proposal.
