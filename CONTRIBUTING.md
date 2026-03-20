# Contributing to 8917-skills

Thank you for contributing to the 8917 open skill arsenal.

## Getting Started

### Prerequisites

- Familiarity with OpenClaw or similar agent frameworks
- Understanding of the DCE methodology in [8917-organization-mastery](https://github.com/Blicae8917/8917-organization-mastery)

### Development Setup

```bash
git clone git@github.com:Blicae8917/8917-skills.git
cd 8917-skills
```

## Creating a New Skill

1. Decide the skill's role clearly:
   - Native skill
   - Wrapper
   - Experimental skill

2. Follow the current spec:
   - `protocol/SKILL_SPEC_V2.md`

3. Place the skill in the appropriate structure:
   - `skills/native/`
   - `skills/wrappers/` (future)
   - or `pending/` during incubation

4. Keep the skill lean:
   - Clear trigger description
   - Minimal frontmatter
   - References/scripts/assets only when needed

5. Submit a PR with:
   - What the skill solves
   - Why it belongs in this repo
   - Whether it is native / wrapper / experimental

## Skill Quality Standards

| Criterion | Requirement |
|:---|:---|
| **Clear role** | Type layer and pattern layer should be clear |
| **Reusable** | Skill solves a repeatable problem |
| **Clean structure** | Follows `SKILL_SPEC_V2.md` |
| **Practical** | Real capability, not theoretical filler |

## Commit Messages

- `feat:` New skill or repo-level capability
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Structural cleanup or reorganization

## Questions?

For skill assets and repository structure, open an issue here.
For theory, governance, and methodology, use `8917-organization-mastery`.

---

By contributing, you agree that your contributions will be licensed under the MIT License.
