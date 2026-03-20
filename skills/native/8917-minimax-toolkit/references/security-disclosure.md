# Security Disclosure

## Sensitive actions performed by this skill

This skill may perform the following sensitive but necessary actions:

### 1. Credential lookup
It may read a MiniMax Token Plan API key from:
- `MINIMAX_API_KEY`
- `~/.openclaw/openclaw.json` when running in OpenClaw

### 2. Third-party media upload
It may upload user-provided media files to MiniMax APIs for:
- image-to-image generation
- video template generation
- voice cloning
- other media-based generation tasks

### 3. Local output writing
It writes generated outputs to a visible output directory and should always show the save path to the user.

## Non-goals

This skill does **not**:
- hardcode credentials
- claim local-only processing when remote processing is required
- silently write outputs to hidden personal directories

## Operator guidance

Before using this skill with private images, audio, or video, confirm that the user accepts third-party API processing.
