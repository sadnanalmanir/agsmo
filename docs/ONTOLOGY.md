# Agent Semantic Memory Ontology (AGSMO)

| Item | Value |
|------|--------|
| **Name** | Agent Semantic Memory Ontology |
| **Acronym** | AGSMO |
| **File** | [`ontology/agsmo.ttl`](../ontology/agsmo.ttl) |
| **Namespace** | `https://w3id.org/agsmo/ns#` |
| **Version IRI** | `https://w3id.org/agsmo/ns/0.2#` |
| **Version** | **0.2.0** |
| **Prior version** | `https://w3id.org/agsmo/ns/0.1#` (0.1.0) |
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

## Writer contract: dual edges (v0.2+)

RDFLib and most triple stores **do not** materialize `owl:inverseOf`.  
**Conformant instance graphs MUST assert both directions** of every linked pair:

| Forward | Inverse | Typical write site |
|---------|---------|-------------------|
| `hasSubGoal` | `subGoalOf` | Parent plan / child step |
| `hasConstraint` | `constrains` | Goal / constraint |
| `achievedBy` | `achieves` | Goal / action |
| `hasOutcome` | `outcomeOf` | Action / outcome |
| `performedBy` | `performs` | Action / agent |
| `partOfEpisode` | `includes` | Goal or action / episode |

Example:

```turtle
agsmo:goal/lit-review agsmo:hasSubGoal agsmo:goal/search-papers .
agsmo:goal/search-papers agsmo:subGoalOf agsmo:goal/lit-review .

agsmo:goal/search-papers agsmo:achievedBy agsmo:action/search .
agsmo:action/search agsmo:achieves agsmo:goal/search-papers .
```

Enforced by SPARQL constraints in [`shapes/agsmo-shapes.ttl`](../shapes/agsmo-shapes.ttl).

## PROV-O in instance graphs

```text
Action  a agsmo:Action , prov:Activity ;
        prov:wasAssociatedWith Agent .
Outcome a agsmo:Outcome , prov:Entity ;
        prov:wasGeneratedBy Action .
```

Also prefer dual-typing agents: `a agsmo:Agent , prov:Agent`.

## Examples (for readers)

Every class and property in the OWL file carries:

- `rdfs:label` / `skos:prefLabel`
- `rdfs:comment` and often `skos:definition`
- **`skos:example`** (prose) and often **`vann:example`** (Turtle snippet)

These appear in WIDOCO/LODE HTML under each term.

**Complete instance graph:** [`examples/literature_review_plan.ttl`](../examples/literature_review_plan.ttl)  
— multi-step plan with dual edges, constraints, ordered subgoals, action, outcome, and PROV links.

Metadata follows the [WIDOCO vocabulary checklist](https://dgarijo.github.io/Widoco/doc/bestPractices/index-en.html).

## Versioning

| Version | Notes |
|---------|--------|
| **0.1.0** | Initial public release |
| **0.2.0** | Required dual edges; new inverses `achieves`, `performs`, `constrains`, `includes`; SHACL dual-edge constraints |
