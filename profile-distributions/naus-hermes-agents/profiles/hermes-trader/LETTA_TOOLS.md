> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

<!-- MARK:HERMES-LETTA-SIDECAR-V1-20260507 -->
<!-- Sourced from Letta agent agent-0fc15ea3-3917-4aa3-b7df-564ea195a038 on 20260511T194819Z -->

# LETTA-CANONICAL TOOL SURFACE

Total tools attached on Letta server: **20**

These execute on the Letta server when this agent is invoked via
`delegate_to_letta(target_agent=...)` or `POST /v1/chat/completions` with `model: <agent>`.

## Tool inventory

- **`cryptosage_market_data`** — HTTP bridge to CryptoSage Firebase Cloud Functions (live market data / sentiment / news / predictions).
- **`equity_pulse_scanner`** — CryptoSage Firebase proxy + Alpaca + FMP 24/7 equity snapshot.
- **`evaluate_historical_loss_rate`** — Deterministically inspect Hermes archival trade memory for a ticker and decide whether high-VIX historical losses require an experiential veto.
- **`execute_equity_sells`** — Execute market sell orders for held positions. Each order needs ticker and qty (positive number of shares to sell).
- **`execute_target_rotation`** — Execute exact market buy orders after a hard buying-power notional safety check.
- **`get_account_state`** — Return available buying power, cash, equity, broker status, market status, and open positions.
- **`get_crypto_price`** — Return the current USD price for a cryptocurrency.
- **`get_equity_price`** — Return the current USD price for an equity or ETF via Yahoo Finance.
- **`get_fear_and_greed`** — Return the current Crypto Fear & Greed Index.
- **`get_macro_snapshot`** — Return the current macro snapshot including core indicators and ecosystem VIX state.
- **`get_market_snapshot`** — Return the broad S&P 500 market snapshot.
- **`get_protective_orders`** — Return open protective orders (trailing_stop, stop, stop_limit) for a symbol.      Sensory graft for the FSM HARD_STOP guard: lets the execution FSM detect     broker-side protection already in place before issuing redundant market     s...
- **`get_sector_constituents`** — Return the checked-in constituent list for a supported sector ETF.
- **`get_technical_indicators`** — Return RSI, VWAP, MACD, Bollinger Bands, and ATR for a ticker symbol.
- **`get_vix_value`** — Return real-time VIX value with regime classification via Yahoo Finance.
- **`liquidate_positions`** — Close the provided tickers using Alpaca close-position actions.
- **`rank_sector_momentum`** — Rank a sector's constituents by 15 minute momentum and return the top three targets.
- **`sell_position_fraction`** — Sell a broker-validated fraction of a live long equity position.
- **`sync_trailing_stops`** — Ensure broker-safe 5% trailing stops exist for current long positions.
- **`validate_target_basket`** — Validate that each target ticker is active, tradable, fractionable, and marginable on Alpaca.
