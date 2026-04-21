# Roadmap Generator

Creates structured implementation roadmaps that transform architecture designs into actionable plans with clear phases, milestones, and validation gates.

## When to Use

- After architecture design is complete
- When translating strategic goals into execution plans
- Creating project timelines with realistic effort estimates
- Breaking down large initiatives into manageable phases

## Roadmap Structure

### Three-Phase Framework

Every roadmap follows MVP → Scale → Advanced phases:

```
Phase 1: MVP (Foundation)
├── Goal: Prove core value proposition
├── Duration: Typically 6-12 weeks
├── Success Criteria: Core functionality working
└── Exit Gate: User validation / metrics threshold

Phase 2: Scale (Growth)
├── Goal: Handle production load, improve reliability
├── Duration: Typically 8-16 weeks
├── Success Criteria: Performance SLAs met
└── Exit Gate: Load testing passed / uptime targets

Phase 3: Advanced (Optimization)
├── Goal: Competitive features, optimization
├── Duration: Ongoing
├── Success Criteria: Feature parity / differentiation
└── Exit Gate: Business metrics achieved
```

## Epic/Story/Task Hierarchy

### Epic
High-level capability that delivers business value.
- **Duration**: 2-6 weeks
- **Format**: "Enable [user] to [capability]"
- **Example**: "Enable customers to receive real-time order notifications"

### Story
User-facing functionality within an epic.
- **Duration**: 2-5 days
- **Format**: "As a [user], I want to [action] so that [benefit]"
- **Example**: "As a customer, I want push notifications so I know when my order ships"

### Task
Technical work to complete a story.
- **Duration**: 2-8 hours
- **Format**: "[Verb] [object] [context]"
- **Example**: "Implement WebSocket connection handler for notification service"

---

## Effort Estimation Framework

### T-Shirt Sizing

| Size | Story Points | Typical Duration | Characteristics |
|------|-------------|------------------|-----------------|
| XS | 1 | 2-4 hours | Trivial change, no unknowns |
| S | 2 | 0.5-1 day | Simple, well-understood |
| M | 3 | 1-2 days | Some complexity, minor unknowns |
| L | 5 | 3-5 days | Complex, some research needed |
| XL | 8 | 1-2 weeks | Very complex, significant unknowns |
| XXL | 13+ | > 2 weeks | Should be broken down |

### Estimation Guidelines

1. **Include buffer**: Add 20-30% for unknowns
2. **Account for context switching**: Multiply by 1.3 for teams juggling priorities
3. **New technology penalty**: Add 50% for unfamiliar tech
4. **Integration tax**: Add 20% for each external system integration

### Team Velocity Calculation

```
Effective Capacity = Team Size × Working Days × Focus Factor × Skill Factor

Focus Factor:
- Dedicated team: 0.8
- 50% allocated: 0.4
- Ad-hoc: 0.2

Skill Factor:
- Expert team: 1.0
- Experienced: 0.8
- Learning curve: 0.5
```

---

## Validation Checkpoints

### Phase Gate Reviews

Each phase ends with a validation gate:

```markdown
## Phase 1 Exit Gate

### Go Criteria
- [ ] Core features functional in staging
- [ ] Unit test coverage > 70%
- [ ] Integration tests passing
- [ ] Performance baseline established
- [ ] Security review completed

### No-Go Signals
- Critical bugs unresolved
- Core functionality missing
- Team capacity insufficient for Phase 2
- Business requirements changed significantly

### Decision
[ ] GO - Proceed to Phase 2
[ ] CONDITIONAL GO - Proceed with identified risks
[ ] NO-GO - Address blockers first
```

### Mid-Phase Checkpoints

- **Week 2**: Architecture validation
- **Week 4**: Integration milestone
- **Week 6**: Feature complete checkpoint
- **Weekly**: Sprint review and course correction

---

## Dependency Management

### Dependency Types

| Type | Description | Mitigation |
|------|-------------|------------|
| **Technical** | Service A needs Service B | Start B early, use mocks |
| **Team** | Need DevOps for deployment | Reserve capacity early |
| **External** | Third-party API integration | Validate early, have fallback |
| **Data** | Need production data for testing | Create synthetic data |

### Critical Path Identification

1. List all dependencies
2. Identify longest chain
3. Mark critical path items
4. Add buffer to critical path (25%)
5. Parallelize non-critical work

---

## Output Format

### Roadmap Document Structure

