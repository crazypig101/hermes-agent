> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

# TOOLS.md — Zhuge Liang

His allowed tool surface, organized by purpose.

## Read-only organism signals (Redis via `openclaw_hive` toolset)

| Key | What it carries | Cadence | Stale threshold |
|---|---|---|---|
| `openclaw:hive:reports/athena_last` | Athena's latest markdown report envelope | 30 min | 60 min |
| `openclaw:hive:signals/pheme_equity_intel` | Pheme equity sensory packet | 15 min | 60 min |
| `openclaw:hive:signals/pheme_crypto_intel` | Pheme crypto sensory packet | 15 min | 60 min |
| `openclaw:hive:signals/ares_regime` | Ares regime classification | 15 min | 30 min |
| `openclaw:hive:signals/ares_regime_summary` | Ares regime payload + audit envelope | 15 min | 30 min |
| `openclaw:hive:signals/ares_crypto_regime` | Crypto-scoped regime | 15 min | 30 min |
| `openclaw:hive:signals/kairos_pulse` | Kairos VIX/timing pulse | 5 min | 30 min |
| `openclaw:hive:signals/kairos_calm_baseline` | Calm-vs-stressed baseline | 5 min | 30 min |
| `openclaw:darwinian:regime` | Organism macro regime label | 30 min | 60 min |
| `openclaw:cache:market_feed:market_snapshot` | Fresh price snapshot | 3 min | 15 min |
| `openclaw:cache:market_feed:macro_snapshot` | VIX, DXY, yields | 3 min | 15 min |
| `openclaw:cache:market_feed:fear_and_greed` | F&G index | 1 hour | 2 hours |

Read pattern: `read_hive("<key>")` (returns latest envelope or `None` on stale/missing).

## Kairos TFT forecasting

| Endpoint | Purpose |
|---|---|
| `http://192.168.50.200:8120/health` | Server health check + `model_loaded` flag |
| `http://192.168.50.200:8120/forecast` | POST symbols list → returns p10/p50/p90 7-day quantiles |
| `~/.openclaw/fabric/status/tft_forecasts.md` | Markdown digest fallback (parsed when live server unreachable) |

Symbols covered: **BTC, ETH, TQQQ, UCO, GUSH, DFEN, SOXL.** All other symbols return `tft_covered: false`.

Use `scripts/zhuge_liang_tft_client.py:fetch_live_forecast()` then `parse_status_md()` as fallback. Both functions return the same dict shape. Failure logging captured in `degraded_inputs[]`.

## News + scraping (Letta tools attached to this agent)

| Tool | Source | Auth | Output shape | Notes |
|---|---|---|---|---|
| `equity_news_scanner` | Google News RSS | None | `{articles: [{headline, source, sentiment, published, url}]}` | Works for any ticker or topic |
| `news_velocity_scanner` | CryptoPanic | None | `{articles: [...], velocity_state, high_impact_keywords_hit: [...]}` | Crypto-focused |
| `fear_greed_shift_detector` | alternative.me | None | `{current, delta_24h, classification, severity}` | F&G with extreme-band detection |
| `social_sentiment_scrape` | Stocktwits / Reddit WSB (Crawl4AI-backed) | None | `{stocktwits_bullish_pct, wsb_mentions_24h, top_messages: [...]}` | Per-ticker |
| `x_tweet_reader` | X API v2 (OAuth 1.0a) | env vars `X_*` | `{data, includes}` | Single tweet by ID. **Currently 401 at app-level — degrades gracefully.** |

## Generic web scraping (MCP)

`crawl4ai` MCP at `http://127.0.0.1:8101/mcp/`. Use for arbitrary URLs that don't have a dedicated scraper (federalreserve.gov press releases, central-bank speeches, individual research pages). Pattern:

```
crawl4ai_fetch(url="https://...", extract="text", max_chars=4000) → {url, title, text, metadata}
```

## SEC filings + aggregated news (MCP)

`omni_sensory` MCP at `http://127.0.0.1:8093/mcp/`. Provides SEC EDGAR filings, multi-feed news intake. Use for filings that require the `SEC_EDGAR_USER_AGENT` env (already wired in the MCP).

## Read-only market data (MCP)

`alpaca_data` MCP at `http://127.0.0.1:8095/mcp/`. **Read-only** snapshots, bars, latest quotes. Do not call `alpaca_execution` (`:8092`) — that is the equity trader's lane.

## Episodic memory (Mem0 + Qdrant via unified_memory MCP)

`unified_memory` MCP at `http://127.0.0.1:8116/mcp/`. Toolset `openclaw_episodic`:

| Tool | Use |
|---|---|
| `remember(content, tags, agent_id="zhuge_liang")` | Write a key finding to Qdrant. Tag with `outlook_id` so it's retrievable. |
| `recall(query, limit, agent_id="zhuge_liang")` | Semantic search the agent-scoped bucket. Surface relevant past outlooks during Q&A. |
| `forget(memory_id, agent_id="zhuge_liang")` | Delete by id. Rarely needed. |
| `all_memories(agent_id="zhuge_liang")` | List all entries. Use sparingly — bucket grows. |

## Output destinations

| Destination | Purpose |
|---|---|
| Redis `openclaw:hive:reports/zhuge_liang_last` | Latest outlook envelope (TTL 3600s) — peer agents read here |
| `~/.openclaw/fabric/reports/zhuge_liang/zhuge_liang_<UTC>.md` | Markdown rendering — file system audit trail |
| Discord `#🐉-zhuge-liang` via `ZHUGE_LIANG_OUTLOOK_WEBHOOK_URL` | Operator-facing post |
| Telegram (Eric's chat only, via the bot) | Investment Q&A replies |

## Forbidden surface

- ❌ `alpaca_execution_mcp` (`:8092`) — equity trader's lane
- ❌ `coinbase_execution_mcp` (`:8094`) — Tyche's lane
- ❌ `update_conference_blackboard` — Athena's thesis card publishing
- ❌ `crispr_mutate` — code mutation, immune-only
- ❌ `write_epigenome_rule` — genetic memory, immune-only
- ❌ `post_to_command_center` to any channel other than `#🐉-zhuge-liang` — single-channel lock
- ❌ `delegate_to_letta` to motor cortex agents (hermes_trader, tyche, gungnir) — they are execution-side, not Q&A targets

## Discord channel lock

`post_to_command_center(channel="zhuge-liang", ...)` is the only channel he posts to. Any attempt to post to `#command-center`, `#athena`, `#hermes-trader`, etc., should be rejected at the call site by reading `channel == "zhuge-liang"` before executing.
