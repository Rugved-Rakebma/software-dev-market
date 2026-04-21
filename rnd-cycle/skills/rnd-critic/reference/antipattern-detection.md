# Anti-Pattern Detector

Identifies recurring failure patterns in technical decisions, organizational structures, and project plans.

## When to Use

- Reviewing architecture proposals
- Evaluating project plans and roadmaps
- Assessing team structures and processes
- Validating technology choices
- Checking migration strategies

## Why Anti-Patterns Matter

Anti-patterns are **proven failure modes**. They look reasonable on the surface but lead to predictable problems:

- **Technical debt accumulation**
- **Team burnout and turnover**
- **Missed deadlines and budgets**
- **System instability**
- **Organizational dysfunction**

Detecting them early saves months of pain.

---

## Anti-Pattern Categories

### 1. Architecture Anti-Patterns

Structural problems in system design.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Big Ball of Mud** | No clear architecture, everything coupled | Can't change X without breaking Y |
| **Golden Hammer** | Using one tech for everything | "We'll use Kubernetes for that too" |
| **Premature Microservices** | Splitting before understanding boundaries | 3 devs managing 20 services |
| **Distributed Monolith** | Microservices with tight coupling | Deploy all services together |
| **Resume-Driven Development** | Tech choices for career, not product | "Let's use Rust for the admin panel" |

### 2. Timeline Anti-Patterns

Planning failures that guarantee missed deadlines.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Timeline Fantasy** | Optimistic estimates ignoring reality | "6 weeks if everything goes well" |
| **Scope Creep Blindness** | Not accounting for inevitable additions | Same deadline, 2x features |
| **Parallel Path Delusion** | Assuming unlimited parallelization | "Add more devs to go faster" |
| **MVP Maximalism** | MVP that's actually V3 | 47 features in "minimum" product |
| **Demo-Driven Development** | Building for demos, not production | "It works on my machine" |

### 3. Team Anti-Patterns

Organizational structures that create dysfunction.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Hero Culture** | Reliance on key individuals | "Only Sarah can fix that" |
| **Knowledge Silos** | Critical info in one person's head | Bus factor of 1 |
| **Conway's Law Violation** | Architecture doesn't match team structure | Team boundaries ≠ service boundaries |
| **Understaffed Ambition** | Big plans with tiny teams | 2 devs building "the platform" |
| **Absent Ownership** | No clear owner for components | Bugs fall through cracks |

### 4. Process Anti-Patterns

Workflow failures that slow delivery.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Cargo Cult Agile** | Agile ceremonies without principles | Standups but no shipping |
| **Analysis Paralysis** | Over-planning, under-executing | Month 3 of "finalizing requirements" |
| **Infinite Refactoring** | Never shipping, always "improving" | "One more cleanup before release" |
| **Documentation Theater** | Docs that no one reads or maintains | 200-page spec, outdated day 1 |
| **Meeting Madness** | More meetings than coding time | "Let's schedule a meeting to discuss" |

### 5. Technology Anti-Patterns

Poor technology decisions.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Shiny Object Syndrome** | Chasing latest tech without reason | "We should rewrite in [new thing]" |
| **Not Invented Here** | Building what should be bought | Custom auth, custom logging, custom everything |
| **Vendor Lock-in Denial** | Ignoring exit costs | "We can always migrate later" |
| **Premature Optimization** | Optimizing before measuring | Caching layer with 10 users |
| **Framework Overload** | Too many frameworks/libraries | 47 npm dependencies for a button |

---

## Detection Process

### Step 1: Scan for Signals

Look for these phrases that often indicate anti-patterns:

**Timeline signals**:
- "If everything goes well..."
- "We can do it faster if we're focused..."
- "Just need to hire..."
- "Should only take..."

**Architecture signals**:
- "We'll figure out the boundaries later..."
- "Everything talks to everything..."
- "It's only for now..."
- "We can always refactor..."

