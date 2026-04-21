# Validation Report Generator

Transforms validation analysis into structured, actionable reports that provide clear verdicts and specific guidance.

## When to Use

- After completing validation analysis of a plan, proposal, or architecture
- When producing final deliverable for rnd-mentor
- When formalizing feedback into a consistent, comprehensive format
- Before handing off validated/rejected work back to the requester

## Report Structure

Every validation report follows the **8-Section Format**:

### Section 1: Verdict
**Purpose**: Unambiguous assessment with confidence level

**Options**:
- **GOOD**: Ready for implementation (may have minor suggestions)
- **NEEDS MAJOR WORK**: Fundamentally sound but has significant gaps
- **BAD**: Should not proceed without fundamental rethinking

**Include**:
- Clear verdict (one of the three options)
- Confidence level (High/Medium/Low)
- One-sentence summary of why

### Section 2: What You Got Right
**Purpose**: Acknowledge genuine strengths (builds trust for criticism)

**Include**:
- 2-3 specific things done well
- Why each matters
- What to preserve in revisions

**Avoid**:
- Generic praise ("good work!")
- Inflating minor positives
- Praising the obvious

### Section 3: Critical Flaws
**Purpose**: Expose fatal or near-fatal weaknesses

**Format for each flaw**:
```
**Flaw**: [What's wrong]
**Why It Matters**: [Business/technical impact]
**Consequence**: [What happens if not addressed]
```

**Include**:
- Prioritized list (most critical first)
- Specific evidence, not vague concerns
- Impact quantification where possible

### Section 4: What You're Not Considering
**Purpose**: Surface blindspots and hidden assumptions

**Types of blindspots**:
- Unstated assumptions (treated as facts)
- Ignored failure modes
- Missing stakeholders
- External dependencies not accounted for
- Scale implications not considered

**Include**:
- What was assumed vs. what should be validated
- Questions that should have been asked
- Scenarios that weren't explored

### Section 5: The Real Question
**Purpose**: Reframe if solving wrong problem

**When to use**:
- Problem definition is too narrow/broad
- Symptoms treated instead of root cause
- Constraint accepted that should be challenged
- Solution in search of a problem

**Format**:
> "You're asking [stated question], but the real question might be [reframed question]."

**Skip if**: The problem is correctly framed (state this explicitly)

### Section 6: What Bulletproof Looks Like
**Purpose**: Define success criteria for revision

**Include**:
- Specific criteria for acceptable solution
- Measurable outcomes
- What evidence would prove the concerns addressed

**Format**:
```
For this to be ready for implementation:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

### Section 7: Recommended Path Forward
**Purpose**: Concrete next steps

**If GOOD**:
- Any minor improvements before proceeding
- What to monitor during implementation
- Validation checkpoints

**If NEEDS MAJOR WORK**:
- Specific areas to revise
- Suggested approach for each
- Whether to route back to architect

**If BAD**:
- Alternative approaches to consider
- What fundamental rethinking is needed
- Whether to restart with different framing

### Section 8: Questions You Need to Answer First
**Purpose**: Information gaps blocking progress

**Include**:
- Questions that must be answered before proceeding
- Who can answer each question
- What decisions are blocked until answered

---

## Generating the Report

### Step 1: Gather Analysis
Before generating report, ensure you have completed:
- [ ] Assumption identification
- [ ] Risk assessment (7 dimensions)
- [ ] Anti-pattern detection
- [ ] Timeline/budget reality check
- [ ] Team capacity evaluation

### Step 2: Determine Verdict
Use the Verdict Criteria to classify:

**GOOD if**:
- Core assumptions are valid
- Timeline is realistic
- Budget is appropriate
- Team can execute
- Risks are manageable
- No fundamental anti-patterns

**NEEDS MAJOR WORK if**:
- Core approach is sound but...
- Significant gaps exist in 2+ areas
- Timeline/budget needs adjustment
- Some assumptions need validation

**BAD if**:
- Core assumptions are invalid
- Fundamental anti-pattern detected
- Timeline is fantasy
- Budget is unrealistic by >50%
- Team cannot execute
- Wrong problem being solved

### Step 3: Gather Evidence
For each section, cite specific evidence:
- Quote from the proposal
- Data points that contradict claims
- Industry benchmarks
- Historical precedent

### Step 4: Calibrate Tone
Match tone to verdict:

| Verdict | Tone |
|---------|------|
| GOOD | Affirming with minor suggestions |
| NEEDS MAJOR WORK | Constructive but direct |
| BAD | Brutally honest but respectful |

### Step 5: Write Report
Use the Report Template below to structure output.

---

## Output Format

```markdown
# Validation Report: [Title]

