# AGSMO examples

Instance graphs that illustrate how to *use* the ontology (not the TBox itself).

| File | What it shows |
|------|----------------|
| [`literature_review_plan.ttl`](literature_review_plan.ttl) | Full multi-step plan: episode, agent, root goal, constraints, ordered subgoals, action, outcome, PROV links |

## Load with RDFLib

```bash
python - <<'PY'
from rdflib import Graph
g = Graph()
g.parse("../ontology/agsmo.ttl", format="turtle")
g.parse("literature_review_plan.ttl", format="turtle")
print("triples", len(g))
print(g.query("""
PREFIX agsmo: <https://w3id.org/agsmo/ns#>
SELECT ?step ?desc ?status WHERE {
  ?g a agsmo:SubGoal ;
     agsmo:stepIndex ?step ;
     agsmo:description ?desc ;
     agsmo:status ?status .
} ORDER BY ?step
"""))
for row in g.query("""
PREFIX agsmo: <https://w3id.org/agsmo/ns#>
SELECT ?step ?desc ?status WHERE {
  ?g a agsmo:SubGoal ;
     agsmo:stepIndex ?step ;
     agsmo:description ?desc ;
     agsmo:status ?status .
} ORDER BY ?step
"""):
    print(int(row.step), row.status, row.desc)
PY
```

## Expected story

1. Agent starts episode `demo-1`
2. Creates plan goal `lit-review` with constraints (peer-reviewed, time-box)
3. Adds subgoals `search-papers` (step 0) and `summarize` (step 1)
4. Completes step 0 with a justified search action and successful outcome
5. Leaves step 1 open (`status` = `active`) — this is the next work item
