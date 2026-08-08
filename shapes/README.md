# AGSMO SHACL shapes (v0.2)

Structural validation for **instance / usage graphs** (ABox), not a replacement
for the OWL TBox in `ontology/agsmo.ttl`.

| File | Role |
|------|------|
| [`agsmo-shapes.ttl`](agsmo-shapes.ttl) | NodeShapes for Agent, Goal, SubGoal, Constraint, Action, Outcome, Episode + dual-edge SPARQL constraints |

## Design (v0.2)

**Required (class shapes):**

- Goal / SubGoal: `description`, controlled `status`
- SubGoal: `stepIndex` ≥ 0
- Action: `description`, `performedBy` → Agent
- Outcome: `description`, `success` (boolean)
- Constraint, Agent, Episode: `description`

**Required (dual edges, AGSMO 0.2):** if a forward link exists, the inverse MUST exist:

| Forward | Inverse |
|---------|---------|
| `hasSubGoal` | `subGoalOf` |
| `hasConstraint` | `constrains` |
| `achievedBy` | `achieves` |
| `hasOutcome` | `outcomeOf` |
| `performedBy` | `performs` |
| `partOfEpisode` | `includes` |

**Optional (allowed missing):**

- `rationale` on Action (recommended for explainability)
- `hasOutcome` (in-progress actions)
- `partOfEpisode`, `timestamp`, constraints on a goal

## Validate locally

```bash
pip install -r requirements-dev.txt
pytest tests/test_shacl.py -q

# or one file with the CLI:
pyshacl -s shapes/agsmo-shapes.ttl \
  -d ontology/agsmo.ttl \
  -d examples/04_literature_review_full.ttl \
  --inference rdfs
```

CI runs these tests before GitHub Pages deploy (same workflow as SPARQL story tests).
