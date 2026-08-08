"""Bad vs good modelling pairs for AGSMO.

- Bad graphs that violate first-cut SHACL must fail validation.
- Good graphs must pass SHACL.
- Pair 02 (orphan action) is a documentation anti-pattern that still
  conforms to first-cut SHACL; we only assert the good side is linked.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "agsmo.ttl"
SHAPES = ROOT / "shapes" / "agsmo-shapes.ttl"
AP = ROOT / "examples" / "anti-patterns"

AGSMO = Namespace("https://w3id.org/agsmo/ns#")

# (bad_file, good_file, bad_must_fail_shacl)
PAIRS = [
    ("01_bad_no_step_index.ttl", "01_good_with_step_index.ttl", True),
    ("02_bad_orphan_action.ttl", "02_good_linked_action.ttl", False),
    ("03_bad_action_no_performer.ttl", "03_good_action_with_performer.ttl", True),
    ("04_bad_status_string.ttl", "04_good_status_string.ttl", True),
    ("05_bad_outcome_no_success.ttl", "05_good_outcome_with_success.ttl", True),
    ("06_bad_one_sided_link.ttl", "06_good_dual_edges.ttl", True),
]


def _load(*names: str) -> Graph:
    g = Graph()
    g.parse(ONTOLOGY, format="turtle")
    for name in names:
        path = AP / name
        assert path.is_file(), path
        g.parse(path, format="turtle")
    return g


def _shacl(data: Graph) -> tuple[bool, str]:
    shapes = Graph()
    shapes.parse(SHAPES, format="turtle")
    conforms, _, report = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
    )
    return bool(conforms), str(report)


@pytest.mark.parametrize("bad,good,bad_fails", PAIRS, ids=[p[0][:2] for p in PAIRS])
def test_pair_shacl(bad: str, good: str, bad_fails: bool) -> None:
    bad_g = _load(bad)
    good_g = _load(good)

    bad_ok, bad_report = _shacl(bad_g)
    good_ok, good_report = _shacl(good_g)

    assert good_ok, f"{good} should pass SHACL:\n{good_report}"
    if bad_fails:
        assert not bad_ok, f"{bad} should fail SHACL but passed"
    else:
        # Orphan action: still shape-valid; document via linkage test below
        assert bad_ok, f"{bad} unexpected SHACL failure:\n{bad_report}"


def test_orphan_action_not_linked_to_goal() -> None:
    """Modelling check for pair 02: bad graph has no achievedBy."""
    bad = _load("02_bad_orphan_action.ttl")
    good = _load("02_good_linked_action.ttl")

    bad_links = list(bad.subject_objects(AGSMO.achievedBy))
    good_links = list(good.subject_objects(AGSMO.achievedBy))
    assert bad_links == []
    assert len(good_links) >= 1


def test_good_linked_action_has_outcome_chain() -> None:
    g = _load("02_good_linked_action.ttl")
    assert list(g.subjects(RDF.type, AGSMO.Outcome))
    assert list(g.subject_objects(AGSMO.hasOutcome))


def test_anti_pattern_files_exist() -> None:
    for bad, good, _ in PAIRS:
        assert (AP / bad).is_file()
        assert (AP / good).is_file()