**Date**: [Date]
**Validated By**: rnd-mentor
**Subject**: [What was validated]

---

## 1. Verdict

### VERDICT: [GOOD / NEEDS MAJOR WORK / BAD]
**Confidence**: [High / Medium / Low]

[One-sentence summary of why this verdict]

---

## 2. What You Got Right

[2-3 specific strengths with explanation of why they matter]

---

## 3. Critical Flaws

### Flaw 1: [Title]
**Why It Matters**: [Impact]
**Consequence**: [What happens if not addressed]

### Flaw 2: [Title]
...

---

## 4. What You're Not Considering

[Blindspots, hidden assumptions, ignored scenarios]

---

## 5. The Real Question

[Reframe if needed, or state "Problem is correctly framed"]

---

## 6. What Bulletproof Looks Like

For this to be ready for implementation:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## 7. Recommended Path Forward

[Specific next steps based on verdict]

---

## 8. Questions You Need to Answer First

| Question | Who Can Answer | Blocks |
|----------|---------------|--------|
| [Question 1] | [Person/Team] | [Decision blocked] |

---

*This validation was conducted by rnd-mentor using standard validation protocol.*
```

---

## Quality Checklist

Before delivering report, verify:

- [ ] Verdict is clear and justified
- [ ] Strengths are genuine (not inflated)
- [ ] Flaws are specific with evidence
- [ ] Blindspots go beyond surface issues
- [ ] Reframe is warranted (or explicitly skipped)
- [ ] Success criteria are measurable
- [ ] Path forward is actionable
- [ ] Questions are answerable and necessary
- [ ] Tone matches verdict severity
- [ ] No generic feedback (everything is specific)

---

## Report Template

Full markdown template for validation reports.

---

```markdown
# Validation Report: [Brief Title of What's Being Validated]

**Date**: [YYYY-MM-DD]
**Validated By**: rnd-mentor
**Subject**: [Plan/Architecture/Proposal] for [System/Feature/Initiative]
**Requested By**: [Who asked for validation]

---

## 1. Verdict

### VERDICT: [GOOD / NEEDS MAJOR WORK / BAD]

**Confidence**: [High / Medium / Low]

> [One-sentence summary explaining the verdict. Be direct and specific.]

**Risk Profile**:
| Dimension | Rating | Notes |
|-----------|--------|-------|
| Business Impact | [Low/Med/High] | [Brief note] |
| Technical Risk | [Low/Med/High] | [Brief note] |
| Timeline Risk | [Low/Med/High] | [Brief note] |
| Team Risk | [Low/Med/High] | [Brief note] |

---

## 2. What You Got Right

### Strength 1: [Specific thing done well]
[Why this matters and what it demonstrates about the thinking]

### Strength 2: [Specific thing done well]
[Why this matters and what to preserve]

### Strength 3: [Specific thing done well] *(optional)*
[Why this matters]

---

## 3. Critical Flaws

### Flaw 1: [Clear title describing the flaw]

