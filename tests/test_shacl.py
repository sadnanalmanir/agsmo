"""SHACL structural contracts for AGSMO usage graphs (first cut).

Complements SPARQL story tests: shapes check well-formed instance data;
SPARQL tests check the progressive tutorial narratives.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "agsmo.ttl"
SHAPES = ROOT / "shapes" / "agsmo-shapes.ttl"
EXAMPLES = ROOT / "examples"


def _example_files() -> list[Path]:
    files = sorted(EXAMPLES.glob("0[1-5]_*.ttl"))
    assert len(files) == 5, f"expected 5 progressive examples, found {files}"
    return files


def _load_data(*paths: Path) -> Graph:
    g = Graph()
    for p in paths:
        g.parse(p, format="turtle")
    return g


def _validate(data: Graph) -> tuple[bool, str]:
    shapes = Graph()
    shapes.parse(SHAPES, format="turtle")
    conforms, _, report = validate(
        data_graph=data,
        shacl_graph=shapes,
        ont_graph=None,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        js=False,
        debug=False,
    )
    return bool(conforms), str(report)


def test_shapes_file_parses() -> None:
    g = Graph()
    g.parse(SHAPES, format="turtle")
    assert len(g) > 20


@pytest.mark.parametrize("example", _example_files(), ids=lambda p: p.name)
def test_example_conforms_to_shacl(example: Path) -> None:
    data = _load_data(ONTOLOGY, example)
    # Ontology TBox types (owl:Class etc.) are not instance targets we care about;
    # shapes target ABox classes. Loading ontology is needed for rdfs:subClassOf
    # (SubGoal ⊑ Goal) so GoalShape applies to SubGoals.
    conforms, report = _validate(data)
    assert conforms, f"{example.name} failed SHACL:\n{report}"


def test_good_minimal_inline_conforms() -> None:
    """Tiny valid graph (same spirit as example 01)."""
    data = _load_data(ONTOLOGY)
    data.parse(
        data="""
        @prefix agsmo: <https://w3id.org/agsmo/ns#> .
        agsmo:a1 a agsmo:Agent ; agsmo:description "bot" .
        agsmo:g1 a agsmo:Goal ;
          agsmo:description "do a thing" ;
          agsmo:status "active" .
        """,
        format="turtle",
    )
    conforms, report = _validate(data)
    assert conforms, report


def test_bad_goal_missing_status_fails() -> None:
    data = _load_data(ONTOLOGY)
    data.parse(
        data="""
        @prefix agsmo: <https://w3id.org/agsmo/ns#> .
        agsmo:g1 a agsmo:Goal ; agsmo:description "no status" .
        """,
        format="turtle",
    )
    conforms, report = _validate(data)
    assert not conforms
    assert "status" in report.lower() or "Goal" in report


def test_bad_action_missing_performer_fails() -> None:
    data = _load_data(ONTOLOGY)
    data.parse(
        data="""
        @prefix agsmo: <https://w3id.org/agsmo/ns#> .
        agsmo:act1 a agsmo:Action ; agsmo:description "did stuff" .
        """,
        format="turtle",
    )
    conforms, report = _validate(data)
    assert not conforms
    assert "performedBy" in report or "Action" in report


def test_bad_status_value_fails() -> None:
    data = _load_data(ONTOLOGY)
    data.parse(
        data="""
        @prefix agsmo: <https://w3id.org/agsmo/ns#> .
        agsmo:g1 a agsmo:Goal ;
          agsmo:description "x" ;
          agsmo:status "done" .
        """,
        format="turtle",
    )
    conforms, report = _validate(data)
    assert not conforms
