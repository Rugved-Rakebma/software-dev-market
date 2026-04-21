# Architecture Pattern Selector

Provides systematic framework for selecting the right architecture pattern based on real-world constraints rather than hype or resume-driven development.

## When to Use

- Designing a new system from scratch
- Evaluating whether to migrate from monolith to microservices
- Choosing between serverless vs container-based architecture
- Assessing if current architecture matches actual needs

## Architecture Patterns

### 1. Monolith
**Best for**: Early-stage products, small teams, rapid iteration

**Characteristics**:
- Single deployable unit
- Shared database
- Simple deployment and debugging
- Fastest time to market

**Choose when**:
- Team < 10 engineers
- < 100K users
- Product-market fit not yet proven
- Need to iterate quickly on features
- Limited DevOps expertise

**Avoid when**:
- Different components need independent scaling
- Multiple teams need to deploy independently
- Parts of system have very different reliability requirements

### 2. Modular Monolith
**Best for**: Growing products that need structure without microservices complexity

**Characteristics**:
- Single deployable unit with clear module boundaries
- Modules communicate through defined interfaces
- Can evolve to microservices later
- Best of both worlds for mid-size teams

**Choose when**:
- Team 10-30 engineers
- 100K-1M users
- Need better code organization
- Want microservices benefits without operational overhead
- Planning future extraction to services

**Avoid when**:
- Need independent deployment per module
- Modules have fundamentally different scaling requirements
- Already have microservices expertise and infrastructure

### 3. Microservices
**Best for**: Large organizations with mature DevOps practices

**Characteristics**:
- Independent deployable services
- Service-specific databases
- Complex operational requirements
- High organizational overhead

**Choose when**:
- Team > 30 engineers with multiple squads
- > 1M users with varying load patterns
- Different services need different scaling strategies
- Strong DevOps/Platform team
- Clear bounded contexts

**Avoid when**:
- Team lacks Kubernetes/container orchestration experience
- No dedicated platform/DevOps team
- Bounded contexts are unclear
- Chasing microservices for resume value

### 4. Serverless
**Best for**: Event-driven workloads, variable traffic, cost optimization

**Characteristics**:
- Pay-per-execution pricing
- Auto-scaling to zero
- Vendor lock-in concerns
- Cold start latency

**Choose when**:
- Highly variable or spiky traffic
- Event-driven processing (webhooks, queues)
- Cost-sensitive with unpredictable load
- Simple request-response patterns
- Limited DevOps capacity

**Avoid when**:
- Consistent high-volume traffic (cost inefficient)
- Low-latency requirements (< 100ms consistently)
- Long-running processes
- Complex stateful workflows

### 5. Hybrid
**Best for**: Complex systems with varied requirements

**Characteristics**:
- Mix of patterns for different components
- Monolith core with serverless functions
- Microservices for specific bounded contexts

**Choose when**:
- Different parts of system have different characteristics
- Migrating incrementally from monolith
- Some components need independent scaling
- Event-driven workflows alongside synchronous APIs

---

## Selection Framework

### Step 1: Assess Current State

```
Team Size:        [ ] < 10   [ ] 10-30   [ ] 30-100   [ ] > 100
User Scale:       [ ] < 100K [ ] 100K-1M [ ] 1M-10M   [ ] > 10M
DevOps Maturity:  [ ] None   [ ] Basic   [ ] Intermediate [ ] Advanced
Deployment Freq:  [ ] Monthly [ ] Weekly [ ] Daily    [ ] Multiple/day
```

### Step 2: Evaluate Constraints

| Constraint | Impact on Pattern Choice |
|------------|-------------------------|
| Time to market | Favors monolith |
| Team autonomy | Favors microservices |
| Cost sensitivity | Favors serverless or monolith |
| Latency requirements | Disfavors serverless |
| Compliance/security | May require isolation (microservices) |

### Step 3: Apply Decision Matrix

See the Decision Matrix section below for the scoring framework.

### Step 4: Consider Migration Path

Every architecture should have a migration path:
- Monolith → Modular Monolith → Microservices
- Monolith → Hybrid (extract specific services)
- Serverless → Containers (when scale justifies)

