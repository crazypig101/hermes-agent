> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

<!-- MARK:HERMES-LETTA-SIDECAR-V1-20260507 -->
<!-- Sourced from Letta agent agent-7df878f4-5499-4c6b-b4c9-9c32be9df48b on 20260511T194819Z -->

# LETTA-CANONICAL TOOL SURFACE

Total tools attached on Letta server: **12**

These execute on the Letta server when this agent is invoked via
`delegate_to_letta(target_agent=...)` or `POST /v1/chat/completions` with `model: <agent>`.

## Tool inventory

- **`cryptosage_market_data`** — HTTP bridge to CryptoSage Firebase Cloud Functions (live market data / sentiment / news / predictions).
- **`get_crypto_price`** — Return the current USD price for a cryptocurrency.
- **`get_equity_price`** — Return the current USD price for an equity or ETF via Yahoo Finance.
- **`get_fear_and_greed`** — Return the current Crypto Fear & Greed Index.
- **`get_macro_snapshot`** — Return the current macro snapshot including core indicators and ecosystem VIX state.
- **`get_market_snapshot`** — Return the broad S&P 500 market snapshot.
- **`get_sector_constituents`** — Return the checked-in constituent list for a supported sector ETF.
- **`get_technical_indicators`** — Return RSI, VWAP, MACD, Bollinger Bands, and ATR for a ticker symbol.
- **`get_vix_value`** — Return real-time VIX value with regime classification via Yahoo Finance.
- **`rank_sector_momentum`** — Rank a sector's constituents by 15 minute momentum and return the top three targets.
- **`read_hive`** — Read a value from the organism's tier-2.5 key-value Hive Mind. If called without key, returns a structured listing of available hive keys so the caller can retry.
- **`write_hive`** — Write a value to the organism's tier-2.5 key-value Hive Mind. If called without key/value, returns available keys and an example call so the caller can retry.
