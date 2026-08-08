# Anti-patterns — bad vs good modelling

Paired instance graphs that show **common mistakes** and the **corrected** form.

Always load with the TBox:

```text
ontology/agsmo.ttl  +  anti-patterns/0N_bad_….ttl   # expect SHACL fail (except orphan action)
ontology/agsmo.ttl  +  anti-patterns/0N_good_….ttl  # expect SHACL pass
```

| Pair | Bad | Good | Main lesson |
|------|-----|------|-------------|
| **01** | `01_bad_no_step_index.ttl` | `01_good_with_step_index.ttl` | SubGoals need `stepIndex` for plan order |
| **02** | `02_bad_orphan_action.ttl` | `02_good_linked_action.ttl` | Link Goal `--achievedBy-->` Action |
| **03** | `03_bad_action_no_performer.ttl` | `03_good_action_with_performer.ttl` | Action needs `performedBy` |
| **04** | `04_bad_status_string.ttl` | `04_good_status_string.ttl` | Status ∈ active\|completed\|failed\|abandoned |
| **05** | `05_bad_outcome_no_success.ttl` | `05_good_outcome_with_success.ttl` | Outcome needs boolean `success` |

**Note on pair 02:** First-cut SHACL does **not** require `achievedBy` (actions can exist without a goal link). The orphan-action case is still a **modelling** anti-pattern for planning/explainability; CI checks the *good* graph passes SHACL and documents the bad narrative in the tutorial.

CI: `tests/test_anti_patterns.py`  
Tutorial: https://sadnanalmanir.github.io/agsmo/tutorial/#mistakes
