# Assumption Challenger

Systematically identifies and stress-tests assumptions that are treated as facts but may not be validated.

## When to Use

- Validating roadmaps and project plans
- Reviewing architecture proposals
- Assessing build vs buy decisions
- Evaluating timelines and budgets
- Challenging strategic initiatives

## Why Assumptions Matter

Most project failures trace back to invalid assumptions:
- **Timeline assumptions**: "We can ship in 6 weeks" (based on nothing)
- **Resource assumptions**: "We'll hire 3 engineers" (in a tight market)
- **Technical assumptions**: "The API can handle 10K requests/sec" (never tested)
- **Business assumptions**: "Users will adopt this feature" (never validated)

**The cost of invalid assumptions compounds over time.** A bad assumption in week 1 can waste months of work.

---

## Assumption Categories

### 1. Timeline Assumptions
Assumptions about how long things will take.

**Common patterns**:
- "This should only take 2 weeks"
- "We'll have the integration done by launch"
- "The team can absorb this additional scope"

**Challenge questions**:
- What's this estimate based on? Past experience or hope?
- What similar work have we done? How long did it actually take?
- What's not included in this estimate? (Testing, documentation, deployment)
- What happens if this takes 2x longer?

### 2. Resource Assumptions
Assumptions about team capacity and availability.

**Common patterns**:
- "We'll hire 2 senior engineers by Q2"
- "The DevOps team can support this"
- "Sarah can lead this while maintaining her other work"

**Challenge questions**:
- What's the hiring timeline? What if we can't find the right people?
- What's the team's current utilization? Where does time come from?
- Who's the backup if the key person is unavailable?
- What happens if the team is 50% of expected capacity?

### 3. Technical Assumptions
Assumptions about system capabilities and constraints.

**Common patterns**:
- "The database can handle the load"
- "We can integrate with their API easily"
- "Our architecture supports this use case"

**Challenge questions**:
- Has this been tested at the required scale?
- What are the documented limits? What happens at those limits?
- What's the failure mode? How do we recover?
- Have we talked to the API provider about our usage patterns?

### 4. Business Assumptions
Assumptions about market, users, and business outcomes.

**Common patterns**:
- "Users want this feature"
- "This will reduce churn by 20%"
- "The market will wait for our solution"

**Challenge questions**:
- What evidence supports this? User research? Data?
- What if users don't adopt this? What's the fallback?
- What are competitors doing in this space?
- How will we know if this assumption is wrong?

### 5. External Assumptions
Assumptions about factors outside your control.

**Common patterns**:
- "The vendor will have the feature ready"
- "Regulations won't change"
- "The market will remain stable"

**Challenge questions**:
- What's our contingency if this doesn't happen?
- What's the vendor's track record on commitments?
- What early warning signs would indicate this is wrong?
- What's the cost of being wrong?

---

## Assumption Identification Process

### Step 1: Surface Assumptions

Read the proposal and identify statements that are treated as facts but aren't validated:

