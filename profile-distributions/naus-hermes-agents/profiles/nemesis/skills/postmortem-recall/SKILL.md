---
name: postmortem-recall
description: Retrieve top-K similar prior trades/lessons from the OpenClaw Qdrant + pgvector index. Use when the user asks about past trades, "have we seen this setup before?", "how did X go?", direction/symbol-specific queries.
version: 1.0.0
metadata:
  hermes:
    tags: [trading, memory, recall, openclaw]
    related_skills: []
config_vars:
  - name: OPENCLAW_LESSONS_DSN
    description: Postgres DSN for openclaw_lessons table (read from env / strike-team/.env, no literal in skill)
    default: "$OPENCLAW_LESSONS_DSN"
  - name: OPENCLAW_QDRANT_URL
    description: Qdrant URL
    default: "http://127.0.0.1:6333"
---

# Postmortem Recall

Retrieve similar prior trades / lessons / postmortems for the operator from the OpenClaw memory layer.

## When to invoke this skill

Trigger on user questions of the form:
- "how did X go?" / "show me LLY shorts" / "any earnings beat trades?"
- "have we traded this setup before?"
- direction/symbol/setup-family/regime keyword queries
- pattern questions ("am I over-trading GOOGL?")

Do NOT invoke for:
- general market commentary (no past-trade lookup needed)
- portfolio status (use `portfolio-health` instead)
- live regime questions (use `consult-alfred`)

## Steps

1. Pass the user's full question (including ticker, direction, regime keywords) to `recall.py`:

   ```bash
   /home/ericm1883/.hermes/skills/postmortem-recall/recall.py "<user's question>" -k 5
   ```

2. The script returns chat-friendly markdown — relay it directly to the user, then add ONE sentence of editorial framing if you can spot a pattern beyond what the "Pattern:" line already says.

3. If `No similar prior setups found`, say so honestly. Do NOT fabricate trades.

4. If 3+ hits share a symbol AND share an outcome (e.g. 4 GOOGL LOSERs), surface this as a flagged pattern: "Worth noting — pattern of GOOGL longs losing this month."

## Output style

- Lead with the recall results, not narration.
- One paragraph of editorial after, max.
- If user asked about a specific symbol with no hits, suggest the pgvector backend explicitly: "We have no postmortems for X yet; you can check by running `find_similar_setup.py 'X long' --backend pgvector`."

## Configuration

Reads `OPENCLAW_LESSONS_DSN` from environment, falling back to `~/workspace/strike-team/.env`.