**Team signals**:
- "Only [person] knows..."
- "We'll hire for that..."
- "[Person] will handle all of..."
- "The team can absorb..."

**Process signals**:
- "We don't need docs for this..."
- "We'll add tests later..."
- "Let's discuss in the meeting..."
- "Requirements are still evolving..."

### Step 2: Verify Pattern Match

For each suspected anti-pattern:

1. **Identify the pattern**: Which specific anti-pattern?
2. **Gather evidence**: What in the proposal matches?
3. **Assess severity**: How bad is it? (Critical/High/Medium/Low)
4. **Check context**: Could this be a reasonable exception?

### Step 3: Document Findings

```markdown
### Anti-Pattern: [Name]

**Category**: Architecture / Timeline / Team / Process / Technology
**Severity**: Critical / High / Medium / Low

**Evidence**:
- [Quote or observation 1]
- [Quote or observation 2]

**Why This Is a Problem**:
[Explain the typical failure mode]

**Historical Examples**:
[Reference similar failures if known]

**Recommendation**:
[Specific action to address]
```

---

## Severity Framework

### Critical
Will cause project failure if not addressed.
- **Examples**: No clear ownership, timeline fantasy for commitments, hero dependency
- **Action**: Stop and address before proceeding

### High
Will cause significant problems.
- **Examples**: Premature microservices, understaffed plans, shiny object syndrome
- **Action**: Address in planning phase

### Medium
Will cause friction and delays.
- **Examples**: Documentation gaps, process inefficiencies, minor scope creep
- **Action**: Include in risk mitigation

### Low
Worth noting but manageable.
- **Examples**: Style inconsistencies, minor tech debt, preference-based choices
- **Action**: Track and address opportunistically

---

## Output Format

```markdown
# Anti-Pattern Analysis: [Plan/Proposal Name]

## Summary
- **Patterns Detected**: [Count]
- **Critical Issues**: [Count]
- **Overall Risk Level**: Critical / High / Medium / Low

## Critical Issues (Must Address)

### 1. [Pattern Name]
**Category**: [Category]
**Evidence**: [What triggered this detection]
**Risk**: [What will go wrong]
**Fix**: [How to address]

---

## High-Priority Issues (Should Address)

### 2. [Pattern Name]
[Same format]

---

## Medium-Priority Issues (Consider Addressing)

### 3. [Pattern Name]
[Same format]

---

## Patterns NOT Detected
[List patterns that were checked but not found - provides confidence]

## Recommendations

### Before Proceeding
1. [Critical action 1]
2. [Critical action 2]

### During Execution
1. [Mitigation 1]
2. [Mitigation 2]

### Monitoring
- [Warning sign to watch for]
- [Metric to track]
```

---

## Common Pattern Combinations

Certain anti-patterns tend to appear together:

### The Startup Death Spiral
- Timeline Fantasy + Understaffed Ambition + Hero Culture
- Result: Burnout, missed deadlines, key person leaves

### The Enterprise Trap
- Analysis Paralysis + Documentation Theater + Meeting Madness
- Result: Nothing ships, team frustrated, competition wins

### The Tech Debt Avalanche
- "We'll refactor later" + No clear ownership + Premature optimization
- Result: System becomes unmaintainable, rewrite required

### The Microservices Mistake
- Premature Microservices + Distributed Monolith + Not enough DevOps
- Result: Complexity explosion, slower delivery than monolith

---

## Integration with Validation

The antipattern-detector feeds into the broader validation workflow:

```
Proposal/Plan
     │
     ▼
[assumption-challenging] → Assumptions identified
     │
     ▼
[antipattern-detection] → Patterns identified
     │
     ▼
[validation-reports] → Combined 8-section report
```

---

## Anti-Pattern Catalog

Detailed examples and remediation for each anti-pattern.

---

### Architecture Anti-Patterns

#### Big Ball of Mud