```markdown
# Implementation Roadmap: [Project Name]

**Created**: [Date]
**Owner**: [Team/Person]
**Architecture Reference**: [Link to architecture doc]

## Executive Summary
[2-3 sentences on approach and timeline]

## Timeline Overview
[Visual timeline or Gantt representation]

## Phase 1: MVP (Weeks 1-8)

### Phase Goals
- [Goal 1]
- [Goal 2]

### Epics

#### Epic 1.1: [Name]
**Duration**: [X weeks]
**Dependencies**: [List]

| Story | Points | Owner | Dependencies |
|-------|--------|-------|--------------|
| [Story 1] | M | [Team] | None |
| [Story 2] | L | [Team] | Story 1 |

**Tasks for Story 1**:
- [ ] [Task 1] (S)
- [ ] [Task 2] (M)

### Phase 1 Exit Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Phase 1 Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Action] |

---

## Phase 2: Scale (Weeks 9-16)
[Same structure as Phase 1]

---

## Phase 3: Advanced (Weeks 17+)
[Same structure as Phase 1]

---

## Resource Requirements

### Team Composition
| Role | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| Backend | 2 FTE | 3 FTE | 2 FTE |
| Frontend | 1 FTE | 2 FTE | 1 FTE |
| DevOps | 0.5 FTE | 1 FTE | 0.5 FTE |

### Infrastructure Costs
| Phase | Monthly Cost | Notes |
|-------|-------------|-------|
| Phase 1 | $X | Development environment |
| Phase 2 | $Y | Staging + production |
| Phase 3 | $Z | Full scale |

---

## Success Metrics

| Metric | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|--------|---------------|----------------|----------------|
| [Metric 1] | [Value] | [Value] | [Value] |
| [Metric 2] | [Value] | [Value] | [Value] |

---

## Appendix

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Open Questions
- [Question 1]
- [Question 2]
```

---

## Anti-Patterns to Avoid

### The Big Bang
Planning everything in detail upfront without iteration.
**Fix**: Plan Phase 1 in detail, Phase 2 at epic level, Phase 3 at theme level.

### The Feature Factory
Listing features without connecting to business outcomes.
**Fix**: Every epic must connect to a measurable business goal.

### The Happy Path
No buffer, no risk mitigation, assumes everything goes perfectly.
**Fix**: Add 25-30% buffer, identify top 5 risks with mitigations.

### The Kitchen Sink
Including every possible feature in MVP.
**Fix**: Ruthlessly cut to core value proposition only.

---

## Estimation Guide

Detailed techniques for accurate effort estimation in technical roadmaps.

### The Estimation Problem

Humans are notoriously bad at estimation, especially for:
- Novel work (never done before)
- Complex work (many unknowns)
- Long-duration work (> 2 weeks)

### T-Shirt Sizing Deep Dive

#### Size Definitions

| Size | Points | Duration | Characteristics | Example |
|------|--------|----------|-----------------|---------|
| **XS** | 1 | 2-4 hours | Config change, copy update, trivial fix | Change environment variable |
| **S** | 2 | 0.5-1 day | Simple, well-understood, no dependencies | Add new API field |
| **M** | 3 | 1-2 days | Some complexity, minor unknowns | Build CRUD endpoint |
| **L** | 5 | 3-5 days | Complex, research needed | Implement authentication |
| **XL** | 8 | 1-2 weeks | Very complex, significant unknowns | Build recommendation engine |
| **XXL** | 13+ | > 2 weeks | Must be broken down | Full microservice |

#### When to Use Each Size

**XS - Trivial**
- You've done this exact thing before
- No code review concerns
- Can be done and deployed in one sitting

**S - Simple**
- Clear implementation path
- Single component affected
- Standard patterns apply

**M - Standard**
- Normal feature work
- May need some research
- Touches 2-3 files/components

**L - Complex**
- Multiple components affected
- Integration work required
- Some architectural decisions

**XL - Very Complex**
- Significant unknowns
- New technology/patterns
- Cross-team coordination
- Should consider breaking down

**XXL - Epic-level**
- Too large for single story
- Must be decomposed
- Red flag if assigned to single item

### Estimation Techniques

#### 1. Reference-Based Estimation

Compare to similar past work:

```
Previous similar feature: 3 weeks
Complexity adjustment: 1.2x (slightly more complex)
Team familiarity: 0.9x (more familiar now)
Estimate: 3 × 1.2 × 0.9 = 3.2 weeks
```

#### 2. Task Decomposition

Break down until tasks are < 1 day:

