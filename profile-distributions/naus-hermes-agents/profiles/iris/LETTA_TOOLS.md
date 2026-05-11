> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

<!-- MARK:HERMES-LETTA-SIDECAR-V1-20260507 -->
<!-- Sourced from Letta agent agent-9733a412-7aa4-4810-85c1-0be59426edd3 on 20260511T194819Z -->

# LETTA-CANONICAL TOOL SURFACE

Total tools attached on Letta server: **1**

These execute on the Letta server when this agent is invoked via
`delegate_to_letta(target_agent=...)` or `POST /v1/chat/completions` with `model: <agent>`.

## Tool inventory

- **`post_to_command_center`** — Post structured status messages to a Discord webhook endpoint with channel-aware routing.
