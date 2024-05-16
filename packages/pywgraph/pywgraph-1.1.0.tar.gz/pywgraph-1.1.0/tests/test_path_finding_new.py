import pytest
from pywgraph import WeightedDirectedGraph, Cycle


def graph() -> WeightedDirectedGraph:
    _dict = {
        "A":{"B":1},
        "B":{"C":1},
        "C":{},
        "Z":{}
    }
    return WeightedDirectedGraph.from_dict(_dict).add_reverse_edges()


class TestMultiPathFinding:
    def test_is_conmutative(self):
        assert graph().is_conmutative

    def test_naive_path_ab(self):
        assert graph().find_paths("A", "B") == [["A", "B"]]

    def test_naive_path_ac(self):
        assert graph().find_paths("A", "C") == [["A", "B", "C"]]

    def test_path_unexisting(self): 
        assert graph().find_paths("A", "Z") == []

    def test_path_max_visits(self):
        paths = graph().find_paths("A", "B", general_max_visitations=2)
        paths_set_tuples = set(tuple(path) for path in paths)
        solution = {("A", "B"), ("A", "B", "C","B"), ("A", "B", "A", "B")}
        assert paths_set_tuples == solution

    def test_path_max_visits_same_node(self):
        paths = graph().find_paths("A", "A", general_max_visitations=2)
        paths_set_tuples = set(tuple(path) for path in paths)
        solution = {("A",),("A", "B", "A"), ("A", "B", "C", "B", "A")}
        assert paths_set_tuples == solution

    def test_path_max_visits_null(self):
        assert graph().find_paths("A", "B", general_max_visitations=0) == []

    def test_cycles_a(self): 
        cycles = graph().get_node_cycles("A")
        solution = {Cycle(["A", "B", "A"]), Cycle(["A"])}
        assert set(cycles) == solution

    def test_cycles_b(self): 
        cycles = graph().get_node_cycles("B")
        solution = {Cycle(["B", "C", "B"]), Cycle(["B", "A", "B"]), Cycle(["B"])}
        assert set(cycles) == solution

    def test_cycles_z(self):
        cycles = graph().get_node_cycles("Z")
        assert cycles == [Cycle(["Z"])]

    def test_cycles_z_2(self):
        cycles = graph().find_paths("Z", "Z", general_max_visitations=4)
        assert cycles == [["Z"]]

    def test_specific_max_visitations_b(self):
        paths = graph().find_paths("A", "B", specific_max_visitations={"B":2})
        paths_set_tuples = set(tuple(path) for path in paths)
        solution = {("A", "B"), ("A", "B", "C", "B")}
        assert paths_set_tuples == solution

    def test_specific_max_visitations_b_plus_a(self):
        paths = graph().find_paths("A", "B", specific_max_visitations={"A":2, "B":2})
        paths_set_tuples = set(tuple(path) for path in paths)
        solution = {("A", "B"), ("A", "B", "C", "B"), ("A", "B", "A", "B")}
        assert paths_set_tuples == solution

    
        