**What It Looks Like**:
```
┌─────────────────────────────────────┐
│  Everything calls everything else   │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐    │
│  │ A ├─┤ B ├─┤ C ├─┤ D ├─┤ E │    │
│  └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘    │
│    │     │     │     │     │       │
│    └─────┴─────┴─────┴─────┘       │
│         (all interconnected)        │
└─────────────────────────────────────┘
```

**Red Flags**:
- "We need to deploy everything together"
- "Changing the user model breaks notifications"
- "I'm not sure where this logic should go"
- Circular dependencies between modules
- 1000+ line files with mixed concerns

**Consequences**:
- Changes are risky and time-consuming
- Testing requires full system
- New developers take months to onboard
- Bugs cascade unpredictably

**Remediation**:
1. Draw actual dependency graph
2. Identify natural boundaries
3. Gradually extract modules with clear interfaces
4. Add integration tests at boundaries

---

#### Golden Hammer

**What It Looks Like**:
- "We'll use Kubernetes for the static website"
- "PostgreSQL for the cache, PostgreSQL for the queue, PostgreSQL for everything"
- "React for the CLI tool"

**Red Flags**:
- Same technology for very different use cases
- Team only knows one stack
- Resistance to considering alternatives
- Justifications like "we already know it"

**Consequences**:
- Square peg, round hole implementations
- Unnecessary complexity
- Performance issues from wrong tool
- Team skill stagnation

**Remediation**:
1. Evaluate each problem independently
2. Create decision criteria matrix
3. Accept some technology diversity is healthy
4. Budget time for learning appropriate tools

---

#### Premature Microservices

**What It Looks Like**:
```
Team size: 4 developers
Services: 15+ microservices
Result: Each dev responsible for 4 services
```

**Red Flags**:
- Starting with microservices for a new product
- More services than team members
- "We need to be ready to scale"
- No clear service boundaries, just "small services"

**Consequences**:
- Massive operational overhead
- Distributed system complexity (network failures, consistency)
- Slower development than monolith would be
- Deployment complexity

**Remediation**:
1. Merge back to modular monolith
2. Only split when you have clear bounded contexts
3. Rule of thumb: 1 service per 2-3 developers minimum
4. Split based on team boundaries, not technical layers

---

#### Distributed Monolith

**What It Looks Like**:
```
"Microservices" that must be:
- Deployed together
- Versioned together
- Tested together
- Released together
```

**Red Flags**:
- Shared database between services
- Synchronous calls everywhere
- Breaking changes require coordinated deploys
- "We need to update all services for this change"

**Consequences**:
- All downsides of microservices (complexity, network)
- None of the benefits (independent deployment, scaling)
- Worse than a monolith

**Remediation**:
1. Acknowledge you have a distributed monolith
2. Either: separate properly OR merge back
3. Define clear API contracts
4. Move to async communication where possible

---

#### Resume-Driven Development

**What It Looks Like**:
- "Let's rewrite in Rust" (for a CRUD app)
- "We should use GraphQL" (for 2 API endpoints)
- "Kubernetes would be perfect" (for a single container)

**Red Flags**:
- Technology choice can't be justified by requirements
- Justification focuses on "learning" not "solving"
- CV-worthy tech for boring problems
- Senior devs pushing tech they want experience in

**Consequences**:
- Wrong tool for the job
- Extended timeline for learning curve
- Team may not maintain after advocate leaves
- Technical debt from inexperience

**Remediation**:
1. Require explicit problem-solution mapping
2. Ask "what would we use if resumes didn't exist?"
3. Separate exploration projects from production
4. Budget for learning in side projects

---

### Timeline Anti-Patterns

#### Timeline Fantasy

**What It Looks Like**:
```
Estimate: "6 weeks"
Basis: "Feels about right"
Buffer: 0%
Risks considered: 0
```

**Red Flags**:
- "If everything goes well"
- No comparison to past projects
- No buffer for unknowns
- Estimate unchanged despite scope growth

**Consequences**:
- Missed deadlines (100% certain)
- Crunch time and burnout
- Quality sacrificed
- Trust erosion