**Flag statements containing**:
- "We will..." (without evidence)
- "We can..." (without proof)
- "Users want..." (without data)
- "It should..." (without testing)
- "We expect..." (without basis)
- "We assume..." (at least they're honest)

### Step 2: Categorize Assumptions

For each assumption, categorize:

| Category | Risk if Wrong | Validation Difficulty |
|----------|---------------|----------------------|
| Timeline | Project delay | Medium (compare to past) |
| Resource | Execution failure | Medium (check market) |
| Technical | System failure | High (requires testing) |
| Business | Wasted investment | High (requires market validation) |
| External | Plans disrupted | Variable |

### Step 3: Assess Each Assumption

For each significant assumption:

```markdown
### Assumption: [Statement]

**Category**: [Type]
**Stated or Implicit**: [Was it stated or hidden?]

**Evidence Supporting**:
- [Evidence 1]
- [Evidence 2]

**Evidence Against**:
- [Counter-evidence 1]
- [Counter-evidence 2]

**Risk if Wrong**:
- [Impact on timeline]
- [Impact on cost]
- [Impact on success]

**Validation Method**:
- [How to test this assumption]
- [Cost/time to validate]

**Verdict**:
[ ] Valid - Evidence supports
[ ] Questionable - Needs validation
[ ] Invalid - Evidence contradicts
[ ] Unknown - Cannot assess
```

### Step 4: Prioritize Challenges

Focus on assumptions that are:
1. **High impact** - Project fails if wrong
2. **Low evidence** - Based on hope, not data
3. **Testable** - Can be validated before commitment

---

## Challenge Patterns

### The Reality Check
Compare assumption to external data.

**Template**:
> "You assume [X]. Industry data shows [Y]. What makes you different?"

**Example**:
> "You assume you can hire 3 senior engineers in 2 months. The average time-to-hire for senior engineers in your market is 4-6 months. What's your strategy to beat that?"

### The History Test
Compare to organization's past performance.

**Template**:
> "You assume [X]. Last time you attempted [similar thing], it took [Y]. What's changed?"

**Example**:
> "You assume 8 weeks for the microservices migration. Your last infrastructure migration took 5 months. What's different this time?"

### The Stress Test
Push assumption to failure point.

**Template**:
> "You assume [X]. What happens when [stress scenario]?"

**Example**:
> "You assume the system handles 10K concurrent users. What happens during a flash sale with 50K? What's the failure mode?"

### The Dependency Audit
Trace assumption to its dependencies.

**Template**:
> "For [assumption] to be true, what else must be true?"

**Example**:
> "For your 6-week timeline to work, you need: (1) API specs finalized by week 1, (2) no scope changes, (3) 100% team availability, (4) no production incidents. How realistic is that?"

### The Inverse Test
Consider what happens if assumption is wrong.

**Template**:
> "If [assumption] is wrong, what's the impact? What's your Plan B?"

**Example**:
> "If users don't adopt this feature, what's the fallback? Have you defined failure criteria?"

---

## Wishful Thinking Indicators

Red flags that suggest assumption is based on hope rather than evidence:

### 1. The Optimistic Timeline
- "Should only take..."
- "If everything goes well..."
- "We can do it if we're focused..."

**Reality**: Things rarely go perfectly. Add 30-50% buffer.

### 2. The Magical Hiring
- "We'll just hire..."
- "Once we have the team..."
- "We're planning to bring on..."

**Reality**: Hiring takes 3-6 months for senior roles. Onboarding adds another 2-3 months to productivity.

### 3. The Simple Integration
- "It's just an API call..."
- "Should be straightforward..."
- "They have good documentation..."

**Reality**: Integrations always have edge cases, rate limits, and unexpected behaviors.

### 4. The Obvious Market
- "Everyone needs this..."
- "Users have been asking for..."
- "It's clear that..."

**Reality**: "Everyone" is not a market segment. Validate with actual user research.

### 5. The Linear Scaling
- "If we can do X, we can do 10X..."
- "We'll scale as needed..."
- "Growth shouldn't be a problem..."

**Reality**: Scaling is non-linear. What works at 10K users may fail at 100K.

---

## Output Format

When challenging assumptions, provide:

```markdown
# Assumption Analysis: [Plan/Proposal Name]

## Summary
- **Total Assumptions Identified**: [Count]
- **High-Risk Assumptions**: [Count]
- **Requires Immediate Validation**: [Count]

## Critical Assumptions (Must Validate Before Proceeding)

### Assumption 1: [Statement]

**Category**: Timeline / Resource / Technical / Business / External
**Stated or Implicit**: Stated / Implicit

**The Problem**:
[Why this assumption is questionable]

**Evidence For**:
- [Supporting evidence]

**Evidence Against**:
- [Counter-evidence]

**If Wrong, Impact**:
- Timeline: [Impact]
- Budget: [Impact]
- Success: [Impact]

**How to Validate**:
- [Validation method]
- [Time required]
- [Cost]

**Verdict**: Valid / Questionable / Invalid / Unknown

---

### Assumption 2: [Statement]
[Same format]

---

## Medium-Risk Assumptions (Should Validate)
[List with brief analysis]

## Low-Risk Assumptions (Monitor)
[List]

## Recommendations

### Before Proceeding
1. [Validation action 1]
2. [Validation action 2]

### Risk Mitigation
1. [Mitigation for assumption 1]
2. [Mitigation for assumption 2]

### Contingency Plans Needed
1. [Plan B for assumption 1]
2. [Plan B for assumption 2]
```

---

## Integration with Validation

The assumption-challenger skill feeds into the broader validation workflow:

```
Proposal/Plan
     │
     ▼
[assumption-challenging] → List of assumptions with verdicts
     │
     ▼
[antipattern-detection] → Identified anti-patterns
     │
     ▼
[validation-reports] → Final 8-section report
```

---

## Challenge Questions by Category

Ready-to-use questions for challenging assumptions in proposals and plans.

### Timeline Assumptions

#### Duration Estimates
- What's this estimate based on? Past projects or intuition?
- What similar work has the team done before? How long did it actually take?
- Does this estimate include testing, documentation, and deployment?
- What's the buffer for unexpected issues? (Every project has them)
- If this takes 2x longer, what's the impact on the overall plan?

#### Deadline Commitments
- What's driving this deadline? Is it real or arbitrary?
- What happens if we miss this deadline by 2 weeks? 4 weeks?
- Who committed to this timeline and on what basis?
- What scope can be cut if we can't hit the deadline?
- Has the team agreed this timeline is achievable?

#### Parallel Work
- You're planning X, Y, and Z in parallel. Do you have the staff for that?
- What happens when these parallel tracks need to integrate?
- Who's the point person for each track? Do they have capacity?
- What's the critical path? What delays everything if it slips?

---

### Resource Assumptions

#### Hiring
- What's your time-to-hire for this role? (Industry average is 3-6 months for senior)
- What's your offer acceptance rate? What if candidates decline?
- Where will these candidates come from? Do you have a pipeline?
- What happens to the project if you only fill 50% of planned hires?
- How long until new hires are productive? (Usually 2-3 months)

#### Team Capacity
- What's the team's current utilization? Where does time for this come from?
- Is anyone on this team also committed to other projects?
- What happens during vacations, sick days, or turnover?
- Who's the backup if the key technical lead is unavailable?
- Have you accounted for support and maintenance of existing systems?

#### Skills
- Does the team have experience with this technology?
- What's the learning curve? Is that factored into the timeline?
- Who's the expert? What if they leave?
- Do you need external help? Is that budgeted?

---

### Technical Assumptions

#### Performance
- Has this been tested at the required scale?
- What's the current performance baseline? What's the target?
- What happens when you hit 2x, 5x, 10x the expected load?
- What's the failure mode? Graceful degradation or crash?
- Have you identified the bottleneck? Is it CPU, memory, network, database?

#### Integration
- Have you talked to the team that owns this API/service?
- What's the API's documented rate limit? What happens when you hit it?
- Is there a staging environment you can test against?
- What's the API's uptime SLA? What's your fallback when it's down?
- Has anyone on the team done this integration before?

#### Architecture
- Does the current architecture support this use case?
- What changes are required to existing systems?
- Have you considered backward compatibility?
- What's the rollback plan if this doesn't work?
- Is this introducing new single points of failure?

#### Data
- Do you have the data you need? In the format you need?
- What's the data quality? Have you validated it?
- Are there privacy/compliance implications?
- What's the data volume? Is your system designed for that?
- Who owns this data? Can you use it for this purpose?

---

### Business Assumptions

#### User Behavior
- What evidence shows users want this feature?
- Have you talked to actual users? How many?
- What's the expected adoption rate? Based on what?
- What if users don't adopt this? What's the fallback?
- How will you measure success? What's the threshold?

#### Market
- What's the competitive landscape? What are others doing?
- What's the time-to-market pressure? What happens if you're late?
- Is the market stable or changing? How will that affect this?
- What's your differentiation? Why will customers choose you?

#### Revenue/Cost
- What's the expected ROI? What's that based on?
- What if costs are 2x higher than projected?
- What if revenue is 50% of projected?
- What's the break-even point? When do you expect to hit it?
- What's the opportunity cost of doing this vs. other initiatives?

---

### External Dependencies

#### Vendors
- What's the vendor's track record on delivery commitments?
- Do you have a contract? What are the SLAs?
- What's the cost at scale? Is there a ceiling?
- What's the lock-in risk? How hard is it to switch?
- Who's the backup vendor if this one fails?

#### Partners
- What's the partner's incentive to deliver on time?
- What do they get from this partnership?
- What's the escalation path if they're slow?
- Have you worked with them before? How did it go?

#### Regulatory
- What regulations apply? Are you sure you're compliant?
- What happens if regulations change?
- Have you talked to legal/compliance?
- What's the cost of getting this wrong?

---

### Meta Questions

#### Evidence Quality
- What evidence supports this assumption?
- Is this assumption stated explicitly or implied?
- Who made this assumption? What's their expertise?
- When was this last validated? Is it still true?

#### Consequence Analysis
- If this assumption is wrong, what's the blast radius?
- Can we continue if this assumption fails?
- What early warning signs would indicate this is wrong?
- What's the cost of validating this assumption now vs. finding out later?

#### Alternative Scenarios
- What's the best case? What's the worst case? What's most likely?
- What would have to be true for the worst case to happen?
- What's Plan B if this assumption proves wrong?
- Can we design the project to be less dependent on this assumption?

---

## Challenge Intensity Levels

### Level 1: Gentle Probe
Use when: Initial exploration, building rapport
> "Help me understand the thinking behind this assumption..."
> "What led you to this conclusion?"

### Level 2: Direct Challenge
Use when: Significant concerns, need clarity
> "I'm not seeing evidence for this. What are we basing it on?"
> "This seems optimistic. What's the realistic scenario?"

### Level 3: Stress Test
Use when: High-stakes decisions, pattern of optimism
> "Walk me through the failure scenario. What happens when this is wrong?"
> "I've seen this assumption fail in 3 other projects. What's different here?"

### Level 4: Hard Stop
Use when: Critical flaws, must address before proceeding
> "I can't validate this plan while this assumption is unverified. We need to test this first."
> "This assumption is the foundation of the entire plan. If it's wrong, everything falls apart."

---

## Question Selection Guide

| Situation | Recommended Questions |
|-----------|----------------------|
| First review | Start with evidence quality questions |
| Technical proposal | Focus on technical and performance questions |
| Business case | Focus on market and ROI questions |
| Timeline-driven | Focus on timeline and resource questions |
| External dependencies | Focus on vendor and partner questions |
| High uncertainty | Use meta questions liberally |