---

## Output Format

When recommending an architecture pattern, provide:

```markdown
## Architecture Recommendation

### Recommended Pattern: [Pattern Name]
**Confidence**: High / Medium / Low

### Why This Pattern
[2-3 specific reasons based on constraints]

### Trade-offs Accepted
- [Trade-off 1 and why it's acceptable]
- [Trade-off 2 and why it's acceptable]

### Migration Path
- **Current**: [Current state]
- **Phase 1**: [Near-term architecture]
- **Phase 2**: [If/when to evolve]
- **Trigger**: [What would cause migration to next phase]

### Patterns Rejected
| Pattern | Reason Not Selected |
|---------|---------------------|
| [Pattern] | [Specific reason] |

### Implementation Considerations
- [Key consideration 1]
- [Key consideration 2]
- [Key consideration 3]
```

---

## Anti-Patterns to Avoid

### Resume-Driven Architecture
Choosing microservices because it looks good on resumes, not because the problem requires it.

**Red flag**: "We should use microservices because that's what Netflix uses."
**Reality check**: You're not Netflix. What's your actual scale and team size?

### Premature Distribution
Distributing a system before understanding the domain boundaries.

**Red flag**: "Let's start with microservices from day one."
**Reality check**: You'll draw the wrong boundaries. Start monolith, extract when clear.

### Complexity Worship
Equating complexity with sophistication.

**Red flag**: "Our architecture needs to be enterprise-grade."
**Reality check**: Simple architectures that work beat complex ones that don't.

---

## Decision Matrix

Scoring framework for selecting the right architecture pattern.

### How to Use

1. Score each factor (1-5) based on your situation
2. Multiply by weight
3. Sum scores for each pattern
4. Highest score = recommended pattern

### Scoring Factors

#### Factor 1: Team Size (Weight: 3)

| Team Size | Monolith | Modular Monolith | Microservices | Serverless |
|-----------|----------|------------------|---------------|------------|
| < 5 engineers | 5 | 3 | 1 | 4 |
| 5-15 engineers | 4 | 5 | 2 | 3 |
| 15-50 engineers | 2 | 4 | 4 | 3 |
| > 50 engineers | 1 | 3 | 5 | 2 |

#### Factor 2: Expected Scale (Weight: 3)

| Scale | Monolith | Modular Monolith | Microservices | Serverless |
|-------|----------|------------------|---------------|------------|
| < 10K users | 5 | 4 | 1 | 4 |
| 10K-100K users | 4 | 5 | 2 | 4 |
| 100K-1M users | 3 | 4 | 4 | 3 |
| 1M-10M users | 2 | 3 | 5 | 3 |
| > 10M users | 1 | 2 | 5 | 2 |

#### Factor 3: DevOps Maturity (Weight: 4)

| Maturity | Monolith | Modular Monolith | Microservices | Serverless |
|----------|----------|------------------|---------------|------------|
| None (manual deploys) | 5 | 3 | 1 | 3 |
| Basic (CI/CD) | 4 | 4 | 2 | 4 |
| Intermediate (containers) | 3 | 5 | 3 | 4 |
| Advanced (K8s, service mesh) | 2 | 4 | 5 | 3 |

#### Factor 4: Time to Market Pressure (Weight: 3)

| Pressure | Monolith | Modular Monolith | Microservices | Serverless |
|----------|----------|------------------|---------------|------------|
| Critical (< 3 months) | 5 | 3 | 1 | 4 |
| High (3-6 months) | 4 | 4 | 2 | 4 |
| Medium (6-12 months) | 3 | 5 | 4 | 3 |
| Low (> 12 months) | 2 | 4 | 5 | 3 |

#### Factor 5: Traffic Pattern (Weight: 2)

| Pattern | Monolith | Modular Monolith | Microservices | Serverless |
|---------|----------|------------------|---------------|------------|
| Steady/predictable | 4 | 4 | 3 | 2 |
| Moderate spikes (2-3x) | 3 | 4 | 4 | 4 |
| High spikes (10x+) | 2 | 3 | 4 | 5 |
| Unpredictable/event-driven | 2 | 3 | 3 | 5 |