**Remediation**:
1. Compare to actual past durations
2. Add 30-50% buffer for unknowns
3. Use three-point estimation (optimistic, realistic, pessimistic)
4. Track actuals vs estimates to improve

---

#### Scope Creep Blindness

**What It Looks Like**:
```
Week 1: "Build user auth"
Week 2: "...and SSO"
Week 3: "...and 2FA"
Week 4: "...and admin impersonation"
Week 5: "Why aren't we done yet?"
```

**Red Flags**:
- "While we're at it..."
- "It's just a small addition"
- Deadline stays fixed as scope grows
- No formal change process

**Consequences**:
- Deadline impossible to meet
- Team demoralized
- Quality suffers
- Original scope not delivered

**Remediation**:
1. Document original scope clearly
2. Every addition requires trade-off discussion
3. Re-estimate when scope changes
4. Make scope changes visible to stakeholders

---

#### MVP Maximalism

**What It Looks Like**:
```
"MVP" feature list:
- Core functionality ✓
- Admin dashboard
- Analytics
- Multi-tenant support
- API for partners
- White-labeling
- 3 language support
- Mobile apps
```

**Red Flags**:
- MVP takes 6+ months
- "We can't launch without [nice-to-have]"
- Features that don't validate core hypothesis
- Enterprise features in v0.1

**Consequences**:
- Never launches
- Builds wrong thing for too long
- Burns runway before validation
- Team exhausted before real feedback

**Remediation**:
1. Define what hypothesis you're testing
2. Minimum = smallest thing to test hypothesis
3. Everything else is v2
4. Set hard deadline and cut ruthlessly

---

### Team Anti-Patterns

#### Hero Culture

**What It Looks Like**:
```
Org chart says: 5 engineers
Reality: 1 engineer who matters + 4 others
```

**Red Flags**:
- "Only [person] can fix that"
- One person in every critical meeting
- Others defer instead of learning
- Hero works nights/weekends

**Consequences**:
- Single point of failure (human)
- Hero burns out or leaves
- Others don't grow
- Resentment builds

**Remediation**:
1. Document what hero knows
2. Pair hero with others on critical systems
3. Rotate ownership deliberately
4. Celebrate team wins, not hero saves

---

#### Knowledge Silos

**What It Looks Like**:
```
"How does billing work?"
"Ask Sarah"

"How do we deploy?"
"Ask Marcus"

"What's the database schema?"
"That's in Tom's head"
```

**Red Flags**:
- Questions always go to same person
- No documentation for critical systems
- Bus factor of 1
- "Tribal knowledge"

**Consequences**:
- Single points of failure
- Slow onboarding
- Key person leaving is catastrophic
- Bottlenecks on individuals

**Remediation**:
1. Document as you go
2. Rotate on-call and support
3. Pair programming on critical systems
4. Record architecture decisions

---

#### Understaffed Ambition

**What It Looks Like**:
```
Plan: "Build the platform"
Team: 2 engineers
Timeline: "Q3"
Reality: Needs 8 engineers for 18 months
```

**Red Flags**:
- "Small but mighty team"
- Comparing to well-funded competitors
- Plans assume 100% productivity
- "We'll hire as we grow"

**Consequences**:
- Burnout guaranteed
- Corners cut everywhere
- Technical debt explosion
- Missed deadlines

**Remediation**:
1. Right-size scope to team
2. Sequence instead of parallelize
3. Have hiring complete before plan starts
4. Build less, but build it well

---

### Process Anti-Patterns

#### Cargo Cult Agile

**What It Looks Like**:
```
Has: Daily standups, sprints, story points
Missing: Working software, customer feedback, adaptation
```

**Red Flags**:
- Ceremonies without outcomes
- Sprint planning but no sprint goals
- Retrospectives with no changes
- Story points without velocity tracking

**Consequences**:
- Process overhead without benefits
- Team cynicism about "agile"
- Predictability still poor
- Customer needs ignored

