# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `8917-write` v0.1: public long-form writing skill in Ye Chengfeng's voice — dual topic gating (HKR + asset criterion), built-in evidence chain (citation blocks + source-verification SOP), four article archetypes, title candidates, and a four-layer self-review with evidence check first (adapted from khazix-writer + original methodology)
- `8917-wenzhen` v2.2: two-tier adversarial retrospective (five-question wrap-up / commander's ten questions with tenth-man dissent, premortem, and falsifiability checks); v2.2 wires up `.8917/` workspace persistence and makes the execution-debt ledger location portable (global ledger when configured, workspace-local `.8917/execution-debt.md` otherwise)
- `8917-skills`: bilingual changelog support via `CHANGELOG_CN.md`

### Changed
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
