---
name: rnd-architect
description: Architecture patterns, technology selection, roadmap generation, and scalability planning reference material. Loaded by main session during /rnd:spec and /rnd:design, and by the rnd-architect agent for batch scenarios.
user-invocable: false
---

# R&D Architect

The rnd-architect skill is the consolidated knowledge base that powers architecture design capabilities. It contains five reference documents, each covering a specific domain of architecture expertise. Loaded by the main session during `/rnd:spec` and `/rnd:design`, and by the `rnd-architect` agent for batch scenarios.

## Reference Documents

### 1. Architecture Patterns (`reference/architecture-patterns.md`)
**Use when**: Selecting between Monolith, Modular Monolith, Microservices, or Serverless architectures.

Includes:
- Pattern definitions with choose/avoid criteria
- Selection framework (assess, evaluate, decide, migrate)
- Decision matrix with weighted scoring (8 factors)
- Pattern comparison across development, operations, scaling, reliability, and cost
- Anti-patterns to avoid (resume-driven architecture, premature distribution, complexity worship)
- Migration paths between patterns

### 2. Roadmap Generation (`reference/roadmap-generation.md`)
**Use when**: Creating phased implementation plans with Epic/Story/Task breakdown.

Includes:
- Three-phase framework (MVP → Scale → Advanced)
- Epic/Story/Task hierarchy with sizing
- T-shirt sizing deep dive with estimation techniques
- Validation checkpoints and phase gate reviews
- Dependency management and critical path identification
- Team velocity calculation
- Python utilities for programmatic roadmap generation
- Estimation guide with adjustment factors and common mistakes

### 3. Tech Stack Selection (`reference/tech-stack-selection.md`)
**Use when**: Selecting technology stacks for new projects or evaluating framework options.

Includes:
- Quick stack recommendations by project type and team profile
- Frontend/backend/database comparison tables
- Stack templates (SaaS, E-commerce, ML Product, Real-time)
- Language selection matrix
- Framework evaluation checklist
- Migration considerations and risk assessment
- Anti-patterns in technology selection

### 4. Scalability Planning (`reference/scalability-planning.md`)
**Use when**: Planning for growth, diagnosing bottlenecks, or designing systems for scale.

Includes:
- Four scaling stages (Startup → Growth → Scale → Enterprise)
- Architecture diagrams for each stage
- Caching strategies and database optimization
- Sharding strategies and event-driven patterns
- Multi-region deployment patterns
- Bottleneck diagnosis guide
- Capacity planning formulas (connections, replicas, cache sizing)
- Infrastructure cost estimates at each scale

### 5. ML/CV Systems (`reference/ml-cv-systems.md`)
**Use when**: Designing ML systems, selecting models, or planning inference architecture.

Includes:
- Model selection decision trees (text, vision, audio, structured data)
- API vs self-hosted cost comparison framework
- Training pipeline architecture (data → training → serving)
- Inference patterns (synchronous, async, edge)
- Computer vision pipeline design (real-time video, object detection)
- LLM integration patterns (RAG, multi-model routing)
- Performance optimization (quantization, batching)
- Model monitoring and drift detection
- Comprehensive model catalog with benchmarks

## Quick Reference

### Architecture Selection
| Pattern | Best For | Avoid When |
|---------|----------|------------|
| Monolith | <10 devs, <100K users, MVP | Need independent scaling |
| Modular Monolith | 10-30 devs, <1M users | Need polyglot persistence |
| Microservices | >30 devs, >1M users | <5 devs or unclear boundaries |
| Serverless | Event-driven, variable load | Latency-critical or long-running |

### Stack by Project Type
| Project | Frontend | Backend | Database |
|---------|----------|---------|----------|
| SaaS MVP | Next.js | Node.js | PostgreSQL |
| E-commerce | Next.js | Node/Python | PostgreSQL + Redis |
| ML Product | React | FastAPI | PostgreSQL + Vector DB |
| Real-time | React | Node.js | PostgreSQL + Redis |

### Scaling Stages
| Stage | Users | Monthly Cost |
|-------|-------|--------------|
| Startup | 0-10K | $100-300 |
| Growth | 10K-100K | $1K-3K |
| Scale | 100K-1M | $10K-30K |
| Enterprise | 1M+ | $100K+ |

### Effort Estimation
| Size | Points | Duration |
|------|--------|----------|
| XS | 1 | 2-4 hours |
| S | 2 | 0.5-1 day |
| M | 3 | 1-2 days |
| L | 5 | 3-5 days |
| XL | 8 | 1-2 weeks |
| XXL | 13+ | > 2 weeks |

## Usage Flow

```
Design Request
    │
    ▼
[tech-stack-selection] → Select technology stack
    │
    ▼
[architecture-patterns] → Select appropriate architecture
    │
    ▼
[ml-cv-systems] → Design ML components (if applicable)
    │
    ▼
[scalability-planning] → Plan for growth stages
    │
    ▼
Design detailed system architecture
    │
    ▼
[roadmap-generation] → Create phased implementation plan
    │
    ▼
Recommend validation by rnd-critic
```