**Remediation**:
1. Start with outcomes, not ceremonies
2. Measure working software delivered
3. Actually change based on retros
4. Talk to customers regularly

---

#### Analysis Paralysis

**What It Looks Like**:
```
Month 1: Requirements gathering
Month 2: Requirements review
Month 3: Architecture discussions
Month 4: More requirements
Month 5: "We need more stakeholder input"
Month 6: Still no code
```

**Red Flags**:
- Requirements doc over 50 pages
- Multiple architecture reviews
- "We need to think about this more"
- Perfect is enemy of good

**Consequences**:
- Nothing ships
- Market moves on
- Team loses momentum
- Stakeholders lose confidence

**Remediation**:
1. Set hard deadline for first delivery
2. Limit planning phase explicitly
3. Accept iteration beats perfection
4. Build to learn, not learn to build

---

### Technology Anti-Patterns

#### Shiny Object Syndrome

**What It Looks Like**:
```
2023: "We should use [Framework X]"
2024: "We should use [Framework Y]"
2025: "We should use [Framework Z]"
(Original project still on Framework W)
```

**Red Flags**:
- New tech proposed every quarter
- "This would solve our problems"
- Grass is greener mentality
- Ignoring switching costs

**Consequences**:
- Constant context switching
- Nothing gets deep investment
- Technical debt from half-migrations
- Team churn from instability

**Remediation**:
1. Define adoption criteria upfront
2. Require proof-of-concept before proposal
3. Calculate total cost of switching
4. Commit to choices for defined period

---

#### Not Invented Here

**What It Looks Like**:
```
Custom built:
- Logging framework
- Authentication system
- Job queue
- ORM
- Testing framework
- Deployment system
```

**Red Flags**:
- "We can build it better"
- Custom solutions for solved problems
- Maintenance burden ignored
- Team proud of infrastructure

**Consequences**:
- Maintaining commodities instead of differentiators
- Security vulnerabilities from non-expert implementations
- Documentation and support burden
- Hiring harder (custom stack)

**Remediation**:
1. Only build what differentiates
2. Calculate true cost (build + maintain + document + support)
3. Use off-the-shelf for commodities
4. Focus engineering on business value

---

#### Vendor Lock-in Denial

**What It Looks Like**:
```
"We can always migrate later"
(3 years later)
"Migration would take 18 months and $2M"
```

**Red Flags**:
- Deep integration with single vendor
- Proprietary APIs used extensively
- No abstraction layer
- Switching costs never calculated

**Consequences**:
- Pricing leverage lost
- Feature roadmap dependency
- Migration costs compound over time
- Vendor changes break everything

**Remediation**:
1. Calculate exit costs before commitment
2. Abstract vendor-specific code
3. Use open standards where possible
4. Maintain backup vendor relationship

---

## Quick Reference Card

### Immediate Red Flags
- [ ] "Only [person] knows..."
- [ ] "If everything goes well..."
- [ ] "We'll figure it out later..."
- [ ] "We need to hire..."
- [ ] "It's just a small addition..."
- [ ] "We can always migrate..."
- [ ] "Let's use [new tech] because..."

### Questions to Ask
1. What happens if the key person leaves?
2. What's this estimate based on?
3. What's the Plan B?
4. What similar things have we done? How long did they take?
5. What's the switching cost?
6. Who owns this?
7. Where is this documented?

### Pattern → Severity Quick Guide

| If you see... | It's probably... | Severity |
|---------------|------------------|----------|
| Single point of human failure | Hero Culture | Critical |
| Optimistic estimate, no buffer | Timeline Fantasy | Critical |
| More services than devs | Premature Microservices | High |
| Custom auth, logging, etc. | Not Invented Here | High |
| MVP with 20+ features | MVP Maximalism | High |
| "Agile" but nothing ships | Cargo Cult Agile | Medium |
| Latest framework every year | Shiny Object Syndrome | Medium |
