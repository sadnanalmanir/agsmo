# AGSMO examples — learn by building up

**Preferred reading UI:** [HTML tutorial on GitHub Pages](https://sadnanalmanir.github.io/agsmo/tutorial/)  
(source: [`docs/tutorial.html`](../docs/tutorial.html)) · **diagrams:** [`diagrams/`](diagrams/)

These files are **instance graphs** (ABox). Always load the TBox first:

```bash
ontology/agsmo.ttl   +   examples/0N_….ttl
```

```python
from rdflib import Graph
g = Graph()
g.parse("ontology/agsmo.ttl", format="turtle")
g.parse("examples/04_literature_review_full.ttl", format="turtle")
```

## Learning path (read in order)

| # | File | You learn… |
|---|------|------------|
| **01** | [`01_minimal_goal.ttl`](01_minimal_goal.ttl) | Smallest graph: Agent + one Goal |
| **02** | [`02_plan_with_constraints.ttl`](02_plan_with_constraints.ttl) | Plan = root Goal + ordered SubGoals + Constraints (no Plan class) |
| **03** | [`03_action_and_explain.ttl`](03_action_and_explain.ttl) | Action + Outcome + **rationale** (“why?”) + PROV |
| **04** | [`04_literature_review_full.ttl`](04_literature_review_full.ttl) | Full happy path: episode, plan, one completed step, one open step |
| **05** | [`05_failure_and_rollup.ttl`](05_failure_and_rollup.ttl) | Failure: failed step + root `status "failed"` |

Companion SPARQL (commented): [`queries.sparql`](queries.sparql)

> Legacy filename: `literature_review_plan.ttl` is a copy of example **04** for older links.

## Picture of example 04

```text
Episode: literature demo
└── Agent: default planning agent
    └── Goal (plan): literature review on agentic memory   status=active
        ├── Constraint: prefer peer-reviewed sources
        ├── Constraint: finish within 2 hours
        ├── SubGoal [0] search papers     status=completed
        │     └── Action: query indexes
        │           rationale: need seed set; respect peer-review constraint
        │           └── Outcome: 12 candidates, 5 relevant   success=true
        └── SubGoal [1] summarize trade-offs   status=active   ← next open step
```

## Mental model (all examples)

```text
Agent ──performs──► Action ──hasOutcome──► Outcome
  │                    ▲
  │                    │ achievedBy
  │                    │
Episode ◄──partOf── Goal/SubGoal ──hasConstraint──► Constraint
                      │
                      └──hasSubGoal──► SubGoal (stepIndex 0..n)
```

## Try it: next open step (example 04)

```python
from rdflib import Graph

g = Graph()
g.parse("ontology/agsmo.ttl", format="turtle")
g.parse("examples/04_literature_review_full.ttl", format="turtle")

q = """
PREFIX agsmo: <https://w3id.org/agsmo/ns#>
SELECT ?step ?desc WHERE {
  ?sg a agsmo:SubGoal ;
      agsmo:status "active" ;
      agsmo:stepIndex ?step ;
      agsmo:description ?desc .
}
ORDER BY ?step
LIMIT 1
"""
for row in g.query(q):
    print("Next open step:", int(row.step), "—", row.desc)
# Expected: Next open step: 1 — Summarize key architectures and trade-offs
```

## Try it: why did we search? (example 04)

```python
q = """
PREFIX agsmo: <https://w3id.org/agsmo/ns#>
SELECT ?rationale ?goal ?outcome WHERE {
  ?a a agsmo:Action ;
     agsmo:description ?ad ;
     agsmo:rationale ?rationale .
  FILTER(CONTAINS(LCASE(?ad), "queried"))
  ?g agsmo:achievedBy ?a ; agsmo:description ?goal .
  ?a agsmo:hasOutcome ?o .
  ?o agsmo:description ?outcome .
}
"""
for row in g.query(q):
    print("Why:", row.rationale)
    print("For goal:", row.goal)
    print("Result:", row.outcome)
```

## Term-level examples in the OWL file

Every class and property in `ontology/agsmo.ttl` also has:

- `skos:example` — short prose situation  
- `vann:example` — Turtle snippet  

Those appear under each term on the [WIDOCO HTML docs](https://sadnanalmanir.github.io/agsmo/).

## Anti-patterns (bad vs good)

See [`anti-patterns/`](anti-patterns/) for paired mistakes and corrections (stepIndex, orphan actions, status strings, …). Covered in the tutorial under [Common mistakes](https://sadnanalmanir.github.io/agsmo/tutorial/#mistakes).

## Contract tests (CI)

The stories above are enforced by automated tests:

```bash
pip install -r requirements-dev.txt
pytest -q
```

| Suite | Checks |
|-------|--------|
| `tests/test_examples.py` | SPARQL story contracts (next step, failure roll-up, …) |
| `tests/test_shacl.py` | SHACL structure ([`shapes/agsmo-shapes.ttl`](../shapes/agsmo-shapes.ttl)) |
| `tests/test_anti_patterns.py` | Bad graphs fail SHACL where expected; good pairs pass |

On GitHub, `pytest` runs before WIDOCO/Pages deploy. If an example breaks its story **or** its structure, the build fails.