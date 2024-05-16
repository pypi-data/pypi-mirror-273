import pytest
from pywgraph import WeightedDirectedGraph, NodeNotFound


def graph() -> WeightedDirectedGraph:
    dictionary: dict[str, dict[str, float]] = {
        "A": {"B": 1.0, "C": 2.5},
        "B": {"C": 2.5},
        "C": {"A": 1 / 2.5, "D": 1.3},
        "D": {"E": 3.4},
        "E": {"C": 1 / (1.3 * 3.4), "A": 13.0},
        "Z": {},
    }
    return WeightedDirectedGraph.from_dict(dictionary)


class TestPathFinding:

    # region PathFindingTest
    def test_ab(self):
        assert graph().find_paths("A", "B", max_paths=1) == [["A", "B"]]

    def test_ac(self):
        assert graph().find_paths("A", "C", max_paths=1)[0] == ["A", "C"]

    def test_ad(self):
        assert graph().find_paths("A", "D", max_paths=1)[0] == ["A", "C", "D"]

    def test_ae(self):
        assert graph().find_paths("A", "E", max_paths=1)[0] == ["A", "C", "D", "E"]

    def test_ba(self):
        assert graph().find_paths("B", "A", max_paths=1)[0] == ["B", "C", "A"]

    def test_bc(self):
        assert graph().find_paths("B", "C", max_paths=1)[0] == ["B", "C"]

    def test_bd(self):
        assert graph().find_paths("B", "D", max_paths=1)[0] == ["B", "C", "D"]

    def test_be(self):
        assert graph().find_paths("B", "E", max_paths=1)[0] == ["B", "C", "D", "E"]

    def test_ca(self):
        assert graph().find_paths("C", "A", max_paths=1)[0] == ["C", "A"]

    def test_cb(self):
        assert graph().find_paths("C", "B", max_paths=1)[0] == ["C", "A", "B"]

    def test_cd(self):
        assert graph().find_paths("C", "D", max_paths=1)[0] == ["C", "D"]

    def test_ce(self):
        assert graph().find_paths("C", "E", max_paths=1)[0] == ["C", "D", "E"]

    def test_da(self):
        assert graph().find_paths("D", "A", max_paths=1)[0] == ["D", "E", "A"]

    def test_db(self):
        assert graph().find_paths("D", "B", max_paths=1)[0] == ["D", "E", "A", "B"]

    def test_dc(self):
        assert graph().find_paths("D", "C", max_paths=1)[0] == ["D", "E", "C"]

    def test_de(self):
        assert graph().find_paths("D", "E", max_paths=1)[0] == ["D", "E"]

    def test_ea(self):
        assert graph().find_paths("E", "A", max_paths=1)[0] == ["E", "A"]

    def test_eb(self):
        assert graph().find_paths("E", "B", max_paths=1)[0] == ["E", "A", "B"]

    def test_ec(self):
        assert graph().find_paths("E", "C", max_paths=1)[0] == ["E", "C"]

    def test_ed(self):
        assert graph().find_paths("E", "D", max_paths=1)[0] == ["E", "C", "D"]

    def test_az(self):
        assert graph().find_paths("A", "Z", max_paths=1) == []

    def test_self_node(self):
        for node in graph().nodes:
            assert graph().find_paths(node, node, max_paths=1)[0] == [node]

    # region Path weights tests
    def test_path_weight_ab(self):
        path = ["A", "B"]
        assert graph().path_weight(path) == 1.0

    def test_path_weight_empty(self):
        path = []
        assert graph().path_weight(path, 0.0) == 0.0

    def test_path_weight_ae(self):
        path = ["A", "C", "D", "E"]
        assert graph().path_weight(path) == pytest.approx(2.5 * 1.3 * 3.4)

    def test_path_large_path(self): 
        path = ["A", "B", "C", "D", "E", "C", "A"]
        assert graph().path_weight(path) == pytest.approx(1.0)

    def test_path_weight_self_node(self):
        path = ["Z"]
        assert graph().path_weight(path) == 1.0

    @pytest.mark.deprecated
    def test_weight_between_ab(self):
        assert graph().weight_between("A", "B") == 1.0

    @pytest.mark.deprecated
    def test_weight_between_az(self):
        assert graph().weight_between("A", "Z", 0.0) == 0.0

    @pytest.mark.deprecated
    def test_weight_between_ae(self):
        assert graph().weight_between("A", "E") == pytest.approx(2.5 * 1.3 * 3.4)

    @pytest.mark.deprecated
    def test_weight_between_self_nodes(self):
        for node in graph().nodes:
            assert graph().weight_between(node, node) == 1.0

    # region ExceptionTests
    def test_end_node_not_in_graph_find_path(self):
        with pytest.raises(NodeNotFound):
            graph().find_paths("A", "F", max_paths=1)

    def test_start_node_not_in_graph_find_path(self):
        with pytest.raises(NodeNotFound):
            graph().find_paths("F", "E", max_paths=1)

    def test_both_nodes_not_in_graph_find_path(self):
        with pytest.raises(NodeNotFound):
            graph().find_paths("F", "G", max_paths=1)

    @pytest.mark.deprecated
    def test_end_node_not_in_graph_weight_between(self):
        with pytest.raises(NodeNotFound):
            graph().weight_between("A", "F")

    @pytest.mark.deprecated
    def test_start_node_not_in_graph_weight_between(self):
        with pytest.raises(NodeNotFound):
            graph().weight_between("F", "E")

    @pytest.mark.deprecated
    def test_both_nodes_not_in_graph_weight_between(self):
        with pytest.raises(NodeNotFound):
            graph().weight_between("F", "G")

    def test_invalid_path(self): 
        path = ["A", "E"]
        with pytest.raises(ValueError):
            graph().path_weight(path)
