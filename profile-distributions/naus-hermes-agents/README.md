# Naus/NOUS Hermes Agent Profile Fleet

This is the sanitized public profile distribution for Eric DGX's Naus/NOUS Hermes Agent fleet, migrated from the previous OpenClaw runtime.

The bundle includes 17 Hermes profiles, their persona/tool sidecar files, and profile-specific custom skills. It deliberately excludes private memory and runtime state: `LETTA_MEMORY.md`, SQLite databases, auth files, sessions, logs, caches, backups, webhook URLs, and Discord tokens are not part of this distribution.

Legacy names such as `openclaw_*`, `openclaw_full`, and `~/.openclaw` may still appear where they are runtime compatibility identifiers. The active identity is Naus/NOUS Hermes Agent.

## Profiles

`alfred`, `ares`, `athena`, `chimera`, `gungnir`, `hephaestus`, `hermes-trader`, `iris`, `kairos`, `mnemosyne`, `nemesis`, `pheme`, `prometheus`, `talos`, `themis`, `tyche`, `zhuge_liang`

## Install

From the root of this repository:

```bash
python3 profile-distributions/naus-hermes-agents/validate.py
python3 profile-distributions/naus-hermes-agents/install.py --target ~/.hermes/profiles
```

To preserve an existing local `config.yaml`, omit `--force-config` as shown above. The installer overlays profile files and skills, but does not remove or overwrite memories, sessions, state databases, auth files, or logs.

## Hermes Desktop

If Hermes Desktop should connect to these profiles through an SSH alias named `dgx`:

```bash
python3 profile-distributions/naus-hermes-agents/connect_hermes_desktop.py --ssh-alias dgx
```

If the app cannot resolve the alias, pass `--host`, `--user`, and `--port`.

## Discord Bridge

The Discord operator bridge should dispatch profile chat through the current Hermes Gateway OpenAI-compatible route:

```text
POST /v1/chat/completions
model: <profile-name>
Authorization: Bearer <local Hermes gateway key>
```

The old `/api/sessions/<agent>-main/chat` route is not used by this distribution.
