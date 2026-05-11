> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

<!-- MARK:HERMES-LETTA-SIDECAR-V1-20260507 -->
<!-- Sourced from Letta agent agent-1d616e0f-9ea0-4e45-a188-a5244bb3b51b on 20260511T194819Z -->

# LETTA-CANONICAL TOOL SURFACE

Total tools attached on Letta server: **19**

These execute on the Letta server when this agent is invoked via
`delegate_to_letta(target_agent=...)` or `POST /v1/chat/completions` with `model: <agent>`.

## Tool inventory

- **`cancel_order`** — Cancel an open Coinbase order by order ID.      Not supported in paper mode (paper trades fill instantly).     Tagged for lobe: hermes_trader.
- **`check_bracket_exits`** — Check if any paper bracket exits (TP/SL) have triggered. MUST be called every heartbeat.
- **`cryptosage_market_data`** — HTTP bridge to CryptoSage Firebase Cloud Functions (live market data / sentiment / news / predictions).
- **`get_coinbase_balance`** — Return Coinbase portfolio balance, positions, and PnL.      In paper mode returns the simulated portfolio.     In live mode returns real account balances from Coinbase Advanced Trade.     Tagged for lobe: hermes_trader.
- **`get_crypto_price`** — Return the current USD price for a cryptocurrency.
- **`get_equity_price`** — Return the current USD price for an equity or ETF via Yahoo Finance.
- **`get_fear_and_greed`** — Return the current Crypto Fear & Greed Index.
- **`get_fills`** — Get recent trade fills / history.      Args:         symbol: Optional filter by asset (e.g. 'BTC'). Empty = all.         limit: Max fills to return (default 20).      Tagged for lobe: hermes_trader.
- **`get_macro_snapshot`** — Return the current macro snapshot including core indicators and ecosystem VIX state.
- **`get_market_snapshot`** — Return the broad S&P 500 market snapshot.
- **`get_open_orders`** — List open / pending Coinbase orders.      Args:         symbol: Optional filter by asset. Empty = all.      Paper mode always returns an empty list (paper trades fill instantly).     Tagged for lobe: hermes_trader.
- **`get_sector_constituents`** — Return the checked-in constituent list for a supported sector ETF.
- **`get_technical_indicators`** — Return RSI, VWAP, MACD, Bollinger Bands, and ATR for a ticker symbol.
- **`get_vix_value`** — Return real-time VIX value with regime classification via Yahoo Finance.
- **`market_pulse_scanner`** — CryptoSage proxy + CoinGecko + F&G snapshot with pump/dump alerts.
- **`place_limit_order`** — Place a limit buy or sell on Coinbase at a specific price.      Args:         symbol: Crypto asset (BTC, ETH, SOL, etc.)         side: 'buy' or 'sell'         base_size: Amount of asset to trade         limit_price: Price per unit in USD...
- **`place_market_order`** — Place a market buy or sell on Coinbase.      Args:         symbol: Crypto asset (BTC, ETH, SOL, etc.)         side: 'buy' or 'sell'         quote_usd: USD amount to spend (buy) or USD worth to sell         take_profit_pct: Optional expec...
- **`rank_sector_momentum`** — Rank a sector's constituents by 15 minute momentum and return the top three targets.
- **`run_exit_scan`** — Run the multi-layer exit scan on all open positions. Checks technicals     (RSI, MACD, Bollinger, VWAP) for each position and applies the exit matrix.     Automatically executes sells when triggered. Call every heartbeat AFTER     check_...
