# Intent: [Name]

**Priority**: [low|medium|high|critical]

## Objective

[The problem to solve + why it matters. Guides trade-offs when ambiguity arises.]

Example: "Help customers resolve Tier-1 issues without frustration so they can get back to work."

## Desired Outcomes

[Observable states that indicate success. From user/stakeholder perspective, not agent's perspective. 2-4 outcomes max.]

- [ ] [Outcome 1: Observable, measurable state change]
- [ ] [Outcome 2: From user perspective]
- [ ] [Outcome 3: Verifiable without agent self-report]

## Health Metrics (Non-Regression)

[What must NOT degrade while optimizing for outcomes. Prevents shortcuts and quality drops.]

- [Metric 1: e.g., Response accuracy must stay >95%]
- [Metric 2: e.g., No increase in escalation rate]
- [Metric 3: e.g., Customer satisfaction remains >4.0/5]

## Strategic Context

[The system we operate in. Business constraints, technical environment, user expectations.]

- **Business Context**: [Why this matters to the organization]
- **Technical Context**: [Systems, APIs, tools available]
- **User Context**: [Who uses this, their expectations]

## Constraints

### Steering Constraints (Prompt Layer)
[Guide agent thinking and trade-offs. Soft boundaries.]

- [Constraint 1: e.g., Prioritize clarity over speed]
- [Constraint 2: e.g., Use simple language, avoid jargon]

### Hard Constraints (Enforced in Orchestration)
[Non-negotiable boundaries. Enforced in code, not prompts.]

- [Constraint 1: e.g., Never access customer payment data]
- [Constraint 2: e.g., Maximum 3 API calls per request]
- [Constraint 3: e.g., Response time <2 seconds]

## Decision Types & Autonomy

[Which decisions the agent may take autonomously vs must escalate.]

### Autonomous Decisions
- [Decision type 1: e.g., Standard troubleshooting steps]
- [Decision type 2: e.g., Providing documentation links]

### Escalate to Human
- [Decision type 1: e.g., Refund requests >$100]
- [Decision type 2: e.g., Account security issues]
- [Decision type 3: e.g., Ambiguous edge cases]

## Stop Rules

[When to halt, escalate, or complete.]

### Complete Successfully When:
- [Condition 1: e.g., Customer confirms issue resolved]
- [Condition 2: e.g., All outcomes achieved]

### Escalate When:
- [Condition 1: e.g., Unable to resolve after 3 attempts]
- [Condition 2: e.g., Customer requests human agent]
- [Condition 3: e.g., Constraint violation detected]

### Halt Immediately When:
- [Condition 1: e.g., Security violation detected]
- [Condition 2: e.g., Data integrity risk]

## Validation Checklist

Before deploying this intent:

- [ ] Can another human make the same decisions under pressure with this spec?
- [ ] Are outcomes observable and measurable?
- [ ] Are health metrics defined to prevent optimization shortcuts?
- [ ] Are hard constraints enforced in code, not just prompts?
- [ ] Are escalation triggers clear and specific?
- [ ] Does the objective explain WHY, not just WHAT?

## Implementation Notes

[Technical details, dependencies, tools, APIs needed.]

- **Tools Required**: [List tools/APIs]
- **Dependencies**: [Other systems/agents]
- **Estimated Complexity**: [Low/Medium/High]

---

**Template Version**: 1.0  
**Based on**: Intent Engineering Framework (productcompass.pm) + Agentic Manifesto principles
