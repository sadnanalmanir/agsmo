"""Executable contracts for progressive AGSMO examples.

Loads ontology/agsmo.ttl with each examples/0N_*.ttl graph and asserts the
SPARQL answers documented in examples/README.md. Failing tests mean the
tutorial story drifted — fix the example or the assertion deliberately.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "agsmo.ttl"
EXAMPLES = ROOT / "examples"

AGSMO = Namespace("https://w3id.org/agsmo/ns#")

PREFIX = """
PREFIX agsmo: <https://w3id.org/agsmo/ns#>
PREFIX prov:  <http://www.w3.org/ns/prov#>
"""


def load(*example_names: str) -> Graph:
    g = Graph()
    g.parse(ONTOLOGY, format="turtle")
    for name in example_names:
        path = EXAMPLES / name
        assert path.is_file(), f"missing example file: {path}"
        g.parse(path, format="turtle")
    return g


def rows(g: Graph, body: str) -> list:
    return list(g.query(PREFIX + body))


# ---------------------------------------------------------------------------
# 01 — minimal: agent + one active goal
# ---------------------------------------------------------------------------


def test_01_minimal_goal_has_one_active_goal() -> None:
    g = load("01_minimal_goal.ttl")
    goals = list(g.subjects(RDF.type, AGSMO.Goal))
    # SubGoal is subclass of Goal in TBox, but this file only asserts Goal
    assert len(goals) == 1
    goal = goals[0]
    assert (goal, AGSMO.status, Literal("active")) in g
    descs = list(g.objects(goal, AGSMO.description))
    assert descs and "abstract" in str(descs[0]).lower()

    agents = list(g.subjects(RDF.type, AGSMO.Agent))
    assert len(agents) == 1

    # No actions yet
    assert not list(g.subjects(RDF.type, AGSMO.Action))


def test_01_sparql_active_goals() -> None:
    g = load("01_minimal_goal.ttl")
    r = rows(
        g,
        """
        SELECT ?desc WHERE {
          ?g a agsmo:Goal ;
             agsmo:status "active" ;
             agsmo:description ?desc .
        }
        """,
    )
    assert len(r) == 1


# ---------------------------------------------------------------------------
# 02 — plan structure: ordered subgoals + constraints
# ---------------------------------------------------------------------------


def test_02_plan_has_three_ordered_subgoals() -> None:
    g = load("02_plan_with_constraints.ttl")
    r = rows(
        g,
        """
        SELECT ?step ?status ?desc WHERE {
          ?sg a agsmo:SubGoal ;
              agsmo:stepIndex ?step ;
              agsmo:status ?status ;
              agsmo:description ?desc .
        }
        ORDER BY ?step
        """,
    )
    assert len(r) == 3
    steps = [int(row.step) for row in r]
    assert steps == [0, 1, 2]
    assert all(str(row.status) == "active" for row in r)


def test_02_root_has_constraints_and_subgoals() -> None:
    g = load("02_plan_with_constraints.ttl")
    r = rows(
        g,
        """
        SELECT (COUNT(DISTINCT ?c) AS ?nc) (COUNT(DISTINCT ?sg) AS ?ns) WHERE {
          ?root a agsmo:Goal ;
                agsmo:hasConstraint ?c ;
                agsmo:hasSubGoal ?sg .
          FILTER NOT EXISTS { [] agsmo:hasSubGoal ?root }
        }
        """,
    )
    assert len(r) == 1
    assert int(r[0].nc) >= 2
    assert int(r[0].ns) == 3


def test_02_next_open_step_is_zero() -> None:
    g = load("02_plan_with_constraints.ttl")
    r = rows(
        g,
        """
        SELECT ?step ?desc WHERE {
          ?sg a agsmo:SubGoal ;
              agsmo:status "active" ;
              agsmo:stepIndex ?step ;
              agsmo:description ?desc .
        }
        ORDER BY ?step
        LIMIT 1
        """,
    )
    assert int(r[0].step) == 0
    assert "api" in str(r[0].desc).lower() or "memory" in str(r[0].desc).lower()


# ---------------------------------------------------------------------------
# 03 — action + outcome + rationale (explainability)
# ---------------------------------------------------------------------------


def test_03_action_has_rationale_and_successful_outcome() -> None:
    g = load("03_action_and_explain.ttl")
    r = rows(
        g,
        """
        SELECT ?rationale ?outcome ?ok ?goal WHERE {
          ?a a agsmo:Action ;
             agsmo:rationale ?rationale ;
             agsmo:hasOutcome ?o .
          ?o agsmo:description ?outcome ;
             agsmo:success ?ok .
          ?g agsmo:achievedBy ?a ;
             agsmo:description ?goal .
        }
        """,
    )
    assert len(r) == 1
    assert len(str(r[0].rationale)) > 20
    assert r[0].ok.toPython() is True
    assert "api" in str(r[0].goal).lower() or "memory" in str(r[0].goal).lower()


def test_03_prov_dual_typing() -> None:
    g = load("03_action_and_explain.ttl")
    from rdflib.namespace import Namespace as NS

    PROV = NS("http://www.w3.org/ns/prov#")
    actions = list(g.subjects(RDF.type, AGSMO.Action))
    assert actions
    for a in actions:
        assert (a, RDF.type, PROV.Activity) in g
    outcomes = list(g.subjects(RDF.type, AGSMO.Outcome))
    assert outcomes
    for o in outcomes:
        assert (o, RDF.type, PROV.Entity) in g


# ---------------------------------------------------------------------------
# 04 — full happy path literature review
# ---------------------------------------------------------------------------


def test_04_next_open_step_is_summarize() -> None:
    g = load("04_literature_review_full.ttl")
    r = rows(
        g,
        """
        SELECT ?step ?desc WHERE {
          ?sg a agsmo:SubGoal ;
              agsmo:status "active" ;
              agsmo:stepIndex ?step ;
              agsmo:description ?desc .
        }
        ORDER BY ?step
        LIMIT 1
        """,
    )
    assert len(r) == 1
    assert int(r[0].step) == 1
    assert "summarize" in str(r[0].desc).lower()


def test_04_root_active_progress_one_of_two() -> None:
    g = load("04_literature_review_full.ttl")
    status_rows = rows(
        g,
        """
        SELECT ?status WHERE {
          ?root a agsmo:Goal ;
                agsmo:status ?status ;
                agsmo:description ?d ;
                agsmo:hasSubGoal ?sg .
          FILTER(CONTAINS(LCASE(STR(?d)), "literature"))
          FILTER NOT EXISTS { [] agsmo:hasSubGoal ?root }
        }
        """,
    )
    assert status_rows
    assert str(status_rows[0].status) == "active"

    total = rows(
        g,
        """
        SELECT (COUNT(?sg) AS ?n) WHERE {
          ?root a agsmo:Goal ;
                agsmo:description ?d ;
                agsmo:hasSubGoal ?sg .
          FILTER(CONTAINS(LCASE(STR(?d)), "literature"))
          FILTER NOT EXISTS { [] agsmo:hasSubGoal ?root }
        }
        """,
    )
    done = rows(
        g,
        """
        SELECT (COUNT(?sg) AS ?n) WHERE {
          ?root a agsmo:Goal ;
                agsmo:description ?d ;
                agsmo:hasSubGoal ?sg .
          ?sg agsmo:status "completed" .
          FILTER(CONTAINS(LCASE(STR(?d)), "literature"))
          FILTER NOT EXISTS { [] agsmo:hasSubGoal ?root }
        }
        """,
    )
    assert int(total[0].n) == 2
    assert int(done[0].n) == 1


def test_04_why_search_rationale() -> None:
    g = load("04_literature_review_full.ttl")
    r = rows(
        g,
        """
        SELECT ?rationale ?goal ?outcome WHERE {
          ?a a agsmo:Action ;
             agsmo:description ?ad ;
             agsmo:rationale ?rationale .
          FILTER(CONTAINS(LCASE(STR(?ad)), "queried"))
          ?g agsmo:achievedBy ?a ; agsmo:description ?goal .
          ?a agsmo:hasOutcome ?o .
          ?o agsmo:description ?outcome ; agsmo:success true .
        }
        """,
    )
    assert len(r) == 1
    assert "peer-reviewed" in str(r[0].rationale).lower() or "seed" in str(r[0].rationale).lower()
    assert "search" in str(r[0].goal).lower() or "papers" in str(r[0].goal).lower()


def test_04_constraints_on_root() -> None:
    g = load("04_literature_review_full.ttl")
    r = rows(
        g,
        """
        SELECT ?cDesc WHERE {
          ?root a agsmo:Goal ;
                agsmo:hasConstraint ?c ;
                agsmo:description ?d .
          ?c agsmo:description ?cDesc .
          FILTER(CONTAINS(LCASE(STR(?d)), "literature"))
        }
        """,
    )
    texts = {str(row.cDesc).lower() for row in r}
    assert any("peer-reviewed" in t for t in texts)
    assert any("2 hours" in t or "hour" in t for t in texts)


# ---------------------------------------------------------------------------
# 05 — failure and roll-up
# ---------------------------------------------------------------------------


def test_05_root_failed_and_has_failed_outcome() -> None:
    g = load("05_failure_and_rollup.ttl")
    r = rows(
        g,
        """
        SELECT ?status WHERE {
          ?root a agsmo:Goal ;
                agsmo:status ?status ;
                agsmo:description ?d .
          FILTER(CONTAINS(LCASE(STR(?d)), "integration") || CONTAINS(LCASE(STR(?d)), "staging"))
          FILTER NOT EXISTS { [] agsmo:hasSubGoal ?root }
        }
        """,
    )
    assert len(r) == 1
    assert str(r[0].status) == "failed"

    failed = rows(
        g,
        """
        SELECT ?action ?outcome WHERE {
          ?o a agsmo:Outcome ;
             agsmo:success false ;
             agsmo:description ?outcome .
          ?a agsmo:hasOutcome ?o ;
             agsmo:description ?action .
        }
        """,
    )
    assert len(failed) >= 1
    assert any("fail" in str(row.outcome).lower() or "test" in str(row.outcome).lower() for row in failed)


def test_05_completed_then_failed_steps() -> None:
    g = load("05_failure_and_rollup.ttl")
    r = rows(
        g,
        """
        SELECT ?step ?status WHERE {
          ?sg a agsmo:SubGoal ;
              agsmo:stepIndex ?step ;
              agsmo:status ?status .
        }
        ORDER BY ?step
        """,
    )
    assert len(r) == 2
    assert int(r[0].step) == 0 and str(r[0].status) == "completed"
    assert int(r[1].step) == 1 and str(r[1].status) == "failed"


# ---------------------------------------------------------------------------
# Ontology hygiene (shared)
# ---------------------------------------------------------------------------


def test_ontology_parses_and_declares_core_classes() -> None:
    g = Graph()
    g.parse(ONTOLOGY, format="turtle")
    assert len(g) > 100
    for name in (
        "Goal",
        "SubGoal",
        "Action",
        "Outcome",
        "Constraint",
        "Episode",
        "Agent",
    ):
        assert (AGSMO[name], RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class")) in g


def test_all_numbered_examples_exist() -> None:
    for n in range(1, 6):
        matches = list(EXAMPLES.glob(f"0{n}_*.ttl"))
        assert len(matches) == 1, f"expected one file for step {n}, got {matches}"
