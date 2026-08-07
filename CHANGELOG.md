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
- MIT license, README, documentation, CodeMeta metadata

### Notes

- **AGSMO** is not [ASMO](https://ocdo.github.io/asmo/) (Atomistic Simulation Methods Ontology)
