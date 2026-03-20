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

- generate images, video, speech, and music with MiniMax
- convert Markdown or existing content into official `.docx` documents
- extract clean text from web pages, X posts, and media links
- follow a structured DCE (Discuss → Confirm → Execute) execution protocol for high-risk tasks

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
4. If a skill is not yet published, fall back to the repository structure under `skills/native/`
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
- otherwise use the local repository path under `skills/native/`
- do not confuse skill assets with methodology docs from `8917-organization-mastery`

---

## Included skills

### First wave

| Skill | What it does | Status |
|:---|:---|:---|
| `8917-minimax-toolkit` | Multi-modal MiniMax toolkit for image, video, speech, voice, and music generation | Published on ClawHub |
| `8917-docx-official` | Converts Markdown or existing content into official-format `.docx` documents | Published on ClawHub |
| `8917-content-ingest` | Extracts readable content from URLs, web pages, X posts, and media links | In repo |

### Second wave (in progress)

| Skill | What it does | Status |
|:---|:---|:---|
| `8917-dce-protocol` | Skillized execution layer of DCE for Discuss → Confirm → Execute workflows | In progress |

---

## Installation

### Option 1: Install published skills

Currently published:

```bash
clawhub install 8917-minimax-toolkit
clawhub install 8917-docx-official
```

### Option 2: Use the repository directly

Clone the repository and reference skills from `skills/native/`:

```bash
git clone git@github.com:Blicae8917/8917-skills.git
cd 8917-skills
```

### Current release policy

Skills in this repository are published **one by one as they mature**.
This repository is not treated as a single bundled release unit.

---

## Quick usage examples

### `8917-minimax-toolkit`
Generate media with MiniMax using a unified output structure.

```bash
clawhub install 8917-minimax-toolkit
```

### `8917-docx-official`
Convert Markdown into an official-format Word document.

```bash
clawhub install 8917-docx-official
```

### `8917-content-ingest`
Use the skill to extract readable body text from links before summarizing, archiving, or analyzing.

See:

```text
skills/native/8917-content-ingest/
```

### `8917-dce-protocol`
Use DCE when a task requires discussion, explicit confirmation, and controlled execution.

See:

```text
skills/native/8917-dce-protocol/
```

---

## Repository structure

```text
8917-skills/
├── skills/
│   └── native/
├── protocol/
├── references/
├── pending/
├── packages/   # migration-era legacy content
└── specs/      # historical spec files
```

### Notes
- `skills/native/` is the main home for current skill assets.
- `packages/` and `specs/` are retained during migration and should not be treated as the long-term primary structure.

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
