> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

<!-- MARK:HERMES-LETTA-SIDECAR-V1-20260507 -->
<!-- Sourced from Letta agent agent-29e8e405-79a1-4033-a383-ab26db85637a on 20260511T194819Z -->

# LETTA-CANONICAL TOOL SURFACE

Total tools attached on Letta server: **13**

These execute on the Letta server when this agent is invoked via
`delegate_to_letta(target_agent=...)` or `POST /v1/chat/completions` with `model: <agent>`.

## Tool inventory

- **`conversation_search`** — Search prior conversation history using hybrid search (text + semantic similarity).  Examples:         # Search all messages         conversation_search(query="project updates")          # Search only assistant messages         conversat...
- **`cross_asset_regime_classifier`** — 6-label cross-asset regime classifier (RISK_ON/RISK_OFF/NEUTRAL/CRYPTO_DECOUPLED/DXY_STRENGTH/BOND_STRESS).
- **`cryptosage_market_data`** — HTTP bridge to CryptoSage Firebase Cloud Functions (live market data / sentiment / news / predictions).
- **`equity_news_scanner`** — Google News RSS scanner for tickers + macro + crypto topics.
- **`equity_pulse_scanner`** — CryptoSage Firebase proxy + Alpaca + FMP 24/7 equity snapshot.
- **`fear_greed_shift_detector`** — Alternative.me Fear & Greed delta detector with severity escalation.
- **`memory_insert`** — The memory_insert command allows you to insert text at a specific location in a memory block.  Examples:         # Update a block containing information about the user (append to the end of the block)         memory_insert(label="custome...
- **`memory_replace`** — The memory_replace command allows you to replace a specific string in a memory block with a new string. This is used for making precise edits.  Do NOT attempt to replace long strings, e.g. do not attempt to replace the entire contents of...
- **`multi_factor_scorer`** — 7-algorithm weighted scoring with optional llm_adjustment blend (BUY/SELL/HOLD +/-0.08).
- **`news_velocity_scanner`** — CryptoPanic breaking-news keyword velocity scanner (2x spike detection).
- **`read_hive`** — Read a value from the organism's tier-2.5 key-value Hive Mind. If called without key, returns a structured listing of available hive keys so the caller can retry.
- **`social_sentiment_scrape`** — Fetch live social-sentiment chatter (Stocktwits + Reddit WSB/CryptoCurrency) via Crawl4AI MCP. Replaces dead Nitter/X-API path.
- **`x_tweet_reader`** — X API v2 OAuth 1.0a tweet-by-ID reader (graceful credentials_missing).
