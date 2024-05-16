import pytest
from pywgraph import (
    WeightedDirectedGraph, 
    WeightedDirectedEdge, 
    NodeAlreadyExists, 
    NodeNotFound,
    EdgeAlreadyExists,
    EdgeNotFound
)


def graph() -> WeightedDirectedGraph:
    nodes = {"A", "B", "C"}
    edges = {
        WeightedDirectedEdge("A", "B", 7),
        WeightedDirectedEdge("A", "C", 9),
        WeightedDirectedEdge("B", "C", 10),
    }
    return WeightedDirectedGraph(nodes, edges)


_dict_graph: dict[str, dict[str, float]] = {
    "A": {"B": 7, "C": 9},
    "B": {"C": 10},
    "C": {},
}


class TestWeightedDirectedGraph:

    def test_nodes(self):
        assert graph().nodes == {"A", "B", "C"}

    def test_edges(self):
        assert graph().edges == {
            WeightedDirectedEdge("A", "B", 7),
            WeightedDirectedEdge("A", "C", 9),
            WeightedDirectedEdge("B", "C", 10),
        }

    @pytest.mark.deprecated
    def test_well_defined(self):
        assert graph().check_definition()

    def test_well_defined_property(self): 
        assert graph().is_well_defined

    @pytest.mark.deprecated
    def test_bad_defined(self):
        assert (
            WeightedDirectedGraph(
                {"A"}, {WeightedDirectedEdge("A", "B", 7)}
            ).check_definition()
            == False
        )

    def test_bad_defined_property(self):
        assert (
            WeightedDirectedGraph(
                {"A"}, {WeightedDirectedEdge("A", "B", 7)}
            ).is_well_defined
            == False
        )

    def test_children(self):
        assert graph().children("A") == {"B", "C"}

    def test_parents(self):
        assert graph().parents("C") == {"A", "B"}

    def test_equal(self):
        nodes = {"A", "B", "C"}
        edges = {
            WeightedDirectedEdge("A", "B", 7),
            WeightedDirectedEdge("A", "C", 9),
            WeightedDirectedEdge("B", "C", 10),
        }
        same_graph = WeightedDirectedGraph(nodes, edges)
        assert graph() == same_graph

    def test_fill_reverse_edges_inplace(self):
        filled_graph = WeightedDirectedGraph(
            {"A", "B", "C"},
            {
                WeightedDirectedEdge("A", "B", 7),
                WeightedDirectedEdge("B", "A", 1 / 7),
                WeightedDirectedEdge("A", "C", 9),
                WeightedDirectedEdge("C", "A", 1 / 9),
                WeightedDirectedEdge("B", "C", 10),
                WeightedDirectedEdge("C", "B", 1 / 10),
            },
        )
        graph_copy = graph()
        graph_copy.add_reverse_edges(inplace=True)
        assert graph_copy == filled_graph

    def test_fill_reverse_edges(self):
        filled_graph = WeightedDirectedGraph(
            {"A", "B", "C"},
            {
                WeightedDirectedEdge("A", "B", 7),
                WeightedDirectedEdge("B", "A", 1 / 7),
                WeightedDirectedEdge("A", "C", 9),
                WeightedDirectedEdge("C", "A", 1 / 9),
                WeightedDirectedEdge("B", "C", 10),
                WeightedDirectedEdge("C", "B", 1 / 10),
            },
        )
        assert graph().add_reverse_edges() == filled_graph

    def test_from_dict_method(self):
        graph_from_dict = WeightedDirectedGraph.from_dict(_dict_graph)
        assert graph() == graph_from_dict

    def test_add_node(self):
        graph_copy = graph()
        extended_graph = graph_copy.add_node("D", inplace=False)
        update_dict = _dict_graph.copy()
        update_dict["D"] = {}
        assert WeightedDirectedGraph.from_dict(update_dict) == extended_graph

    def test_add_node_inplace(self):
        graph_copy = graph()
        graph_copy.add_node("D", inplace=True)
        update_dict = _dict_graph.copy()
        update_dict["D"] = {}
        assert WeightedDirectedGraph.from_dict(update_dict) == graph_copy

    def test_add_node_exception(self):
        with pytest.raises(NodeAlreadyExists):
            graph().add_node("A")

    def test_delete_node(self): 
        graph_copy = graph()
        new_dict = _dict_graph.copy()
        del new_dict["A"]
        new_graph = WeightedDirectedGraph.from_dict(new_dict)
        assert graph_copy.delete_node("A", inplace=False) == new_graph

    def test_delete_node_inplace(self):
        graph_copy = graph()
        new_dict = _dict_graph.copy()
        del new_dict["A"]
        new_graph = WeightedDirectedGraph.from_dict(new_dict)
        graph_copy.delete_node("A", inplace=True)
        assert graph_copy == new_graph

    def test_delete_node_exception(self):
        with pytest.raises(NodeNotFound):
            graph().delete_node("D")

    # region Testing adding edges
    def test_add_edge_naive(self):
        graph_copy = graph()
        new_graph = graph_copy.add_edge("C", "A", 10, inplace=False)
        update_dict = _dict_graph.copy()
        update_dict["C"] = update_dict["C"] | {"A": 10}
        assert WeightedDirectedGraph.from_dict(update_dict) == new_graph

    def test_add_edge_naive_inplace(self):
        graph_copy = graph()
        graph_copy.add_edge("C", "A", 10, inplace=True)
        update_dict = _dict_graph.copy()
        update_dict["C"] = update_dict["C"] | {"A": 10}
        assert WeightedDirectedGraph.from_dict(update_dict) == graph_copy

    def test_add_edge_weight_ignore_rest(self):
        """If weight is given the result will not depend on any other argument"""
        graph_copy = graph()
        new_graph = graph_copy.add_edge(
            start="C",
            end="A",
            weight=10,
            path=[1, 4, 5, 65, 6],  # Should reach this although is not a path
            allow_inverse=False,
            inplace=False,
        )
        update_dict = _dict_graph.copy()
        update_dict["C"] = update_dict["C"] | {"A": 10}
        assert WeightedDirectedGraph.from_dict(update_dict) == new_graph

    def test_add_edge_good_path(self):
        graph = WeightedDirectedGraph.from_dict(
            {
                "A": {"B": 2},
                "B": {"C": 3},
                "C": {},
            }
        )
        path = ["A", "B", "C"]
        new_graph = graph.add_edge(start="A", end="C", path=path, inplace=False)
        result_graph = WeightedDirectedGraph.from_dict(
            {
                "A": {"B": 2, "C": 6},
                "B": {"C": 3},
                "C": {},
            }
        )
        assert new_graph == result_graph

    def test_add_edge_good_path_inplace(self):
        graph = WeightedDirectedGraph.from_dict(
            {
                "A": {"B": 2},
                "B": {"C": 3},
                "C": {},
            }
        )
        path = ["A", "B", "C"]
        graph.add_edge(start="A", end="C", path=path, inplace=True)
        result_graph = WeightedDirectedGraph.from_dict(
            {
                "A": {"B": 2, "C": 6},
                "B": {"C": 3},
                "C": {},
            }
        )
        assert graph == result_graph

    def test_add_edge_bad_path(self):
        graph_copy = graph()
        path = ["C", "A"]
        with pytest.raises(ValueError):
            graph_copy.add_edge(
                start="C", end="A", path=path, inplace=False, allow_inverse=False
            )

    def test_add_edge_reverse_path(self):
        graph_copy = graph()
        path = ["C", "A", "B"]
        new_graph = graph_copy.add_edge(
            start="C", end="B", path=path, inplace=False, allow_inverse=True
        )
        update_dict = _dict_graph.copy()
        update_dict["C"] = update_dict["C"] | {"B": (1/9) * 7}
        assert WeightedDirectedGraph.from_dict(update_dict) == new_graph

    @pytest.mark.deprecated
    def test_add_edge_find_path(self): 
        graph_copy = graph()
        new_graph = graph_copy.add_edge(start="C", end="A", inplace=False, allow_inverse=True)
        update_dict = _dict_graph.copy()
        update_dict["C"] = update_dict["C"] | {"A": 1/9}
        assert WeightedDirectedGraph.from_dict(update_dict) == new_graph

    @pytest.mark.deprecated
    def test_add_edge_find_non_existing_path(self): 
        graph_copy = graph()
        assert graph_copy == graph_copy.add_edge(start="C", end="A", inplace=False, allow_inverse=False)

    def test_add_edge_bad_nodes(self): 
        graph_copy = graph()
        with pytest.raises(NodeNotFound):
            graph_copy.add_edge(start="S", end="A", weight=2)

    def test_add_edge_existing_edge(self): 
        graph_copy = graph()
        with pytest.raises(EdgeAlreadyExists):
            graph_copy.add_edge(start="A", end="B", weight=2, inplace=True)

        assert graph_copy == graph()

    def test_delete_edge(self): 
        graph_copy = graph()
        new_dict = _dict_graph.copy()
        new_dict["B"] = {}
        new_graph = WeightedDirectedGraph.from_dict(new_dict)
        assert new_graph == graph_copy.delete_edge(start="B", end="C", inplace=False)

    def test_delete_edge_inplace(self):
        graph_copy = graph()
        new_dict = _dict_graph.copy()
        new_dict["B"] = {}
        new_graph = WeightedDirectedGraph.from_dict(new_dict)
        graph_copy.delete_edge(start="B", end="C", inplace=True)
        assert graph_copy == new_graph

    def test_delete_edge_bad_nodes(self):
        graph_copy = graph()
        with pytest.raises(NodeNotFound):
            graph_copy.delete_edge(start="S", end="A")

    def test_delete_edge_bad_edges(self):
        graph_copy = graph()
        with pytest.raises(EdgeNotFound):
            graph_copy.delete_edge(start="C", end="B")