#### Factor 6: Latency Requirements (Weight: 2)

| Requirement | Monolith | Modular Monolith | Microservices | Serverless |
|-------------|----------|------------------|---------------|------------|
| Real-time (< 50ms) | 4 | 4 | 3 | 1 |
| Interactive (< 200ms) | 4 | 4 | 4 | 3 |
| Standard (< 1s) | 4 | 4 | 4 | 4 |
| Tolerant (> 1s ok) | 4 | 4 | 4 | 5 |

#### Factor 7: Domain Clarity (Weight: 3)

| Clarity | Monolith | Modular Monolith | Microservices | Serverless |
|---------|----------|------------------|---------------|------------|
| Unclear/evolving | 5 | 4 | 1 | 3 |
| Partially defined | 4 | 5 | 2 | 3 |
| Well-defined | 3 | 4 | 4 | 4 |
| Crystal clear bounded contexts | 2 | 3 | 5 | 4 |

#### Factor 8: Budget Constraints (Weight: 2)

| Budget | Monolith | Modular Monolith | Microservices | Serverless |
|--------|----------|------------------|---------------|------------|
| Very tight | 5 | 4 | 1 | 4 |
| Limited | 4 | 4 | 2 | 4 |
| Moderate | 3 | 4 | 4 | 4 |
| Generous | 3 | 4 | 5 | 3 |

---

### Score Calculation Example

**Scenario**: Series A startup, 12 engineers, targeting 500K users in 12 months, basic DevOps, need to ship MVP in 4 months.

| Factor | Weight | Monolith | Mod. Mono | Microservices | Serverless |
|--------|--------|----------|-----------|---------------|------------|
| Team Size (12) | 3 | 4x3=12 | 5x3=15 | 2x3=6 | 3x3=9 |
| Scale (500K) | 3 | 3x3=9 | 4x3=12 | 4x3=12 | 3x3=9 |
| DevOps (Basic) | 4 | 4x4=16 | 4x4=16 | 2x4=8 | 4x4=16 |
| Time (4 mo) | 3 | 5x3=15 | 3x3=9 | 1x3=3 | 4x3=12 |
| Traffic (Mod.) | 2 | 3x2=6 | 4x2=8 | 4x2=8 | 4x2=8 |
| Latency (Std) | 2 | 4x2=8 | 4x2=8 | 4x2=8 | 4x2=8 |
| Domain (Partial) | 3 | 4x3=12 | 5x3=15 | 2x3=6 | 3x3=9 |
| Budget (Limited) | 2 | 4x2=8 | 4x2=8 | 2x2=4 | 4x2=8 |
| **TOTAL** | | **86** | **91** | **55** | **79** |

**Recommendation**: Modular Monolith (highest score: 91)

---

### Quick Decision Guide

#### Choose Monolith If:
- Score > 80 AND team < 10 AND time critical

#### Choose Modular Monolith If:
- Highest score AND team 10-30 AND moderate time pressure

#### Choose Microservices If:
- Score > 75 AND team > 30 AND DevOps advanced AND domains clear

#### Choose Serverless If:
- Score > 75 AND traffic spiky AND latency tolerant AND event-driven

#### Choose Hybrid If:
- No pattern scores > 75 AND different components have different needs

---

### Override Conditions

Regardless of scores, certain conditions override the matrix:

#### Force Monolith
- Team < 5 engineers (complexity will overwhelm)
- No product-market fit yet (need iteration speed)
- < 3 month deadline (no time for distributed systems)

#### Force Microservices
- Regulatory requirement for isolation
- Acquisitions requiring integration of disparate systems
- Team > 100 with clear bounded contexts

#### Force Serverless
- Extremely variable load (10x+ spikes regularly)
- Event processing workloads
- Strict budget constraints with unpredictable usage

---

### Scoring Template

Copy and fill in for your project:

