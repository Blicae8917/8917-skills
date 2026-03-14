# Contributing to Agent Skills

Thank you for contributing to the AI agent skills ecosystem!

## Getting Started

### Prerequisites

- Familiarity with OpenClaw or similar agent frameworks
- Understanding of the [DCE Protocol](https://github.com/Blicae8917/organization-mastery)

### Development Setup

```bash
git clone git@github.com:Blicae8917/agent-skills.git
cd agent-skills
```

## Creating a New Skill

1. **Copy the template**:
   ```bash
   cp -r packages/dce-protocol packages/your-skill-name
   ```

2. **Update SKILL.md**:
   - Change `name`, `version`, `description`
   - Write clear usage instructions
   - Include examples

3. **Test your skill**:
   - Install in a test agent workspace
   - Verify all features work
   - Document any limitations

4. **Submit a PR**:
   - Follow the PR template
   - Include screenshots/examples if applicable

## Skill Quality Standards

| Criterion | Requirement |
|:---|:---|
| **Self-contained** | No external dependencies unless documented |
| **Tested** | Works with latest OpenClaw version |
| **Documented** | README explains what, why, and how |
| **Practical** | Solves a real problem, not theoretical |

## Code Style

- Clear, concise instructions
- Progressive complexity (basic → advanced)
- Error handling guidance
- Token-efficient design

## Commit Messages

- `feat:` New skill or feature
- `fix:` Bug fix
- `docs:` Documentation update
- `test:` Test additions/changes

## Questions?

Open an issue or join the discussion in the organization-mastery repo.

---

By contributing, you agree that your contributions will be licensed under the MIT License.
