# Agent Semantic Memory Ontology (AGSMO)

| Item | Value |
|------|--------|
| **Name** | Agent Semantic Memory Ontology |
| **Acronym** | AGSMO |
| **File** | [`ontology/agsmo.ttl`](../ontology/agsmo.ttl) |
| **Namespace** | `https://w3id.org/agsmo/ns#` |
| **Version IRI** | `https://w3id.org/agsmo/ns/0.1#` |
| **Version** | 0.1.0 |
| **Prefix** | `agsmo` |
| **License** | MIT |
| **Alignment** | [W3C PROV-O](https://www.w3.org/TR/prov-o/) |

## Naming note

**AGSMO** is distinct from **[ASMO](https://ocdo.github.io/asmo/)** (Atomistic Simulation Methods Ontology). Do not abbreviate this work as ASMO.

## Class hierarchy

```
agsmo:MemoryEntity
├── agsmo:Goal
│   └── agsmo:SubGoal
├── agsmo:Constraint
├── agsmo:Action          ⊑ prov:Activity
├── agsmo:Outcome         ⊑ prov:Entity
└── agsmo:Episode

agsmo:Agent               ⊑ prov:Agent

agsmo:GoalStatus          (statusActive, statusCompleted, statusFailed, statusAbandoned)
```

## Plans

A multi-step **plan** is a root `agsmo:Goal` with ordered `agsmo:SubGoal` children (`agsmo:stepIndex`), optional `agsmo:Constraint`s on the root, and `agsmo:Action` / `agsmo:Outcome` primarily on subgoals. There is no separate Plan class.

## Status values

Stored as `xsd:string` on goals: `active` | `completed` | `failed` | `abandoned`.

## PROV-O in instance graphs

```text
Action  a agsmo:Action , prov:Activity ;
        prov:wasAssociatedWith Agent .
Outcome a agsmo:Outcome , prov:Entity ;
        prov:wasGeneratedBy Action .
```

## Versioning

| Version | Notes |
|---------|--------|
| **0.1.0** | Initial public release |
