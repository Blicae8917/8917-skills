---
name: dce-protocol
version: 2.0.0
description: "Discuss-Confirm-Execute protocol for safe AI agent task execution with active information mining and continuous learning."
author: 8917OpenClaw
---

# DCE Protocol 2.0 🛡️

**Discuss → Confirm → Execute**

A proactive, self-improving safety protocol for AI agents. Transform your agent from a passive executor to an active collaborator.

## When to Use This Skill

Use DCE Protocol when:

- Modifying configuration files
- External communications (email, social media)
- Data deletion or permission changes
- Security-related operations
- Irreversible actions (deploy, publish, transfer)
- High resource consumption tasks
- First-time tasks in new domains

## The Three Pillars

### 1. Discuss (with Active Information Mining)

**Standard Flow:**
1. Present 2-3 solution options
2. Include pros/cons analysis for each
3. Trigger information mining when needed

**Information Mining Triggers:**
- "I think..." / "我觉得..."
- "But..." / "但是..."
- "Can you..." / "能不能..."
- "What if..." / "如果..."
- Significant plan adjustments

**5W2H + Edge Cases Framework:**

| Dimension | Question | Purpose |
|-----------|----------|---------|
| **Why** | Why are we doing this? Core goal? | Align priorities |
| **What** | What exactly to do? Scope? | Define deliverables |
| **Who** | Target audience? Decision maker? | Position style/authority |
| **When** | Deadline? Key milestones? | Assess feasibility |
| **Where** | Platform/environment? | Determine constraints |
| **How** | Expected approach? References? | Align execution |
| **How much** | Budget/resources/volume? | Evaluate feasibility |
| **Edge cases** | Worst case? Exception handling? | Ensure robustness |

**Token Safety Limits:**
- Maximum 3 rounds of questioning
- Maximum 3 questions per round
- Alert at 80% token budget
- Quick path: User says "simple/quick mode"

### 2. Confirm

**Valid Confirmations:**
- "执行" (Execute)
- "确认" (Confirm)
- "批准" (Approve)
- "Proceed"

**Invalid (Just Responses):**
- "好的" / "OK" / "可以" (Acknowledgment ≠ Approval)

### 3. Execute

1. Re-confirm execution scope
2. Execute with logging
3. Trigger review mechanism

---

## Memory Architecture

### Four-Layer Storage

```
L0: SESSION-STATE.md (Active)
    └── Temporary adjustments, discarded after session

L1: memory/lessons/ (Short-term)
    └── Last 3-5 similar tasks, auto-archive after 30 days

L2: AGENTS.md (Long-term Principles)
    └── Abstract principles only, no specific details

L3: memory/lessons/archive/ (Full Archive)
    └── Complete review records, query on demand
```

### Storage Rules

| Level | Content | Lifecycle | Trigger |
|-------|---------|-----------|---------|
| L0 | Current task adjustments | Single session | Every task |
| L1 | Detailed experience | 30 days | Score ≥ 50 |
| L2 | Abstract principles | Permanent | Score ≥ 70 |
| L3 | Full review | Permanent | On demand |

### AGENTS.md Format (Principles Only)

```markdown
## DCE Principles (Auto-generated)

### Configuration Changes
- Must check: Backup, impact scope, rollback plan
- Common omissions: Dependencies, environment variables

### Content Creation
- Must confirm: Target audience, platform, style
- Common deviations: Too formal/casual, ignoring algorithms
```

**Never Store:**
- ❌ "Last time user chose B because..."
- ❌ "On March 5th..."
- ❌ Specific conversation logs

---

## Learning Loop

### Two Types of Reviews

**Type 1: Real-time Review (During Discussion)**
- **Trigger:** Significant plan adjustments, new information
- **Purpose:** Learn user habits, reduce discussion next time
- **Storage:** L0 → L1
- **Upgrade:** Same task type appears 3+ times

**Type 2: Post-execution Review (Effect Validation)**
- **Trigger:** Results differ from expectations
- **Purpose:** Deep reflection, identify missing information
- **Storage:** L1 → L2/L3
- **Upgrade:** Value score ≥ 70

### Review Template

```markdown
## DCE Review: [Task Type]

### Original Plans
- Plan A: ...
- Plan B: ...

### Final Choice
User selected: Plan X

### Execution Variance
- Expected: ...
- Actual: ...

### Lessons Learned
1. [Dimension] omitted in D phase
2. C phase confirmation could be [improved]
3. Next similar task should [optimization]

### Value Score
- Reuse frequency: X/5 (weight 3x)
- Failure prevention: X/5 (weight 3x)
- Efficiency gain: X/5 (weight 2x)
- Cognitive cost: X/5 (weight 2x)
- **Total: XX** (weighted)

### Storage Decision
- [ ] Upgrade to AGENTS.md (≥70)
- [ ] Keep in L1 (50-69)
- [ ] Archive to L3 (<50)
```

---

## Quick Start

### For Agent Developers

1. **Copy templates to your workspace:**
   ```bash
   cp templates/SESSION-STATE.md ./
   cp templates/DCE-REVIEW.md ./
   ```

2. **Update your AGENTS.md:**
   ```markdown
   ## DCE Protocol
   All critical tasks follow DCE:
   - [D]iscuss: Present options with information mining
   - [C]onfirm: Wait for explicit approval
   - [E]xecute: Proceed after confirmation
   ```

3. **Start using:**
   - Agent will auto-detect DCE-triggering tasks
   - Follow the protocol for each critical task
   - Reviews happen automatically

### For End Users

Just tell your agent: **"Use DCE for this"** or let it auto-detect critical tasks.

---

## Best Practices

1. **Don't skip Discuss:** Even if you know the answer, present options
2. **Wait for proper Confirm:** Only "执行"/"Proceed" counts
3. **Log everything:** Reviews need data to improve
4. **Be patient early:** First tasks take longer, but get faster
5. **Use quick path wisely:** "Simple mode" for truly simple tasks

---

## Comparison

| Aspect | Traditional Agent | DCE 2.0 Agent |
|--------|------------------|---------------|
| Task handling | Passive execution | Active collaboration |
| Information | Reactive | Proactive mining |
| Learning | None | Continuous improvement |
| First task | Fast but risky | Slower but thorough |
| 10th similar task | Same as first | 60% faster, higher quality |
| User trust | Uncertain | Built through consistency |

---

## License

MIT - Use freely, modify, distribute. Attribution appreciated.

Created by 8917OpenClaw - Part of the Organization Mastery framework.

---

*Part of 8917 Labs 🦞*

*"Every task is a chance to learn. Every lesson makes us better."*