```
Feature: User Dashboard

Tasks:
├── Design API schema (S: 4h)
├── Implement backend endpoint (M: 8h)
├── Create React components (M: 12h)
├── Write unit tests (S: 4h)
├── Integration tests (S: 4h)
├── Documentation (XS: 2h)
└── Code review + fixes (S: 4h)

Total: 38 hours ≈ 5 days
Add 25% buffer: 6.25 days
Estimate: L (3-5 days) → round up to 1.5 weeks
```

#### 3. Three-Point Estimation

Estimate optimistic, most likely, and pessimistic:

```
Optimistic (O): Everything goes perfectly = 3 days
Most Likely (M): Normal development = 5 days
Pessimistic (P): Everything goes wrong = 12 days

PERT Estimate = (O + 4M + P) / 6
             = (3 + 20 + 12) / 6
             = 5.8 days
```

#### 4. Planning Poker

Team-based estimation:
1. Present story to team
2. Everyone estimates privately
3. Reveal estimates simultaneously
4. Discuss outliers
5. Re-estimate until consensus

### Adjustment Factors

#### Multipliers to Apply

| Factor | Multiplier | When to Apply |
|--------|------------|---------------|
| **New technology** | 1.5x | Team hasn't used tech before |
| **New team member** | 1.3x | < 3 months on project |
| **External dependency** | 1.2x | Per external team/service |
| **Legacy code** | 1.4x | Poorly documented old code |
| **Compliance requirements** | 1.3x | Security/audit requirements |
| **Cross-timezone** | 1.2x | Team spans > 6 hour difference |

#### Velocity Adjustments

```
Theoretical capacity:
  5 engineers × 40 hours = 200 hours/week

Realistic capacity (apply factors):
  - Meetings/admin: 0.8x
  - Context switching: 0.85x
  - Interruptions: 0.9x
  - Learning/research: 0.9x

Effective capacity:
  200 × 0.8 × 0.85 × 0.9 × 0.9 = 110 hours/week

That's 55% of theoretical!
```

### Common Estimation Mistakes

#### 1. The 90% Done Trap
**Mistake**: "We're 90% done" for weeks.
**Fix**: Track tasks to completion, not percentage.

#### 2. Ignoring Integration
**Mistake**: Estimate components in isolation.
**Fix**: Add explicit integration tasks and testing.

#### 3. Happy Path Only
**Mistake**: Estimate assumes no bugs, no blockers.
**Fix**: Always add 20-30% buffer.

#### 4. Scope Creep Blindness
**Mistake**: Estimate original scope, deliver expanded scope.
**Fix**: Re-estimate when scope changes.

#### 5. Anchoring
**Mistake**: First estimate biases all subsequent estimates.
**Fix**: Use planning poker, estimate independently first.

#### 6. Planning Fallacy
**Mistake**: Optimism despite past evidence.
**Fix**: Compare to actual duration of past similar work.

### Estimation for Different Phases

#### Phase 1: MVP
- Estimate in detail (story/task level)
- Add 25% buffer
- Expect 20% scope change

#### Phase 2: Scale
- Estimate at epic level
- Add 30% buffer
- Expect 30% scope change

#### Phase 3: Advanced
- Estimate at theme level only
- Add 40% buffer
- Expect 50% scope change

### Team Velocity

#### Calculating Historical Velocity

```
Sprint 1: 34 points completed
Sprint 2: 28 points completed
Sprint 3: 31 points completed
Sprint 4: 35 points completed

Average velocity: 32 points/sprint
Standard deviation: 2.9 points

Conservative estimate: 29 points/sprint (avg - 1 std dev)
```

#### Using Velocity for Planning

```
Total backlog: 180 points
Conservative velocity: 29 points/sprint
Sprints needed: 180 / 29 = 6.2 sprints

Add buffer (20%): 7.5 sprints
Estimate: 8 sprints (4 months with 2-week sprints)
```

### Estimation Checklist

Before finalizing estimates, verify:

- [ ] Broke down items to < 1 week
- [ ] Considered integration time
- [ ] Accounted for testing
- [ ] Included documentation
- [ ] Added code review time
- [ ] Applied technology multipliers
- [ ] Compared to past similar work
- [ ] Added 20-30% buffer
- [ ] Team agreed on estimates
- [ ] Identified dependencies

### Templates

#### Story Estimation Template

