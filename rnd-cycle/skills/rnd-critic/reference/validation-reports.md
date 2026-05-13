# Validation Reports

Structured report format for adversarial validation of plans, proposals, decisions, and roadmaps. **Used by `/rnd:validate`** — the heavy adversarial pass. `/rnd:plan` uses the compact verdict format from `plan-verification.md` instead.

## When to Use

- After completing assumption-challenging + antipattern-detection + (if build plans) plan-verification
- When producing a final 8-section deliverable with a clear verdict
- Before handing off validated or rejected work back to the requester

## 8-Section Report

| # | Section | Purpose | Gates verdict? |
|---|---|---|---|
| 1 | **Verdict** | Unambiguous assessment + confidence | Yes — this IS the verdict |
| 2 | **What You Got Right** | Genuine strengths (builds trust for criticism) | No |
| 3 | **Critical Flaws** | Fatal or near-fatal weaknesses | Yes — presence → not GOOD |
| 4 | **What You're Not Considering** | Blindspots, hidden assumptions | No |
| 5 | **The Real Question** | Reframe if solving wrong problem (skip if framing is correct) | No |
| 6 | **What Bulletproof Looks Like** | Success criteria for revision | Yes — measurable checkboxes |
| 7 | **Recommended Path Forward** | Concrete next steps, routes by verdict | Yes — actionable steps |
| 8 | **Questions to Answer First** | Information gaps blocking progress | Yes — blockers explicit |

## Verdict Options

| Verdict | Meaning | Action |
|---|---|---|
| **GOOD** | Ready for implementation | Proceed with minor notes |
| **NEEDS MAJOR WORK** | Sound foundation, significant gaps | Revise and re-validate |
| **BAD** | Fundamentally flawed | Stop and rethink |

### GOOD Criteria (ALL must hold)

- Core assumptions are validated or validatable
- Problem framing is correct
- Solution addresses the actual problem
- Timeline / budget realistic (within ~20% of comparable projects)
- Team has skills (or has clear acquisition plan)
- Major risks identified with mitigations
- Failure modes considered
- Trade-offs explicit; alternatives considered

### NEEDS MAJOR WORK Triggers (any 2+ true → flag)

- Timeline optimistic by 30-50%
- Budget underestimated by 30-50%
- 1-2 critical assumptions unvalidated
- Key risks unmitigated
- Team skill gaps significant but addressable
- Major alternative not considered

The foundation is sound but the gaps matter. Revise and re-validate.

### BAD Triggers (any one fatal flaw)

- **Wrong problem** — solving symptoms not root cause; success metrics misaligned with business goals
- **Invalid foundation** — core assumptions demonstrably false; tech mismatch; arch can't support requirements
- **Unrealistic execution** — timeline fantasy (>50% under); budget impossible (>50% under); team can't acquire skills
- **Anti-pattern dominance** — premature optimization, shiny object syndrome, hero culture, second system effect

### Decision Tree

```
START
  │
  ├─► Is the problem correctly framed?
  │     NO ───────────────────────────► BAD
  │     YES → continue
  │
  ├─► Are core assumptions valid?
  │     >2 invalid ─────────────────► BAD
  │     1-2 questionable → flag for NEEDS MAJOR WORK
  │     All valid → continue
  │
  ├─► Is timeline realistic?
  │     >50% under ──────────────────► BAD
  │     30-50% under → flag
  │     Within 30% → continue
  │
  ├─► Is budget realistic?
  │     >50% under ──────────────────► BAD
  │     30-50% under → flag
  │     Within 30% → continue
  │
  ├─► Can the team execute?
  │     Cannot acquire skills ──────► BAD
  │     Significant gaps → flag
  │     Capable → continue
  │
  ├─► Major anti-pattern present?
  │     Dominant ───────────────────► BAD
  │     Minor → flag
  │     None → continue
  │
  └─► Count flags
        0-1 ──────────────────────────► GOOD
        2+  ──────────────────────────► NEEDS MAJOR WORK
```

### Confidence Levels

- **High** — sufficient info, domain expertise, comparable projects, clear evidence
- **Medium** — some gaps (noted in Questions section), adjacent expertise
- **Low** — significant gaps or novel domain; recommend expert review

### Edge Cases

| Situation | Approach |
|---|---|
| Mixed signals: 1 BAD + rest GOOD | NEEDS MAJOR WORK (one fatal flaw can be addressed) |
| Mixed signals: 2+ BAD | BAD (multiple fundamental issues) |
| All borderline | NEEDS MAJOR WORK (cumulative risk) |
| >80% info | Verdict with notes |
| 50-80% info | Verdict with Low confidence |
| <50% info | Cannot validate — request more info |
| Proposal wrong scope entirely | BAD (reframe needed) |

## Report Template

