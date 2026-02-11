# Context Capsule Template System

Standardized intent engineering framework for AI agents.

## What's Included

1. **intent-capsule.md** - Template following Intent Engineering Framework
2. **validate_intent.py** - Validator checking structure and quality

## Template Structure

Based on [Intent Engineering Framework](https://www.productcompass.pm/p/intent-engineering-framework-for-ai-agents) and [Agentic Manifesto](https://dev.to/crywolfe/the-agentic-manifesto-why-agile-is-breaking-in-the-age-of-ai-agents-1939):

- **Objective**: Problem + why it matters (guides trade-offs)
- **Desired Outcomes**: Observable states (2-4 max, from user perspective)
- **Health Metrics**: Non-regression constraints (prevents shortcuts)
- **Strategic Context**: Business/technical/user environment
- **Constraints**: Steering (prompt) + Hard (enforced in code)
- **Decision Types**: Autonomous vs escalate
- **Stop Rules**: Complete/escalate/halt conditions

## Usage

### Create New Intent

```bash
cp templates/intent-capsule.md intents/my-new-intent.md
# Edit the file, replacing placeholders
```

### Validate Intent

```bash
python templates/validate_intent.py intents/my-new-intent.md
```

Validator checks:
- ✅ Required sections present
- ✅ Objective explains WHY (not just WHAT)
- ✅ Outcomes are states (not activities)
- ✅ 2-4 outcomes defined
- ✅ Health metrics prevent optimization shortcuts
- ✅ Both steering and hard constraints defined
- ✅ Autonomous vs escalation decisions clear
- ✅ Stop rules comprehensive

## Example: Customer Support Agent

```markdown
## Objective

Help customers resolve Tier-1 issues without frustration so they can get back to work.

## Desired Outcomes

- [ ] Customer confirms their issue is resolved
- [ ] No follow-up ticket on same topic within 24 hours
- [ ] Customer rates interaction as helpful

## Health Metrics

- Response accuracy must stay >95%
- No increase in escalation rate
- Customer satisfaction remains >4.0/5
```

## Integration with Overnight Builder

The overnight builder (2 AM cron) can validate intents before building:

```bash
# In overnight builder script
for intent in intents/*.md; do
  if python templates/validate_intent.py "$intent"; then
    # Build agent from validated intent
  else
    # Log validation errors, skip build
  fi
done
```

## Philosophy

**"Context without intent is noise."**

Agents fail not because they can't reason, but because objectives, outcomes, and constraints are underspecified. This template ensures every intent is:

1. **Clear**: Objective explains why, not just what
2. **Measurable**: Outcomes are observable states
3. **Bounded**: Constraints prevent harmful optimization
4. **Autonomous**: Decision boundaries explicit
5. **Safe**: Stop rules prevent runaway behavior

## Next Steps

1. ✅ Template created
2. ✅ Validator built
3. 🔄 Migrate existing intents to new format
4. 🔄 Integrate with intent-to-agent compiler
5. 🔄 Add to overnight builder validation

---

**Version**: 1.0  
**Created**: 2026-02-11  
**Based on**: Intent Engineering Framework + Agentic Manifesto principles