```markdown
## Architecture Pattern Score

**Project**: [Name]
**Date**: [Date]

| Factor | Weight | Score | Reasoning |
|--------|--------|-------|-----------|
| Team Size | 3 | | |
| Expected Scale | 3 | | |
| DevOps Maturity | 4 | | |
| Time to Market | 3 | | |
| Traffic Pattern | 2 | | |
| Latency Req | 2 | | |
| Domain Clarity | 3 | | |
| Budget | 2 | | |

**Total Scores**:
- Monolith:
- Modular Monolith:
- Microservices:
- Serverless:

**Recommended Pattern**:
**Override Conditions**: [None / If applicable]
```

---

## Pattern Comparison

Side-by-side comparison of architecture patterns across key dimensions.

### Overview Comparison

| Aspect | Monolith | Modular Monolith | Microservices | Serverless |
|--------|----------|------------------|---------------|------------|
| **Deployment** | Single unit | Single unit | Multiple units | Functions |
| **Database** | Shared | Shared (module schemas) | Per-service | Per-function or shared |
| **Scaling** | Vertical + horizontal | Vertical + horizontal | Per-service | Auto per-function |
| **Team Structure** | Any | Feature teams | Service teams | Function owners |
| **Complexity** | Low | Medium | High | Medium-High |
| **Initial Cost** | Low | Low-Medium | High | Low |
| **Operational Cost** | Medium | Medium | High | Variable |

### Development Experience

| Aspect | Monolith | Modular Monolith | Microservices | Serverless |
|--------|----------|------------------|---------------|------------|
| Local development | Easy | Easy | Complex | Medium |
| Debugging | Easy | Easy | Hard | Hard |
| Testing | Easy | Medium | Complex | Medium |
| Onboarding new devs | Fast | Fast | Slow | Medium |
| IDE support | Excellent | Excellent | Fragmented | Good |
| Refactoring | Easy | Medium | Hard | Medium |

### Operational Characteristics

| Aspect | Monolith | Modular Monolith | Microservices | Serverless |
|--------|----------|------------------|---------------|------------|
| Deployment frequency | Limited by size | Limited by size | Per-service | Per-function |
| Rollback | All or nothing | All or nothing | Per-service | Per-function |
| Monitoring | Simple | Simple | Complex | Complex |
| Distributed tracing | Not needed | Not needed | Essential | Essential |
| Service discovery | Not needed | Not needed | Required | Managed |
| Load balancing | Simple | Simple | Complex | Managed |

### Scaling Characteristics

| Aspect | Monolith | Modular Monolith | Microservices | Serverless |
|--------|----------|------------------|---------------|------------|
| Scale granularity | Entire app | Entire app | Per-service | Per-function |
| Scale speed | Medium | Medium | Fast | Instant |
| Scale to zero | No | No | Possible | Yes |
| Cost at low scale | Fixed | Fixed | Fixed (higher) | Near-zero |
| Cost at high scale | Efficient | Efficient | Variable | Can be high |

### Reliability Characteristics

| Aspect | Monolith | Modular Monolith | Microservices | Serverless |
|--------|----------|------------------|---------------|------------|
| Failure blast radius | Entire app | Entire app | Per-service | Per-function |
| Partial degradation | Hard | Hard | Built-in | Built-in |
| Data consistency | Easy (ACID) | Easy (ACID) | Complex (eventual) | Complex |
| Network failures | Not an issue | Not an issue | Major concern | Major concern |

### Cost Analysis

#### Development Costs

| Pattern | Initial Build | Feature Development | Maintenance |
|---------|---------------|---------------------|-------------|
| Monolith | $ | $ | $ |
| Modular Monolith | $$ | $ | $$ |
| Microservices | $$$$ | $$ | $$$$ |
| Serverless | $$ | $$ | $$ |

#### Infrastructure Costs (at different scales)

| Pattern | 10K users/mo | 100K users/mo | 1M users/mo | 10M users/mo |
|---------|--------------|---------------|-------------|--------------|
| Monolith | $50-200 | $200-500 | $500-2K | $2K-10K |
| Modular Monolith | $50-200 | $200-500 | $500-2K | $2K-10K |
| Microservices | $200-500 | $500-2K | $2K-10K | $10K-50K |
| Serverless | $10-50 | $50-500 | $500-5K | $5K-50K |

*Note: Costs are illustrative. Actual costs depend heavily on workload characteristics.*

#### Hidden Costs

