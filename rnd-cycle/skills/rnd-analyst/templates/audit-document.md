# Document Audit Report

**Analysis Date:** [YYYY-MM-DD]

## Document Summary

**Document analyzed:** [Title or file path of the document]
**Type:** [Spec / PRD / Proposal / Design Document / Architecture Document]
**Scope:** [What the document covers]
**Calibration tier:** [full_maturity / standard / minimal_decisive]

## Gaps

Missing requirements, unaddressed scenarios, and undefined interfaces.

### Missing Requirements

**[Gap title]:**
- What is missing: [Description of the missing requirement]
- Why it matters: [What breaks or is undefined without it]
- Section affected: [Which part of the document should address this]

### Unaddressed Scenarios

**[Scenario]:**
- Description: [Edge case, error state, or user path not covered]
- Likelihood: [How often this scenario occurs in practice]
- Impact if unaddressed: [What happens when this scenario is hit]

### Undefined Interfaces

**[Interface]:**
- What is undefined: [API contract, data format, integration point]
- What depends on it: [What cannot be built without this definition]

## Assumptions

Stated and implied assumptions with confidence classification.

### [Area Name]

- **Assumption:** [Decision statement]
  - **Evidence:** [What supports this — cite document sections or file paths]
  - **If Wrong:** [Concrete consequence]
  - **Confidence:** Confident | Likely | Unclear

[Repeat for each assumption area — number based on calibration tier]

## Risks

Technical, business, and timeline risks.

### [Risk Title]

- **Category:** Technical | Business | Timeline | Resource | External
- **Description:** [What could go wrong]
- **Likelihood:** High (>70%) | Medium (30-70%) | Low (<30%)
- **Impact:** Critical (blocks launch) | High (significant rework) | Medium (delays) | Low (minor adjustment)
- **Mitigation:** [What can reduce likelihood or impact]
- **Owner:** [Who should track this risk]

## Ambiguities

Statements that could be interpreted multiple ways.

### [Ambiguous Statement]

- **Document section:** [Where this appears]
- **Interpretation A:** [One way to read it]
- **Interpretation B:** [Another way to read it]
- **Impact of misinterpretation:** [What goes wrong if the wrong interpretation is chosen]
- **Recommendation:** [How to clarify — specific question to answer]

## Implementability Assessment

Can this be built with the stated constraints?

### Timeline Feasibility
- **Assessment:** Feasible | Tight | Unrealistic
- **Reasoning:** [Why this timeline does or does not work]
- **Key risks:** [What could extend the timeline]

### Skill Requirements
- **Assessment:** Covered | Gaps Exist | Significant Gaps
- **Reasoning:** [What skills are needed vs available]
- **Missing skills:** [Specific expertise not on team]

### Dependency Risks
- **External dependencies:** [Third-party services, APIs, or tools required]
- **Availability:** [Are they available, reliable, affordable?]
- **Lock-in risk:** [How hard to switch if dependency fails]

### Technical Feasibility
- **Assessment:** Feasible | Challenging | Infeasible
- **Hard problems:** [Technically difficult requirements]
- **Unknown unknowns:** [Areas where feasibility cannot be assessed without research]

### Resource Constraints
- **Budget alignment:** [Does scope match budget?]
- **Infrastructure needs:** [What infrastructure is required?]
- **Operational burden:** [What ongoing costs and maintenance does this create?]

## Recommendations

Specific actions to improve the document before implementation.

### Must Clarify
Items that MUST be resolved before implementation can begin:
1. [Item — what needs clarification and who can provide it]

### Should Research
Items that need investigation but do not block starting:
1. [Item — what to research and expected timeline]

### Should Add
Missing sections or requirements to add to the document:
1. [Item — what to add and where in the document]

### Consider Revising
Existing content that should be reworked:
1. [Item — what to change and why]

---
*Document audit: [date]*
