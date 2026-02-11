# Context Capsule Quick Start

Get started with intent engineering in 5 minutes.

## 1. Create Your First Intent

```bash
cd /home/node/.openclaw/workspace
cp templates/intent-capsule.md intents/my-first-intent.md
```

## 2. Fill Out the Template

Edit `intents/my-first-intent.md`:

### Objective (Required)
Explain the problem + why it matters. Use "so that" or "because" to connect problem to impact.

**Example:**
```markdown
## Objective

Help customers resolve Tier-1 technical issues without frustration so they can get back to work quickly and maintain trust in our product.
```

### Desired Outcomes (Required, 2-4 items)
Observable states from user perspective. NOT activities the agent performs.

**Good:**
- Customer confirms issue is resolved
- No follow-up ticket within 24 hours

**Bad:**
- Agent sends troubleshooting steps (activity, not outcome)
- Agent searches knowledge base (activity, not outcome)

### Health Metrics (Required)
What must NOT degrade while optimizing for outcomes.

**Example:**
- Response accuracy stays >95%
- Escalation rate remains <15%
- Customer satisfaction >4.0/5

### Constraints (Required)
**Steering** (prompt layer, guides thinking):
- Prioritize clarity over speed
- Use simple language

**Hard** (enforced in code, non-negotiable):
- Never access payment data
- Max 3 API calls per request
- Response time <2 seconds

### Decision Types (Required)
**Autonomous:**
- Standard troubleshooting
- Providing documentation

**Escalate to Human:**
- Refund requests >$50
- Security issues
- After 3 failed attempts

### Stop Rules (Required)
**Complete:** Customer confirms resolved  
**Escalate:** Unable to resolve after 3 attempts  
**Halt:** Security violation detected

## 3. Validate Your Intent

```bash
python3 templates/validate_intent.py intents/my-first-intent.md
```

Validator checks:
- ✅ All required sections present
- ✅ Objective explains WHY
- ✅ Outcomes are states (not activities)
- ✅ 2-4 outcomes defined
- ✅ Both constraint types present
- ✅ Decision boundaries clear
- ✅ Stop rules comprehensive

## 4. Common Mistakes

### ❌ Activity-Based Outcomes
```markdown
- Agent creates ticket
- Agent searches database
```

### ✅ State-Based Outcomes
```markdown
- Customer confirms issue resolved
- Ticket marked as closed
```

### ❌ Vague Objective
```markdown
Handle customer support efficiently.
```

### ✅ Clear Objective with WHY
```markdown
Help customers resolve issues quickly so they can get back to work without frustration.
```

### ❌ Missing Hard Constraints
```markdown
## Constraints
- Be polite
- Respond quickly
```

### ✅ Steering + Hard Constraints
```markdown
## Constraints

### Steering Constraints
- Be polite and empathetic
- Respond quickly

### Hard Constraints
- Never access payment data
- Max 3 API calls per request
```

## 5. Next Steps

Once validated:
1. Intent is ready for overnight builder (2 AM cron)
2. Builder will generate LangChain agent
3. Check `flogs/YYYY-MM-DD/` for build results
4. Test generated agent
5. Iterate based on results

## Examples

See `templates/example-customer-support.md` for a complete, validated example.

---

**Pro Tip:** If you can hand your intent to another human and they'd make the same decisions under pressure, your agent has a chance. If not, it will optimize something you forgot to say out loud.