| Pattern | Hidden Costs |
|---------|-------------|
| Monolith | Technical debt accumulation, scaling ceiling |
| Modular Monolith | Discipline required to maintain boundaries |
| Microservices | Platform team, tooling, training, debugging time |
| Serverless | Cold starts, vendor lock-in, debugging complexity |

### Team Requirements

#### Minimum Team for Effective Operation

| Pattern | Min Engineers | Required Roles |
|---------|---------------|----------------|
| Monolith | 1 | Full-stack developer |
| Modular Monolith | 3 | Full-stack developers with architecture awareness |
| Microservices | 15+ | Platform team (2-3), service teams, SRE |
| Serverless | 2 | Cloud-native developers |

#### Skills Required

| Pattern | Essential Skills |
|---------|-----------------|
| Monolith | Language/framework, SQL, basic deployment |
| Modular Monolith | Above + DDD, module design, interface design |
| Microservices | Above + containers, K8s, service mesh, distributed systems |
| Serverless | Cloud provider, event-driven design, IAM, monitoring |

### Migration Paths

#### From Monolith

```
Monolith
    │
    ├──► Modular Monolith (lowest risk)
    │         │
    │         └──► Microservices (when ready)
    │
    ├──► Hybrid (extract specific services)
    │
    └──► Serverless (for specific workloads)
```

#### Migration Triggers

| From | To | Trigger |
|------|-----|---------|
| Monolith | Modular Monolith | Team growing, code getting tangled |
| Modular Monolith | Microservices | Modules need independent scaling/deployment |
| Any | Serverless | Event-driven workloads, cost optimization |
| Microservices | Modular Monolith | Over-distributed, too much overhead |

### Technology Stack Examples

#### Monolith

```
┌─────────────────────────────────────┐
│           Load Balancer             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Application Server          │
│  ┌─────────────────────────────┐    │
│  │  Rails / Django / Spring     │    │
│  │  All features in one codebase│    │
│  └─────────────────────────────┘    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│           PostgreSQL                │
└─────────────────────────────────────┘
```

#### Modular Monolith

```
┌─────────────────────────────────────┐
│           Load Balancer             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Application Server          │
│  ┌─────────┬─────────┬─────────┐   │
│  │ Users   │ Orders  │ Products│   │
│  │ Module  │ Module  │ Module  │   │
│  └────┬────┴────┬────┴────┬────┘   │
│       │ Internal APIs     │        │
└───────┴─────────┬─────────┴────────┘
                  │
┌─────────────────▼───────────────────┐
│   PostgreSQL (schema per module)    │
└─────────────────────────────────────┘
```

#### Microservices

```
┌─────────────────────────────────────┐
│         API Gateway / Mesh          │
└───┬─────────────┬─────────────┬─────┘
    │             │             │
┌───▼───┐    ┌────▼───┐    ┌───▼────┐
│ Users │    │ Orders │    │Products│
│Service│    │Service │    │Service │
└───┬───┘    └────┬───┘    └───┬────┘
    │             │             │
┌───▼───┐    ┌────▼───┐    ┌───▼────┐
│User DB│    │Order DB│    │Prod DB │
└───────┘    └────────┘    └────────┘
```

#### Serverless

```
┌─────────────────────────────────────┐
│          API Gateway                │
└───┬─────────────┬─────────────┬─────┘
    │             │             │
┌───▼───┐    ┌────▼───┐    ┌───▼────┐
│Lambda │    │Lambda  │    │Lambda  │
│GetUser│    │CreateOrd│   │ListProd│
└───┬───┘    └────┬───┘    └───┬────┘
    │             │             │
    └─────────────┼─────────────┘
                  │
         ┌────────▼────────┐
         │   DynamoDB      │
         └─────────────────┘
```

### Decision Checklist

Before finalizing pattern selection, verify:

- [ ] Team has required skills (or plan to acquire)
- [ ] Budget covers operational costs at projected scale
- [ ] Timeline accounts for infrastructure setup
- [ ] Migration path exists if requirements change
- [ ] Trade-offs are explicitly accepted by stakeholders
- [ ] Pattern matches actual needs, not industry hype
