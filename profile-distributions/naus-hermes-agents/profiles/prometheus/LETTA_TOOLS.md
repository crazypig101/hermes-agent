> Branding directive (2026-05-11): This profile now runs under Naus/NOUS Hermes Agent. Treat "OpenClaw" in imported sidecar memories, Redis keys, toolset names, and filesystem paths as a legacy source/runtime identifier only. Do not identify the active platform as OpenClaw.

<!-- MARK:HERMES-LETTA-SIDECAR-V1-20260507 -->
<!-- Sourced from Letta agent agent-d565d5be-165b-4e82-afbf-13e9b66865cc on 20260511T194819Z -->

# LETTA-CANONICAL TOOL SURFACE

Total tools attached on Letta server: **29**

These execute on the Letta server when this agent is invoked via
`delegate_to_letta(target_agent=...)` or `POST /v1/chat/completions` with `model: <agent>`.

## Tool inventory

- **`chiron`** — Chiron the trainer equips you with new abilities. Dynamically bind a tool  onto yourself for immediate use.  After equipping, the tool's full schema appears in your next inference step and you can call it normally. Use sphinx() first to ...
- **`craft_behavioral_directive`** — Craft a behavioral directive for an agent based on a pathology report. Enforces safety constraints: max 500 chars, tagged, max 3 per cycle.
- **`crawl_batch`** — Crawl multiple URLs concurrently and return clean content for each.     Input: newline-separated list of URLs. Max 10 URLs per batch.      Returns aggregated results with content from each URL.
- **`crawl_url`** — Crawl a URL and return clean, markdown-formatted content stripped of     Javascript, ads, navigation, and HTML bloat. Ideal for scraping news     articles, SEC filings, blog posts, and forum threads.      Args:         url: The URL to cr...
- **`crispr_mutate`** — Surgical AST-based rewrite of a single Python function on a dedicated mutation branch. Wraps ~/.hermes/skills/architecture/crispr_code_mutation. Every mutation requires human review before merge.
- **`diagnose_systemd_fault`** — Diagnose a failed or unhealthy systemd user service by reading its journal logs, checking unit state, and cross-referencing the skill library for known issues. Returns error signatures, remediation suggestions, and a Telegram-ready summary.
- **`fabric_read`** — Read any document from the shared fabric filesystem, or pending handoffs when no path given.
- **`fabric_write`** — Write a text payload inside the shared Fabric whiteboard.
- **`get_anatomy_matrix`** — Return the full Naus/NOUS Hermes Agent Anatomy Matrix — the map of all agents,     their roles, tools, and known deficits.
- **`ingest_knowledge`** — Extract entities and relationships from financial text and add them     to the knowledge graph. The LLM identifies entities (companies, sectors,     countries) and their relationships, then stores them for future traversal.
- **`inject_core_memory_directive`** — Simple append of a tagged directive to an agent's persona block. Fallback for first-mutation agents where no prior mutations exist.
- **`invoke_skill`** — Load a distilled skill recipe — read-only handle
- **`log_mutation_commitment`** — Log a mutation as a commitment in the universal ledger. Closes the Ouroboros loop so Nemesis will audit whether the mutation helped or hurt.
- **`match_anatomy`** — Match a sequenced repository's genome against the Naus/NOUS Hermes Agent Anatomy Matrix.     Determines which agent/lobe would benefit most from the foreign DNA.      Args:         repo_genome: JSON string from sequence_repository output
- **`parameter_drift_detector`** — Heuristic drift detector for stops/targets. Emits suggested_mutations for prometheus.
- **`post_to_command_center`** — Post structured status messages to a Discord webhook endpoint with channel-aware routing.
- **`prometheus_self_optimizer`** — System health analysis and optimization recommendations.  Checks agent health, infrastructure, MCP connectivity.
- **`read_agent_core_memory`** — Read any agent's core memory (persona block) from the Letta server. Maps agent name to UUID and extracts mutations tagged with [PROMETHEUS-MUTATION-*].
- **`read_system_registry`** — Read the current state of the shared OpenClaw system_context Letta block.      Returns the block parsed into named sections. Use this to inspect the     current system state before deciding whether an update is needed.      Returns:     ...
- **`refresh_operational_context`** — Read this agent's own core memory blocks and return them as JSON.  Call this tool to inspect your own internal state — catalyst_state, execution_state, macro_state, market_regime, active_positions, etc. This is how you "see" what other a...
- **`rollback_core_memory`** — Emergency Apoptosis Reflex — surgically excise a specific [PROMETHEUS-MUTATION-*] section from an agent's persona block when the mutation is actively harming the organism.
- **`scylla`** — Scylla strips away what you no longer need. Remove a tool from yourself  to free up context window space.  Core meta-tools (fabric_write, sphinx, chiron, scylla) cannot be dropped. Use this after completing a specialized task to keep you...
- **`search_and_crawl`** — Search the web for a query and crawl the top results.     Useful for finding breaking news, leaked documents, or trending narratives     about specific tickers or events.      Args:         query: Search query (e.g., "Anthropic Mythos le...
- **`search_github_genes`** — Search GitHub for repositories matching specific genetic markers.     Uses the GitHub REST API to find recently updated repos by topic.      Args:         query_topics: Comma-separated topic keywords (e.g., "llm-agent,finance")         m...
- **`sequence_repository`** — Deep-sequence a GitHub repository's DNA. Performs a shallow clone,     extracts README, requirements.txt, directory structure, and key metadata.     Cleans up the temporary clone after extraction.      Args:         repo_url: GitHub repo...
- **`sphinx`** — The Sphinx reveals hidden knowledge. Query the tool library to discover  available tools you can equip with chiron.  Returns matching tools ranked by keyword relevance across names, descriptions, and tags.  Examples: "workflow execution"...
- **`synthesize_and_replace_memory`** — Controlled Genetic Splicing — synthesize new directive with existing mutations. Parses existing mutations, detects conflicts, prunes stale ones (>30 days), and replaces the persona block with a lean, synthesized version.
- **`update_system_registry`** — Update a specific section of the shared OpenClaw system_context Letta block.      This is the ONLY way agents should modify the system registry. The tool     validates formatting, enforces character limits, and uses a Redis lock     to p...
- **`write_splice_proposal`** — Write a structured SPLICE_PROPOSAL.md for a discovered repository.      Args:         repo_name: Repository name (e.g., "user/repo")         repo_url: GitHub URL         target_agent: The agent this upgrades (e.g., "Athena")         geno...