**The Problem**:
[Specific description of what's wrong]

**Why It Matters**:
[Business or technical impact - quantify if possible]

**Consequence If Not Addressed**:
[What happens if this goes to production/implementation as-is]

**Evidence**:
> [Quote from proposal or specific data point that supports this flaw]

---

### Flaw 2: [Clear title]

**The Problem**:
[Description]

**Why It Matters**:
[Impact]

**Consequence If Not Addressed**:
[Outcome]

**Evidence**:
> [Supporting evidence]

---

### Flaw 3: [Clear title] *(if applicable)*

[Same format]

---

## 4. What You're Not Considering

### Hidden Assumptions

| Assumption Made | Reality Check | Risk |
|-----------------|---------------|------|
| [What was assumed as fact] | [Why it might not be true] | [Consequence] |
| [Another assumption] | [Reality] | [Risk] |

### Blindspots

1. **[Blindspot title]**: [Description of what wasn't considered and why it matters]

2. **[Blindspot title]**: [Description]

### Scenarios Not Explored

- **What if [scenario]?** [Why this matters]
- **What if [scenario]?** [Why this matters]

---

## 5. The Real Question

<!-- Use ONE of these formats: -->

<!-- If reframe is needed: -->
### Problem Reframe Needed

**You're asking**: "[The stated question/problem]"

**But the real question might be**: "[Reframed question that gets at the actual issue]"

**Why this matters**: [Explanation of why the reframe changes the approach]

<!-- OR if problem is correctly framed: -->
### Problem is Correctly Framed

The problem definition is appropriate. The proposal correctly identifies [what it correctly identifies] and is solving the right problem.

---

## 6. What Bulletproof Looks Like

For this [plan/architecture/proposal] to be ready for implementation, it must:

### Must-Have Criteria
- [ ] **[Criterion 1]**: [Measurable definition of success]
- [ ] **[Criterion 2]**: [Measurable definition]
- [ ] **[Criterion 3]**: [Measurable definition]

### Evidence Required
- [ ] [What proof would validate the assumptions]
- [ ] [What data would confirm the approach]

### Validation Checkpoints
- [ ] [Checkpoint 1]: Before [milestone], confirm [what]
- [ ] [Checkpoint 2]: At [milestone], verify [what]

---

## 7. Recommended Path Forward

<!-- Choose the appropriate section based on verdict: -->

### For GOOD Verdict:

**Proceed with implementation**, noting the following:

1. **Before starting**: [Minor adjustments]
2. **During implementation**: [What to monitor]
3. **Validation checkpoints**: [When to pause and verify]

**Minor improvements to consider**:
- [Suggestion 1]
- [Suggestion 2]

---

### For NEEDS MAJOR WORK Verdict:

**Do not proceed until the following are addressed**:

1. **[Area 1]**:
   - What to fix: [Specific change]
   - Suggested approach: [How to fix]
   - Who should do this: [rnd-architect / team / external]

2. **[Area 2]**:
   - What to fix: [Specific change]
   - Suggested approach: [How]
   - Who should do this: [Who]

**Recommended workflow**:
1. Route back to rnd-architect for revision
2. Address critical flaws 1 and 2
3. Re-validate before proceeding

**Timeline impact**: [Estimate of delay this introduces]

---

### For BAD Verdict:

**Do not proceed. Fundamental rethinking required.**

**Why this can't be fixed incrementally**:
[Explanation of why revision won't work]

**Alternative approaches to consider**:
1. **[Alternative 1]**: [Brief description and trade-offs]
2. **[Alternative 2]**: [Brief description and trade-offs]

**Recommended next steps**:
1. [Step 1 - e.g., Stakeholder discussion to realign goals]
2. [Step 2 - e.g., Reframe the problem]
3. [Step 3 - e.g., Start fresh with new constraints]

---

## 8. Questions You Need to Answer First

These questions must be answered before this [plan/architecture/proposal] can proceed:

| # | Question | Who Can Answer | What It Blocks | Priority |
|---|----------|---------------|----------------|----------|
| 1 | [Specific question] | [Person/team] | [Decision blocked] | Critical |
| 2 | [Specific question] | [Person/team] | [Decision blocked] | High |
| 3 | [Specific question] | [Person/team] | [Decision blocked] | Medium |

### Question Details

**Q1: [Question]**
- Why this matters: [Context]
- Possible answers and implications:
  - If [answer A]: [implication]
  - If [answer B]: [implication]

**Q2: [Question]**
- Why this matters: [Context]
- Possible answers and implications:
  - If [answer A]: [implication]
  - If [answer B]: [implication]

---

## Summary

| Aspect | Assessment |
|--------|------------|
| **Verdict** | [GOOD/NEEDS MAJOR WORK/BAD] |
| **Confidence** | [High/Medium/Low] |
| **Critical Flaws** | [Count] identified |
| **Strengths** | [Count] noted |
| **Blocking Questions** | [Count] unanswered |
| **Recommendation** | [Proceed / Revise / Restart] |

---

*This validation was conducted by rnd-mentor following standard validation protocol. The goal is to prevent costly mistakes by surfacing issues early, not to criticize for its own sake.*

*Next Steps: [Specific action - e.g., "Schedule meeting with rnd-architect to discuss revisions" or "Proceed to implementation planning"]*
```

---

## Usage Notes

### Adapting the Template

- **Skip sections that don't apply** (e.g., Reframe section if problem is correct)
- **Add sections if needed** (e.g., Compliance considerations for regulated industries)
- **Adjust depth based on scope** (MVP validation needs less than enterprise architecture)

### Tone Calibration

| Verdict | Opening Tone | Flaw Tone | Closing Tone |
|---------|-------------|-----------|--------------|
| GOOD | Affirming | Advisory | Encouraging |
| NEEDS MAJOR WORK | Neutral | Direct | Constructive |
| BAD | Sympathetic | Firm | Helpful |

### Common Mistakes

1. **Generic feedback**: Every point should be specific to this proposal
2. **Inflated strengths**: Don't praise the obvious to soften criticism
3. **Vague flaws**: "Could be better" is not actionable
4. **Missing evidence**: Every flaw needs supporting data
5. **Impossible criteria**: Bulletproof criteria should be achievable

---

## Verdict Criteria

Decision framework for determining validation verdicts.

### Verdict Options

| Verdict | Meaning | Action |
|---------|---------|--------|
| **GOOD** | Ready for implementation | Proceed (with minor notes) |
| **NEEDS MAJOR WORK** | Sound foundation, significant gaps | Revise and re-validate |
| **BAD** | Fundamentally flawed | Stop and rethink |

---

### GOOD Criteria

A proposal receives **GOOD** when ALL of the following are true:

#### Core Validity
- [ ] Core assumptions are validated or validatable
- [ ] Problem framing is correct
- [ ] Solution addresses the actual problem

#### Feasibility
- [ ] Timeline is realistic (within 20% of similar projects)
- [ ] Budget is appropriate (with reasonable contingency)
- [ ] Team has skills to execute (or clear plan to acquire)
- [ ] Technology choices are justified

#### Risk Management
- [ ] Major risks are identified
- [ ] Mitigation strategies exist for high risks
- [ ] Failure modes are considered
- [ ] Rollback plan exists

#### Quality
- [ ] Trade-offs are explicit
- [ ] Alternatives were considered
- [ ] Success metrics are defined
- [ ] Monitoring approach is specified

#### Minor Issues Acceptable
- Small optimizations possible
- Documentation gaps
- Minor scope clarifications
- Nice-to-have features deferred

---

### NEEDS MAJOR WORK Criteria

A proposal receives **NEEDS MAJOR WORK** when:

#### The foundation is sound BUT...

**Any 2+ of these are true**:
- [ ] Timeline is optimistic by 30-50%
- [ ] Budget underestimates by 30-50%
- [ ] 1-2 critical assumptions are unvalidated
- [ ] Key risks are not mitigated
- [ ] Team skill gaps are significant but addressable
- [ ] Major alternative was not considered

#### Specific Triggers

| Issue | Threshold for NEEDS MAJOR WORK |
|-------|-------------------------------|
| Timeline variance | 30-50% too optimistic |
| Budget variance | 30-50% underestimated |
| Unvalidated assumptions | 1-2 critical assumptions |
| Missing risk mitigation | High-risk areas without plans |
| Team gaps | Gaps addressable in 4-8 weeks |
| Scope issues | 20-40% scope unclear |

#### What Makes It Fixable
- Core architecture is sound
- Problem is correctly framed
- Team can address gaps
- Timeline can be adjusted
- Budget can be revised

---

### BAD Criteria

A proposal receives **BAD** when ANY of the following are true:

#### Fatal Flaws

##### Wrong Problem
- [ ] Solving symptoms, not root cause
- [ ] Constraint accepted that should be challenged
- [ ] Solution looking for a problem
- [ ] Success metrics don't align with business goals

##### Invalid Foundation
- [ ] Core assumptions are demonstrably false
- [ ] Fundamental technology mismatch
- [ ] Architecture cannot support requirements
- [ ] Data doesn't exist and can't be obtained

##### Unrealistic Execution
- [ ] Timeline is fantasy (>50% underestimate)
- [ ] Budget is impossible (>50% underestimate)
- [ ] Team cannot acquire needed skills
- [ ] Dependencies cannot be satisfied

##### Anti-Pattern Dominance
- [ ] Premature optimization driving decisions
- [ ] Shiny object syndrome (tech for tech's sake)
- [ ] Hero culture dependency (single point of failure)
- [ ] Second system effect (over-engineering)

#### Specific Triggers

| Issue | Threshold for BAD |
|-------|-------------------|
| Timeline variance | >50% too optimistic |
| Budget variance | >50% underestimated |
| Core assumption validity | >2 critical assumptions false |
| Team capability | Cannot reasonably acquire skills |
| Problem framing | Fundamentally incorrect |
| Anti-patterns | Major anti-pattern present |

---

### Confidence Levels

#### High Confidence
- Sufficient information to assess
- Domain expertise matches the proposal
- Similar projects for comparison
- Clear evidence for verdict

#### Medium Confidence
- Some information gaps (noted in Questions section)
- Adjacent domain expertise
- Limited comparable projects
- Verdict based on patterns/experience

#### Low Confidence
- Significant information gaps
- Novel domain for evaluator
- No comparable projects
- Verdict is best guess (recommend expert review)

---

### Edge Cases

#### Mixed Signals

When different dimensions give different signals:

| If you have... | Verdict | Rationale |
|----------------|---------|-----------|
| 1 BAD signal, rest GOOD | NEEDS MAJOR WORK | One fatal flaw can be addressed |
| 2+ BAD signals | BAD | Multiple fundamental issues |
| All borderline | NEEDS MAJOR WORK | Cumulative risk too high |

#### Insufficient Information

| Information Level | Approach |
|-------------------|----------|
| >80% complete | Give verdict with notes |
| 50-80% complete | Give verdict with Low confidence |
| <50% complete | Cannot validate - request more info |

#### Scope Mismatch

| Situation | Approach |
|-----------|----------|
| Proposal too ambitious | BAD if unrealistic, otherwise NEEDS MAJOR WORK with scope reduction |
| Proposal too limited | GOOD with expansion recommendations |
| Wrong scope entirely | BAD - reframe needed |

---

### Decision Tree

```
START
  │
  ├─► Is the problem correctly framed?
  │     NO ──────────────────────────────────────► BAD
  │     YES
  │       │
  │       ▼
  ├─► Are core assumptions valid?
  │     >2 invalid ──────────────────────────────► BAD
  │     1-2 questionable ────► (continue with caution)
  │     All valid
  │       │
  │       ▼
  ├─► Is timeline realistic?
  │     >50% underestimate ──────────────────────► BAD
  │     30-50% underestimate ──► (flag for NEEDS MAJOR WORK)
  │     Within 30%
  │       │
  │       ▼
  ├─► Is budget realistic?
  │     >50% underestimate ──────────────────────► BAD
  │     30-50% underestimate ──► (flag for NEEDS MAJOR WORK)
  │     Within 30%
  │       │
  │       ▼
  ├─► Can team execute?
  │     Cannot acquire skills ───────────────────► BAD
  │     Significant gaps ──────► (flag for NEEDS MAJOR WORK)
  │     Team capable
  │       │
  │       ▼
  ├─► Are major anti-patterns present?
  │     Dominant anti-pattern ───────────────────► BAD
  │     Minor anti-pattern ────► (flag for NEEDS MAJOR WORK)
  │     None detected
  │       │
  │       ▼
  └─► Count flags for NEEDS MAJOR WORK
        0-1 flags ───────────────────────────────► GOOD
        2+ flags ────────────────────────────────► NEEDS MAJOR WORK
```

---

### Calibration Examples

#### Example 1: GOOD

**Proposal**: Notification system architecture
- Timeline: 8 weeks (realistic for scope)
- Budget: $3K/month (aligned with scale)
- Team: 2 backend engineers (sufficient)
- Assumptions: All validated
- Risks: Identified with mitigations

**Verdict**: GOOD
**Confidence**: High
**Notes**: Minor suggestions for monitoring approach

---

#### Example 2: NEEDS MAJOR WORK

**Proposal**: Microservices migration
- Timeline: 8 weeks (similar projects took 16+ weeks)
- Budget: $10K/month (realistic)
- Team: 3 engineers (need DevOps skills)
- Assumptions: 2 unvalidated (database performance, traffic patterns)
- Risks: Some identified, missing failure modes

**Verdict**: NEEDS MAJOR WORK
**Confidence**: High
**Reasons**: Timeline 50% underestimated, team gap, unvalidated assumptions

---

#### Example 3: BAD

**Proposal**: AI-powered recommendation engine
- Timeline: 4 weeks (impossible for ML system)
- Budget: $1K/month (need $10K+ for compute)
- Team: No ML experience
- Assumptions: "We have enough data" (have 1000 records, need 100K)
- Anti-pattern: Shiny object syndrome (want AI, don't have AI problem)

**Verdict**: BAD
**Confidence**: High
**Reasons**: Timeline fantasy, budget impossible, team can't execute, core assumption invalid, wrong problem

---

### Final Notes

#### Be Honest, Not Harsh
- BAD verdict is not failure—it's preventing expensive failure
- Deliver hard truths with respect
- Always provide path forward

#### Err Toward Caution
- When in doubt between GOOD and NEEDS MAJOR WORK → NEEDS MAJOR WORK
- When in doubt between NEEDS MAJOR WORK and BAD → NEEDS MAJOR WORK (but with strong warnings)
- Better to over-validate than under-validate

#### Document Reasoning
- Always explain WHY each verdict criterion applied
- Cite specific evidence
- Make reasoning auditable
