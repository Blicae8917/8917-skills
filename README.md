# 8917-skills

A curated collection of reusable AI agent skills from 8917.

[中文版](README_CN.md)

---

## What is this?

`8917-skills` is the executable capability repository of the 8917 system.

It focuses on **practical, reusable, installable skills** that can make an agent immediately more capable.

If `8917-organization-mastery` explains the principles and methodology behind 8917, this repository contains the skills and wrappers that put those ideas into action.

---

## What you can do with these skills

Current skills in this repository help agents:

- write public long-form articles in a consistent authorial voice (topic gating → evidence chain → drafting → four-layer self-review)
- assemble an ad-hoc multi-perspective expert panel for roundtable discussion, adversarial review, or planning — works standalone even without a local expert library
- run adversarial retrospectives on projects and plans (lightweight five-question wrap-up / ten-question full consultation), with an execution-debt ledger loop and `.8917/` workspace persistence

---

## For Humans

If you are a human user, this repository helps you:
- discover what 8917 skills exist
- install or copy the skills you need
- understand what each skill is good at
- decide whether to use a published skill or a local repository version

If you only care about installation and usage, jump to:
- [Included skills](#included-skills)
- [Installation](#installation)
- [Quick usage examples](#quick-usage-examples)

---

## For Agents

If you are giving this repository to an agent (such as OpenClaw), the agent should:

1. Read this README first
2. Identify which skill best matches the user’s actual task
3. Prefer already-published skills when available
4. If a skill is not yet published, fall back to the repository structure under `skills/`
5. Refer to `8917-organization-mastery` when methodology or governance background is needed

### Copy-paste prompt for OpenClaw or another agent

```text
Read the 8917-skills repository README and identify which skill best fits my task.
Then guide me through installation and usage.
If the skill is already published, prefer the published installation path.
If not, use the repository structure and explain how to use it locally.
If methodology or governance background is needed, also refer to 8917-organization-mastery.
```

### Guidance rule for agents

When helping a user from this repository:
- prefer the most stable published skill first
- otherwise use the local repository path under `skills/`
- do not confuse skill assets with methodology docs from `8917-organization-mastery`

---

## Included skills

| Skill | What it does | Status |
|:---|:---|:---|
| `8917-write` | Public long-form writing in Ye Chengfeng's voice: dual topic gating (HKR + asset criterion) → evidence chain (citation blocks + source-verification SOP) → four article archetypes → title candidates → four-layer self-review with evidence check first | v0.1, in repo |
| `8917-expert-panel` | Multi-perspective expert panel: three modes (discussion / review / planning) × two execution tiers (in-conversation / Workflow engine); dual-source expert casting — uses a local expert library when present, otherwise generates personas on the fly with zero external dependencies | v2.1, in repo |
| `8917-wenzhen` | Two-tier adversarial retrospective ("wenzhen" = diagnostic inquiry): five questions (outpatient, 2-minute wrap-up) / commander's ten questions (full consultation — axis-shifting review, tenth-man dissent, premortem, stop-loss lines); execution-debt ledger loop + `.8917/` workspace persistence | v2.2, in repo |

> Earlier skills (`8917-minimax-toolkit`, `8917-docx-official`, `8917-content-ingest`, `8917-dce-protocol`) were removed in 2026-07 (unmaintained or superseded by stronger general-purpose tools). See git history; users who installed via ClawHub are unaffected. An upgraded official-document skill will return.

---

## Installation

Clone the repository and copy the skills you need into your agent's skill directory:

```bash
git clone git@github.com:Blicae8917/8917-skills.git
cp -r 8917-skills/skills/8917-write ~/.claude/skills/
cp -r 8917-skills/skills/8917-expert-panel ~/.claude/skills/
cp -r 8917-skills/skills/8917-wenzhen ~/.claude/skills/
```

Or simply hand the repository URL to your agent and let it install for you.

### Current release policy

Skills in this repository are published **one by one as they mature**.
This repository is not treated as a single bundled release unit.

---

## Quick usage examples

### `8917-write`
Tell your agent "turn this project retrospective into a public article". The skill runs: topic gating → evidence-chain sourcing → archetype-based drafting → 5-8 title candidates → four-layer self-review with a QA report.

See:

```text
skills/8917-write/
```

### `8917-expert-panel`
Tell your agent "assemble an expert panel to review this plan". The skill runs: expert-source detection (local library / generated personas) → roster confirmation → parallel anti-anchoring dispatch → synthesis of consensus and disagreements.

See:

```text
skills/8917-expert-panel/
```

### `8917-wenzhen`
Say "five questions" at wrap-up for a 2-minute retrospective, or "wenzhen" / "ten questions" at major milestones for a full adversarial consultation — it reconciles the execution-debt ledger first, then outputs blind spots, tenth-man dissent, stop-loss lines, and three immediate actions, persisted to `.8917/wenzhen/`.

See:

```text
skills/8917-wenzhen/
```

---

## Repository structure

```text
8917-skills/
├── skills/          # main home for skill assets
│   ├── 8917-write/
│   ├── 8917-expert-panel/
│   └── 8917-wenzhen/
├── protocol/        # repository-level skill spec (SKILL_SPEC_V2)
└── README / CHANGELOG / CONTRIBUTING / LICENSE
```

### Notes
- Skills live directly under `skills/`.
- The migration-era directories (`packages/`, `specs/`, `pending/`, `references/`) were cleaned up in 2026-07; see CHANGELOG.

---

## Related repository

### `8917-organization-mastery`
This is the methodology and governance repository behind the skills.

Use it when you want to understand:
- why these skills are designed this way
- the DCE protocol in its full theoretical form
- the organizational principles behind 8917

In short:
- `8917-skills` = executable capability assets
- `8917-organization-mastery` = principles, governance, and methodology

Repository:
- https://github.com/Blicae8917/8917-organization-mastery

---

## Contributing

See:
- `CONTRIBUTING.md`
- `protocol/SKILL_SPEC_V2.md`

---

Maintained by 8917OpenClaw.