```markdown
# Validation Report: [Brief Title]

**Date**: YYYY-MM-DD
**Validated By**: rnd-critic
**Subject**: [Plan / Architecture / Proposal] for [System / Feature]

---

## 1. Verdict

### VERDICT: [GOOD / NEEDS MAJOR WORK / BAD]

**Confidence**: [High / Medium / Low]

> [One-sentence summary of why this verdict.]

**Risk Profile**:
| Dimension | Rating | Notes |
|---|---|---|
| Business | Low/Med/High | … |
| Technical | Low/Med/High | … |
| Timeline | Low/Med/High | … |
| Team | Low/Med/High | … |

---

## 2. What You Got Right

### Strength 1: [Specific]
[Why this matters; what to preserve in revisions]

### Strength 2: [Specific]
[…]

---

## 3. Critical Flaws

### Flaw 1: [Title]
- **The Problem**: [Specific description]
- **Why It Matters**: [Business or technical impact, quantified if possible]
- **Consequence If Not Addressed**: [What happens at implementation]
- **Evidence**: > [Quote or data point]

### Flaw 2: [Title]
[Same format]

---

## 4. What You're Not Considering

### Hidden Assumptions
| Assumption Made | Reality Check | Risk |
|---|---|---|
| [What was assumed] | [Why it might be wrong] | [Consequence] |

### Blindspots
1. **[Title]**: [Description]
2. **[Title]**: [Description]

### Scenarios Not Explored
- **What if [scenario]?** [Why this matters]

---

## 5. The Real Question

[Use ONE format:]

**If reframe needed:**
> You're asking: "[stated question]"
> But the real question might be: "[reframed question]"
> Why this matters: [explanation]

**If problem is correctly framed:**
> The problem definition is appropriate. The proposal correctly identifies [X] and is solving the right problem.

---

## 6. What Bulletproof Looks Like

For this to be ready for implementation:

### Must-Have Criteria
- [ ] **[Criterion 1]**: [Measurable]
- [ ] **[Criterion 2]**: [Measurable]
- [ ] **[Criterion 3]**: [Measurable]

### Evidence Required
- [ ] [What proof would validate the assumptions]
- [ ] [What data would confirm the approach]

---

## 7. Recommended Path Forward

**If GOOD:**
- Minor adjustments before starting: …
- What to monitor during implementation: …
- Validation checkpoints: …

**If NEEDS MAJOR WORK:**
- Do not proceed until these are addressed:
  1. **[Area]**: [What to fix, suggested approach, who should do it]
  2. **[Area]**: […]
- Recommended workflow: revise → re-validate → proceed
- Timeline impact: [Estimate]

**If BAD:**
- Do not proceed. Fundamental rethinking required.
- Why this can't be fixed incrementally: [explanation]
- Alternative approaches:
  1. **[Alternative]**: [Brief + trade-offs]
  2. **[Alternative]**: [Brief + trade-offs]
- Recommended next steps: stakeholder discussion → reframe → restart

---

## 8. Questions You Need to Answer First

| # | Question | Who Can Answer | What It Blocks | Priority |
|---|---|---|---|---|
| 1 | [Specific question] | [Person/Team] | [Decision blocked] | Critical |
| 2 | [Specific question] | […] | […] | High |

---

## Summary

| Aspect | Assessment |
|---|---|
| **Verdict** | [GOOD / NEEDS MAJOR WORK / BAD] |
| **Confidence** | [High / Medium / Low] |
| **Critical Flaws** | [Count] |
| **Blocking Questions** | [Count] |
| **Recommendation** | [Proceed / Revise / Restart] |

**Next Steps**: [Specific action]
```

## Tone Calibration

| Verdict | Opening | Flaws | Closing |
|---|---|---|---|
| GOOD | Affirming | Advisory | Encouraging |
| NEEDS MAJOR WORK | Neutral | Direct | Constructive |
| BAD | Sympathetic | Firm | Helpful |

## Quality Checklist

Before delivering:

- [ ] Verdict is clear and justified
- [ ] Strengths are genuine (not inflated)
- [ ] Flaws are specific with evidence
- [ ] Blindspots go beyond surface issues
- [ ] Reframe is warranted (or explicitly skipped)
- [ ] Bulletproof criteria are measurable
- [ ] Path forward is actionable
- [ ] Questions are answerable and blocking
- [ ] No generic feedback — everything is specific to this proposal

## Notes

- **Skip sections that don't apply** (e.g., Reframe if problem is correct)
- **Err toward caution** — when in doubt between GOOD and NEEDS MAJOR WORK, pick NEEDS MAJOR WORK
- **BAD is not failure** — it's preventing expensive failure. Deliver with respect and provide a path forward.
- **No generic feedback** — every point must be specific to this proposal, not boilerplate.
