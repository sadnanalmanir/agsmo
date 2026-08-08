# Changelog

All notable changes to **AGSMO** are documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## 0.2.0 — 2026-08-08

### Added — Required inverse properties (dual-edge writer contract)

New object properties (inverses of existing links):

| New property | Inverse of |
|--------------|------------|
| `agsmo:achieves` | `agsmo:achievedBy` |
| `agsmo:performs` | `agsmo:performedBy` |
| `agsmo:constrains` | `agsmo:hasConstraint` |
| `agsmo:includes` | `agsmo:partOfEpisode` |

Existing pairs remain: `hasSubGoal`↔`subGoalOf`, `hasOutcome`↔`outcomeOf`.

### Changed

- **Writer contract:** instance graphs MUST assert **both** directions of every object-property link that has an inverse (RDFLib does not materialize `owl:inverseOf`)
- Version IRI: `https://w3id.org/agsmo/ns/0.2#` (`owl:priorVersion` → `…/ns/0.1#`)
- Progressive examples `02`–`05`, `literature_review_plan.ttl`, and good anti-patterns emit dual edges
- SHACL shapes **0.2.0**: SPARQL constraints fail one-sided links
- New anti-pattern pair **06** (one-sided `hasSubGoal` vs dual edges)
- Tutorial SPARQL: Q6–Q8 use inverse paths
- Docs / CodeMeta / README updated for 0.2.0

### Migration from 0.1.x instance data

For every existing triple:

| If you have | Also write |
|-------------|------------|
| `?p hasSubGoal ?c` | `?c subGoalOf ?p` |
| `?g hasConstraint ?c` | `?c constrains ?g` |
| `?g achievedBy ?a` | `?a achieves ?g` |
| `?a hasOutcome ?o` | `?o outcomeOf ?a` |
| `?a performedBy ?ag` | `?ag performs ?a` |
| `?m partOfEpisode ?e` | `?e includes ?m` |

Namespace URI is unchanged (`https://w3id.org/agsmo/ns#`). Only version IRI and writer expectations change.

## 0.1.0 — 2026-08-07

### Added

- First public release of **AGSMO** (Agent Semantic Memory Ontology)
- OWL/Turtle file: [`ontology/agsmo.ttl`](ontology/agsmo.ttl)
- Namespace: `https://w3id.org/agsmo/ns#` (prefix `agsmo:`)
- Version IRI: `https://w3id.org/agsmo/ns/0.1#`
- Core classes: Goal, SubGoal, Constraint, Action, Outcome, Episode, Agent, MemoryEntity
- Multi-step plans via ordered subgoals (`stepIndex`) and constraints
- PROV-O alignment for Action, Outcome, and Agent
- **WIDOCO best-practice metadata** (abstract, introduction, creator entity, citation, codeRepository, status, …)
- **`skos:example` / `vann:example` on every class and property** so HTML docs are understandable
- Progressive instance examples `examples/01_…`–`05_…` plus `queries.sparql` (tutorial path)
- Worked happy path: [`examples/04_literature_review_full.ttl`](examples/04_literature_review_full.ttl)
- MIT license, README, documentation, CodeMeta metadata
- Automated GitHub Pages docs via WIDOCO (LODE term sections)

### Notes

- **AGSMO** is not [ASMO](https://ocdo.github.io/asmo/) (Atomistic Simulation Methods Ontology)
