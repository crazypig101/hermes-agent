---
name: source_apoptosis
description: Identifies upstream data sources that consistently cause drift and severs them.
---

# source_apoptosis

## When to use
Fires every 5 min via oracle-immune.timer. Athena ingest code should consult is_apoptosed(source_id) before pulling from a feed.

## How (concrete API)

The concrete implementation lives at:
  `~/.openclaw/workspace/organism/oracle_immune.py`

Library API you can call directly from Python:
```python
from oracle_immune import is_apoptosed, source_apoptosis
if is_apoptosed(rss_feed_url):
    return  # source severed; do not ingest
report = source_apoptosis()  # see active severs
```

CLI entry point:
```
python3 ~/.openclaw/workspace/organism/oracle_immune.py apoptosis
```

## Why this matters
Some news/RSS/API sources publish stale or off-watchlist data that triggers oracle drift events repeatedly. Apoptosis stops the bleeding at the source instead of perpetually cleaning up after it.

## Self-evolution hook
v1 maps cmdline → source (script identity = source identity). Future hook: ingest will tag :_source on every cache write so we can apoptose at the per-feed level instead of per-script.

## Wiring status
Live; severs published at openclaw:immune:apoptosis:<basename>. Ingest code should consult before fetching.
