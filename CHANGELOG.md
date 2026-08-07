# Changelog

All notable changes to **AGSMO** are documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

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
