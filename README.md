# AGSMO — Agent Semantic Memory Ontology

**Formal OWL vocabulary for long-term semantic memory of AI agents:** goals, ordered subgoals (plans), constraints, actions, outcomes, episodes, and agents — with [W3C PROV-O](https://www.w3.org/TR/prov-o/) alignment for provenance and explainability.

| | |
|--|--|
| **Full name** | Agent Semantic Memory Ontology |
| **Acronym** | **AGSMO** |
| **Version** | 0.1.0 |
| **Preferred prefix** | `agsmo` |
| **Namespace IRI** | `https://w3id.org/agsmo/ns#` |
| **Version IRI** | `https://w3id.org/agsmo/ns/0.1#` |
| **Serialization** | [`ontology/agsmo.ttl`](ontology/agsmo.ttl) (Turtle / OWL) |
| **License** | [MIT](LICENSE) |
| **CodeMeta** | [`codemeta.json`](codemeta.json) |

> **Not to be confused with** [ASMO — Atomistic Simulation Methods Ontology](https://ocdo.github.io/asmo/) (materials science). That project owns the ASMO acronym; this ontology is **AGSMO**.

## Scope

AGSMO models structured agent memory suitable for:

- Multi-step **planning** (root goal + ordered subgoals + constraints)
- **Actions** and **outcomes** with rationales
- **Episodes** (sessions) and **agents**
- SPARQL queryability and “why did you do X?” provenance

It does **not** claim to cover all agent communication protocols or workflow engines. Aligns with PROV-O; optional future mapping to EP-PLAN / other agent ontologies is out of scope for v0.1.

## Quick load (Python / RDFLib)

```python
from rdflib import Graph

g = Graph()
g.parse("ontology/agsmo.ttl", format="turtle")
print(len(g), "triples")
```

## SPARQL prefix

```sparql
PREFIX agsmo: <https://w3id.org/agsmo/ns#>
PREFIX prov:  <http://www.w3.org/ns/prov#>

SELECT ?g ?desc WHERE {
  ?g a agsmo:Goal ;
     agsmo:description ?desc ;
     agsmo:status "active" .
}
```

## Core classes

| Class | Role |
|-------|------|
| `agsmo:Goal` / `agsmo:SubGoal` | Objectives; plans are goal trees with `agsmo:stepIndex` |
| `agsmo:Constraint` | Rules/limits on goals |
| `agsmo:Action` | What was done (`⊑ prov:Activity`) |
| `agsmo:Outcome` | Result of an action (`⊑ prov:Entity`) |
| `agsmo:Episode` | Session / work window |
| `agsmo:Agent` | Who acted (`⊑ prov:Agent`) |

See [docs/ONTOLOGY.md](docs/ONTOLOGY.md) for properties, plan shape, and versioning.

## Related software

This ontology is used by the **semantic-memory-agent** Python library (agent tool loop + RDFLib store). This repository publishes **only the ontology** for independent citation, reuse, and permanent identifiers.

## Permanent identifiers (w3id)

Target permanent IRIs use the [w3id.org](https://w3id.org/) pattern:

- `https://w3id.org/agsmo/ns#`
- `https://w3id.org/agsmo/ns/0.1#`

A redirect entry on [perma-id/w3id.org](https://github.com/perma-id/w3id.org) can be registered after this repository is public (not required for local use of the Turtle file).

## Citation

```bibtex
@misc{agsmo2026,
  title        = {Agent Semantic Memory Ontology (AGSMO)},
  author       = {Al Manir, Sadnan},
  year         = {2026},
  howpublished = {\url{https://github.com/sadnanalmanir/agsmo}},
  note         = {Version 0.1.0}
}
```

Update the GitHub URL if your account/org name differs.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Sadnan Al Manir.