```markdown
## Story: [Title]

### Decomposition
| Task | Estimate | Confidence |
|------|----------|------------|
| [Task 1] | 4h | High |
| [Task 2] | 8h | Medium |
| [Task 3] | 4h | Low |

### Base Estimate
Sum of tasks: 16 hours

### Adjustments
- New technology: +50% (8h)
- Integration: +20% (3h)

### Final Estimate
27 hours ≈ 3.5 days → Size: L

### Risks to Estimate
- [Risk 1]: Could add 1-2 days
- [Risk 2]: Could add 0.5 days
```

#### Project Estimation Summary

```markdown
## Project: [Name]

### Estimated Duration
| Phase | Points | Weeks | Confidence |
|-------|--------|-------|------------|
| MVP | 89 | 8 | High |
| Scale | 120 | 12 | Medium |
| Advanced | 80 | 10 | Low |

### Buffer Applied
- MVP: +25% → 10 weeks
- Scale: +30% → 15.6 weeks
- Advanced: +40% → 14 weeks

### Total: 39.6 weeks (~10 months)

### Key Assumptions
1. Team of 5 engineers
2. 30 points/sprint velocity
3. No major scope changes
```

---

## Python Utilities

This reference includes Python utilities for programmatic roadmap generation.

### generator.py

```python
"""
Roadmap Generator

Generates structured implementation roadmaps with Epic/Story/Task breakdown,
effort estimates, and validation checkpoints.

Usage:
    from generator import RoadmapGenerator

    generator = RoadmapGenerator()
    roadmap = generator.create_roadmap(
        project_name="Notification System",
        phases=[phase1, phase2, phase3],
        team_size=5,
        start_date="2025-01-15"
    )

    print(roadmap.to_markdown())
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict
import json


class Size(Enum):
    """T-shirt sizing for effort estimation"""
    XS = 1  # 2-4 hours
    S = 2   # 0.5-1 day
    M = 3   # 1-2 days
    L = 5   # 3-5 days
    XL = 8  # 1-2 weeks
    XXL = 13  # > 2 weeks, should be broken down


class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 1  # Blocks everything
    HIGH = 2      # Core functionality
    MEDIUM = 3    # Important but not blocking
    LOW = 4       # Nice to have


class RiskLevel(Enum):
    """Risk probability and impact levels"""
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Task:
    """Technical work item (2-8 hours)"""
    title: str
    size: Size
    owner: Optional[str] = None
    completed: bool = False

    def hours(self) -> float:
        """Estimated hours based on size"""
        hours_map = {
            Size.XS: 3,
            Size.S: 6,
            Size.M: 12,
            Size.L: 32,
            Size.XL: 64,
            Size.XXL: 104
        }
        return hours_map[self.size]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "size": self.size.name,
            "hours": self.hours(),
            "owner": self.owner,
            "completed": self.completed
        }


@dataclass
class Story:
    """User-facing functionality (2-5 days)"""
    title: str
    description: str
    size: Size
    tasks: List[Task] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    owner: Optional[str] = None
    priority: Priority = Priority.MEDIUM

    def points(self) -> int:
        """Story points based on size"""
        return self.size.value

    def total_hours(self) -> float:
        """Total estimated hours from tasks"""
        if self.tasks:
            return sum(t.hours() for t in self.tasks)
        # Estimate from size if no tasks defined
        return self.size.value * 8

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "size": self.size.name,
            "points": self.points(),
            "total_hours": self.total_hours(),
            "tasks": [t.to_dict() for t in self.tasks],
            "dependencies": self.dependencies,
            "owner": self.owner,
            "priority": self.priority.name
        }


@dataclass
class Epic:
    """High-level capability (2-6 weeks)"""
    title: str
    description: str
    stories: List[Story] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    owner: Optional[str] = None

    def total_points(self) -> int:
        """Total story points"""
        return sum(s.points() for s in self.stories)

    def total_hours(self) -> float:
        """Total estimated hours"""
        return sum(s.total_hours() for s in self.stories)

    def estimated_weeks(self, team_capacity_hours_per_week: float = 30) -> float:
        """Estimated weeks based on team capacity"""
        return self.total_hours() / team_capacity_hours_per_week

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "stories": [s.to_dict() for s in self.stories],
            "dependencies": self.dependencies,
            "owner": self.owner,
            "total_points": self.total_points(),
            "total_hours": self.total_hours()
        }


@dataclass
class Risk:
    """Project risk"""
    title: str
    description: str
    probability: RiskLevel
    impact: RiskLevel
    mitigation: str
    owner: Optional[str] = None

    def score(self) -> int:
        """Risk score (probability × impact)"""
        return self.probability.value * self.impact.value

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "probability": self.probability.name,
            "impact": self.impact.name,
            "score": self.score(),
            "mitigation": self.mitigation,
            "owner": self.owner
        }


@dataclass
class ExitCriteria:
    """Phase exit gate criteria"""
    criterion: str
    met: bool = False

    def to_dict(self) -> dict:
        return {
            "criterion": self.criterion,
            "met": self.met
        }


@dataclass
class Phase:
    """Implementation phase (MVP, Scale, Advanced)"""
    name: str
    description: str
    goals: List[str]
    epics: List[Epic] = field(default_factory=list)
    exit_criteria: List[ExitCriteria] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)
    duration_weeks: Optional[int] = None

    def total_points(self) -> int:
        """Total story points across all epics"""
        return sum(e.total_points() for e in self.epics)

    def total_hours(self) -> float:
        """Total estimated hours"""
        return sum(e.total_hours() for e in self.epics)

    def estimated_weeks(self, team_capacity_hours_per_week: float = 30) -> float:
        """Estimated weeks based on team capacity"""
        if self.duration_weeks:
            return self.duration_weeks
        return self.total_hours() / team_capacity_hours_per_week

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "goals": self.goals,
            "epics": [e.to_dict() for e in self.epics],
            "exit_criteria": [c.to_dict() for c in self.exit_criteria],
            "risks": [r.to_dict() for r in self.risks],
            "total_points": self.total_points(),
            "total_hours": self.total_hours(),
            "estimated_weeks": self.estimated_weeks()
        }


@dataclass
class TeamAllocation:
    """Team resource allocation per phase"""
    role: str
    phase1_fte: float
    phase2_fte: float
    phase3_fte: float

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "phase1_fte": self.phase1_fte,
            "phase2_fte": self.phase2_fte,
            "phase3_fte": self.phase3_fte
        }


@dataclass
class Roadmap:
    """Complete implementation roadmap"""
    project_name: str
    created_date: str
    owner: str
    summary: str
    phases: List[Phase]
    team: List[TeamAllocation] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)

    def total_weeks(self) -> float:
        """Total estimated weeks across all phases"""
        return sum(p.estimated_weeks() for p in self.phases)

    def total_points(self) -> int:
        """Total story points"""
        return sum(p.total_points() for p in self.phases)

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "created_date": self.created_date,
            "owner": self.owner,
            "summary": self.summary,
            "phases": [p.to_dict() for p in self.phases],
            "team": [t.to_dict() for t in self.team],
            "assumptions": self.assumptions,
            "open_questions": self.open_questions,
            "total_weeks": self.total_weeks(),
            "total_points": self.total_points()
        }

    def to_json(self, indent: int = 2) -> str:
        """Export roadmap as JSON"""
        return json.dumps(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        """Export roadmap as Markdown"""
        lines = [
            f"# Implementation Roadmap: {self.project_name}",
            "",
            f"**Created**: {self.created_date}",
            f"**Owner**: {self.owner}",
            f"**Total Duration**: ~{self.total_weeks():.1f} weeks",
            f"**Total Story Points**: {self.total_points()}",
            "",
            "## Executive Summary",
            "",
            self.summary,
            "",
            "---",
            ""
        ]

        # Phases
        for i, phase in enumerate(self.phases, 1):
            lines.extend([
                f"## Phase {i}: {phase.name}",
                "",
                phase.description,
                "",
                f"**Estimated Duration**: ~{phase.estimated_weeks():.1f} weeks",
                f"**Story Points**: {phase.total_points()}",
                "",
                "### Goals",
                ""
            ])

            for goal in phase.goals:
                lines.append(f"- {goal}")

            lines.extend(["", "### Epics", ""])

            for j, epic in enumerate(phase.epics, 1):
                lines.extend([
                    f"#### Epic {i}.{j}: {epic.title}",
                    "",
                    epic.description,
                    "",
                    f"**Points**: {epic.total_points()} | **Hours**: ~{epic.total_hours():.0f}",
                    ""
                ])

                if epic.stories:
                    lines.extend([
                        "| Story | Size | Points | Dependencies |",
                        "|-------|------|--------|--------------|"
                    ])
                    for story in epic.stories:
                        deps = ", ".join(story.dependencies) if story.dependencies else "None"
                        lines.append(f"| {story.title} | {story.size.name} | {story.points()} | {deps} |")
                    lines.append("")

            # Exit criteria
            if phase.exit_criteria:
                lines.extend(["### Exit Criteria", ""])
                for criteria in phase.exit_criteria:
                    status = "x" if criteria.met else " "
                    lines.append(f"- [{status}] {criteria.criterion}")
                lines.append("")

            # Risks
            if phase.risks:
                lines.extend([
                    "### Risks",
                    "",
                    "| Risk | Probability | Impact | Score | Mitigation |",
                    "|------|-------------|--------|-------|------------|"
                ])
                for risk in sorted(phase.risks, key=lambda r: r.score(), reverse=True):
                    lines.append(f"| {risk.title} | {risk.probability.name} | {risk.impact.name} | {risk.score()} | {risk.mitigation} |")
                lines.append("")

            lines.extend(["---", ""])

        # Team allocation
        if self.team:
            lines.extend([
                "## Resource Requirements",
                "",
                "| Role | Phase 1 | Phase 2 | Phase 3 |",
                "|------|---------|---------|---------|"
            ])
            for alloc in self.team:
                lines.append(f"| {alloc.role} | {alloc.phase1_fte} FTE | {alloc.phase2_fte} FTE | {alloc.phase3_fte} FTE |")
            lines.extend(["", "---", ""])

        # Assumptions
        if self.assumptions:
            lines.extend(["## Assumptions", ""])
            for assumption in self.assumptions:
                lines.append(f"- {assumption}")
            lines.extend(["", "---", ""])

        # Open questions
        if self.open_questions:
            lines.extend(["## Open Questions", ""])
            for question in self.open_questions:
                lines.append(f"- {question}")
            lines.append("")

        return "\n".join(lines)


class RoadmapGenerator:
    """Factory for creating roadmaps"""

    def __init__(self,
                 team_hours_per_week: float = 30,
                 buffer_percentage: float = 0.25):
        self.team_hours_per_week = team_hours_per_week
        self.buffer_percentage = buffer_percentage

    def create_roadmap(self,
                      project_name: str,
                      owner: str,
                      summary: str,
                      phases: List[Phase],
                      team: Optional[List[TeamAllocation]] = None,
                      assumptions: Optional[List[str]] = None,
                      open_questions: Optional[List[str]] = None) -> Roadmap:
        """Create a complete roadmap"""
        return Roadmap(
            project_name=project_name,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            owner=owner,
            summary=summary,
            phases=phases,
            team=team or [],
            assumptions=assumptions or [],
            open_questions=open_questions or []
        )

    def estimate_duration(self,
                         total_points: int,
                         team_size: int,
                         velocity_per_person: float = 8) -> float:
        """Estimate duration in weeks"""
        team_velocity = team_size * velocity_per_person
        weeks = total_points / team_velocity
        # Add buffer
        return weeks * (1 + self.buffer_percentage)


# Example usage
if __name__ == "__main__":
    # Create a sample roadmap
    phase1 = Phase(
        name="MVP",
        description="Core notification functionality",
        goals=[
            "Deliver real-time push notifications",
            "Integrate with existing order system",
            "Achieve < 5 second delivery latency"
        ],
        epics=[
            Epic(
                title="Push Notification Infrastructure",
                description="Set up push notification delivery system",
                stories=[
                    Story("Implement FCM integration", "Integrate Firebase Cloud Messaging", Size.L),
                    Story("Create notification service", "Build core notification microservice", Size.XL),
                    Story("Add delivery tracking", "Track notification delivery status", Size.M)
                ]
            )
        ],
        exit_criteria=[
            ExitCriteria("Push notifications delivered to iOS and Android"),
            ExitCriteria("Delivery latency < 5 seconds at p95"),
            ExitCriteria("Integration tests passing")
        ],
        risks=[
            Risk(
                "FCM rate limits",
                "Firebase may throttle at high volume",
                RiskLevel.MEDIUM,
                RiskLevel.HIGH,
                "Implement batching and retry logic"
            )
        ]
    )

    generator = RoadmapGenerator()
    roadmap = generator.create_roadmap(
        project_name="Notification System",
        owner="Platform Team",
        summary="Implement real-time notification system to reduce support tickets by 60%",
        phases=[phase1],
        team=[
            TeamAllocation("Backend", 2, 3, 2),
            TeamAllocation("Mobile", 1, 2, 1),
            TeamAllocation("DevOps", 0.5, 1, 0.5)
        ],
        assumptions=[
            "FCM/APNs credentials available",
            "Order service can emit events"
        ],
        open_questions=[
            "What's the notification preference UI scope?",
            "Do we need SMS fallback in Phase 1?"
        ]
    )

    print(roadmap.to_markdown())
```
