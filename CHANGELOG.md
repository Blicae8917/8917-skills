# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `8917-skills`: one-shot installers `scripts/install.ps1` / `scripts/install.sh` — enumerate `skills/` and link every skill into each host present on the machine (auto-detects `~/.claude` and `~/.codex`); idempotent (installed links skipped, occupied non-repo paths warned and never overwritten); Git Bash environments are redirected to the ps1 (MSYS `ln -s` copies instead of linking)
- `8917-skills`: skill roster consistency test `tests/test_skill_roster.py` — keeps the `skills/` directory, both README rosters, and each SKILL.md `name` field aligned, preventing unregistered skills (retrospective from `8917-session-restore` v1.0 shipping without CHANGELOG/README entries)
- `8917-session-restore` v1.0: restores the Claude Code Desktop session list after switching accounts — auto-detects the current account partition and migrates old-partition records deduplicated by cliSessionId (dry-run / automatic backup / rollback), with a full account-switch impact checklist (macOS)
- `8917-write` v0.1: public long-form writing skill in Ye Chengfeng's voice — dual topic gating (HKR + asset criterion), built-in evidence chain (citation blocks + source-verification SOP), four article archetypes, title candidates, and a four-layer self-review with evidence check first (adapted from khazix-writer + original methodology)
- `8917-wenzhen` v2.2: two-tier adversarial retrospective (five-question wrap-up / commander's ten questions with tenth-man dissent, premortem, and falsifiability checks); v2.2 wires up `.8917/` workspace persistence and makes the execution-debt ledger location portable (global ledger when configured, workspace-local `.8917/execution-debt.md` otherwise)
- `8917-skills`: bilingual changelog support via `CHANGELOG_CN.md`

### Changed
- `8917-session-restore` v1.2: migration filters — `--from` (restrict source partitions by UUID prefix for multi-account setups) and `--cwd` (restrict by project path substring); migration preview flags same-title sessions as "likely fork" (dedup remains by cliSessionId; duplicate same-title entries are harmless)
- `8917-session-restore` v1.1: cross-platform — auto-detects the storage root on macOS / Windows (Windows: `%APPDATA%\Claude\claude-code-sessions`); backup switched from the external `tar` command to Python's built-in tarfile; migrated records now clear the account-bound fields `bridgeSessionIds` / `remoteMcpServersConfig` (restored entries are local-only; mechanism field-verified on Windows via an equivalent manual migration); metadata reads pinned to UTF-8 (fixes a latent Windows locale-encoding failure on Chinese titles); adds unit tests for sessions_root / sanitize_meta plus a dry-run CLI behavior test
- `8917-expert-panel` v2.2: runtime-aware routing — Claude Code and Codex now use their own native expert registries; adds a canonical expert-card registry script, capability negotiation, dynamic dispatch waves, mode-specific schemas, failure ledgers, and explicit reproducibility gates; missing heavy-tier capabilities no longer silently masquerade as a successful downgrade
- `8917-expert-panel` v2.1: dual-source expert casting — prefers the local expert library (`~/.claude/agents/`, e.g. agency-agents) when installed, otherwise generates expert personas on the fly with zero external dependencies; machine-local path references removed for open-source portability
- Repository structure: skills now live directly under `skills/` (the redundant `native/` layer was removed)

### Removed
- `8917-minimax-toolkit`, `8917-docx-official`, `8917-content-ingest`, `8917-dce-protocol`: unmaintained since 2026-03 or superseded by stronger general-purpose tools; all versions remain in git history, and ClawHub-published copies are unaffected. An upgraded official-document skill is planned to return.
- Migration-era directories `packages/`, `pending/`, `specs/`, `references/`: legacy content cleaned up as planned during the original migration

### Documentation
- `protocol/SKILL_SPEC_V2.md`: retained as the current repository-level skill specification reference
- README (EN/CN) and CONTRIBUTING updated to the new structure and skill roster

## [0.1.0] - 2026-03-14

### Added
- Initial repository setup
- Early DCE protocol skill package prototype
- Early skill specification draft

[Unreleased]: https://github.com/Blicae8917/8917-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Blicae8917/8917-skills/releases/tag/v0.1.0
