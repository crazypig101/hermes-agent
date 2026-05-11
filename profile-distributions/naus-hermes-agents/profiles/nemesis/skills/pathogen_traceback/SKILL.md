---
name: pathogen_traceback
description: Traces drift events to the writer script that caused them and quarantines chronic offenders.
---

# pathogen_traceback

## When to use
When the truth-oracle reports drift on any surface. Fires automatically every 5 min via oracle-immune.timer; you may also invoke it manually after a suspected pathogen event.

## How (concrete API)

The concrete implementation lives at:
  `~/.openclaw/workspace/organism/oracle_immune.py`

Library API you can call directly from Python:
```python
from oracle_immune import pathogen_traceback, is_quarantined
result = pathogen_traceback()           # full report
if is_quarantined(__file__):            # writers self-check
    return
```

CLI entry point:
```
python3 ~/.openclaw/workspace/organism/oracle_immune.py pathogen
```

## Why this matters
Currently the truth-oracle deletes phantom keys but the writer keeps recreating them. pathogen_traceback identifies the source (via redis MONITOR + ss + /proc) and adds it to the quarantine list — preventing recurrence at the source.

## Self-evolution hook
Quarantines auto-lift after 24h of clean behavior. If the same script keeps re-quarantining, the score band escalates and prometheus drafts a structural fix proposal.

## Wiring status
Live and writing to ~/.openclaw/workspace/organism/data/oracle_immune_quarantine.json. Writers should consult is_quarantined(__file__) before any cache write.
