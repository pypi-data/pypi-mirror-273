from functools import reduce  # type: ignore
from numpy import inf
from math import factorial
from warnings import warn  # type: ignore
from ..groups import Group, real_multiplicative_group
from ..exceptions import NodeNotFound, NodeAlreadyExists, EdgeAlreadyExists, EdgeNotFound  # type: ignore
from .._wrappers import deprecation_warning, behavior_change_warning  # type: ignore
from ._edge import WeightedDirectedEdge  # type: ignore
from ._paths import PathExplorer, Path, Cycle  # type: ignore


def _check_nodes_in_edges(
    nodes: set[str],
    edges: set[WeightedDirectedEdge],
) -> bool:
    edge_nodes = set().union(*[{edge.start, edge.end} for edge in edges])
    return edge_nodes <= nodes


# def _check_weights_of_edges(
#     edges: set[WeightedDirectedEdge],
#     group: Group,
# ) -> set[WeightedDirectedEdge]:
#     if group._group_checker is None:
#         raise ValueError(
#             "Unable to check if weights are in the group because no checker function was provided"
#         )
#     bad_edges = {edge for edge in edges if not group.check(edge.weight)}
#     return bad_edges


class WeightedDirectedGraph:

    def __init__(
        self,
        nodes: set[str],
        edges: set[WeightedDirectedEdge],
        group: Group = real_multiplicative_group,
    ) -> None:
        self._nodes = nodes
        self._edges = edges
        self._group = group

    # region Properties
    @property
    def nodes(self) -> set[str]:
        return self._nodes

    @property
    def edges(self) -> set[WeightedDirectedEdge]:
        return self._edges

    @property
    def group(self) -> Group:
        return self._group

    @property
    def is_well_defined(self) -> bool:
        """Checks if the graph is defined correctly. This is, that all edges nodes are in the nodes set."""
        return _check_nodes_in_edges(self.nodes, self.edges)

    @property
    def cycles(self) -> set[Cycle]:
        """Returns all cycles in the graph."""
        return set.union(*[set(self.get_node_cycles(node)) for node in self.nodes])

    @property
    def is_conmutative(self) -> bool:
        """Checks if the graph is conmutative. This is, that given two paths with the same
        starting and ending nodes, the weight of traversing both paths is the same."""
        complete_graph = self.add_reverse_edges(inplace=False)
        group = self.group
        identity = group.identity
        check = all(
            group.equal(complete_graph.path_weight(cycle), identity)
            for cycle in complete_graph.cycles
        )
        return check

    # region Node methods
    @deprecation_warning(
        f"This is method is deprecated and will be removed in the future. Use the property 'is_well_defined' instead."
    )
    def check_definition(self) -> bool:
        """Checks if the graph is defined correctly."""
        return _check_nodes_in_edges(self.nodes, self.edges)

    def children(self, node: str) -> set[str]:
        """Returns the children of a node."""
        if node not in self._nodes:
            raise NodeNotFound(node)
        return {edge.end for edge in self._edges if edge.start == node}

    def parents(self, node: str) -> set[str]:
        """Returns the parents of a node."""
        if node not in self._nodes:
            raise NodeNotFound(node)
        return {edge.start for edge in self._edges if edge.end == node}

    def add_node(self, node: str, inplace: bool = False):
        """Adds a node to the graph"""
        if node in self._nodes:
            raise NodeAlreadyExists(node)
        if inplace:
            self._nodes.add(node)
            return

        return_graph = WeightedDirectedGraph(
            nodes=self._nodes | {node}, edges=self._edges, group=self.group
        )
        return return_graph

    def delete_node(self, node: str, inplace: bool = False):
        """Deletes a node from the graph. Also removes all edges connected to this node."""
        if node not in self._nodes:
            raise NodeNotFound(node)

        node_edges = {
            edge for edge in self._edges if edge.start == node or edge.end == node
        }
        good_edges = self.edges - node_edges

        if inplace:
            self._nodes.remove(node)
            self._edges = good_edges
            return

        return_graph = WeightedDirectedGraph(
            nodes=self._nodes - {node}, edges=good_edges, group=self.group
        )
        return return_graph

    # region Edge methods
    def add_edge(
        self,
        start: str,
        end: str,
        weight: "Group.element" = None,
        path: list[str] | None = None,
        allow_inverse: bool = True,
        inplace: bool = False,
    ):
        """Adds an edge connectingh two existing nodes.

        Parameter
        --------
        start: str
            The start node of the edge. Must be an existing node from the graph.
        end: str
            The end node of the edge. Must be an existing node from the graph.
        weight: Optional[Group.element]
            The weight of the edge. If no weight and not path is provided, the weight will be try
            to be calculated finding a path connecting the edges.
        path: Optional[list[str]]
            If this is provided and no weight is given the weight will be calculated using this path.
            If this path is not possible and exception will be raised. It is possible to use
            a path that exists but does not connect start and end node, this might be removed
            in future versions.
        allow_inverse: bool
            If True, allows the creation of the inverse edge to find a path between edges.
        """

        bad_nodes = {start, end} - self._nodes
        if bad_nodes:
            raise NodeNotFound(bad_nodes)
        if (start, end) in {(edge.start, edge.end) for edge in self._edges}:
            raise EdgeAlreadyExists(start, end)

        if weight is None:  # Find weight in another way
            if allow_inverse:
                search_graph = self.add_reverse_edges(inplace=False)
            else:
                search_graph = self

            if path is not None:  # Apply weight of the given path
                weight = search_graph.path_weight(path)
            else:  # Find path to get a weight
                warn(
                    "The behaviour of trying to find a path when no weight or path is given is deprecated and will be removed."
                    + "Instead, either specify weight or find first a path between edges with the 'find_paths' method.",
                    DeprecationWarning,
                )
                path = search_graph.find_path(start, end)
                if not path:
                    print(f"Unable to find a weight to connect edge {start} -> {end}")
                    if inplace:
                        return
                    return self
                else:
                    weight = search_graph.path_weight(path)

        if inplace:
            self._edges.add(WeightedDirectedEdge(start, end, weight, self.group))
            return

        return_graph = WeightedDirectedGraph(
            nodes=self._nodes,
            edges=self._edges | {WeightedDirectedEdge(start, end, weight)},
            group=self.group,
        )
        return return_graph

    def delete_edge(self, start: str, end: str, inplace: bool = False):
        """Deletes an edge connecting two existing nodes."""

        bad_nodes = {start, end} - self._nodes
        if bad_nodes:
            raise NodeNotFound(bad_nodes)

        good_edges = {
            edge for edge in self._edges if (edge.start, edge.end) != (start, end)
        }
        if good_edges == self._edges:
            raise EdgeNotFound(start, end)
        if inplace:
            self._edges = good_edges
            return

        return WeightedDirectedGraph(self._nodes, good_edges, self.group)

    def add_reverse_edges(self, inplace: bool = False):
        """Adds the missing inverse direction edges. The weight assign to this new edges is
        the inverse of the original edge weight."""

        all_inverse_edges = {edge.inverse for edge in self._edges}
        inverse_edges = {
            edge
            for edge in all_inverse_edges
            if edge.start not in self.parents(edge.end)
        }
        if inplace:
            self._edges.update(inverse_edges)
            return

        return WeightedDirectedGraph(
            self._nodes, self._edges | inverse_edges, self.group
        )

    # region Paths methods
    def find_paths(
        self,
        start: str,
        end: str,
        general_max_visitations: int = 1,
        specific_max_visitations: dict[str, int] = {},
        max_iter: int | None = None,
        max_paths: int | None = None,
    ) -> list[Path]:
        """Finds all the paths between two nodes in the graph.

        Parameters
        ----------
        start : str
            The start node.
        end : str
            The end node.
        general_max_visitations : int, optional
            A positive integer that controls the maximum number that a node can be visited
            throughout the search. The default is 1.
        specific_max_visitations : dict[str, int], optional
            A dictionary of node names and their maximum number of visits that the node can
            be visited throughout the search. This overwrites the general_max_visitations parameter
            for the specify nodes. The default is {}.
        max_iter : int, optional
            A positive integer that controls the maximum number of iterations that the searching algorithm
            can perform. If the algorithm reach this number, a warning will be raised. The default is 
            the factorial of the number of nodes of the graph.
        max_paths : int, optional
            A positive integer that controls the maximum number of paths that the searching algorithm
            will look for. The default is None, which means that the algorithm will look for all the paths.

        Returns
        -------
        list[Path]
            A list of Path objects containing all the found paths. If no paths are found, an empty list is returned.

        More information about the method
        ---------------------------------
            The most basic way of using this method is just passing the start and end nodes. In this situation,
            the algorithm will look for all the paths between the start and end nodes not allowing node repetition.
            This means that if start and end nodes are the same (you are looking for a cycle), the algorithm will return an empty list
            because it will need to visit the same node twice.

            If you want to look for cycles that contains node 'A', start and end node should be set to 'A'
            and the `specific_max_visitations` parameter should be at least `{'A': 2}`, so the algorithm
            is allowed to visit node 'A' twice.

            Given a graph that connect nodes 'A' and 'B' in both directions and 'B' and 'C' also
            in both directions. We have the following examples:

            Example 1: `start = 'A', end = 'B', general_max_visitations = 2`
                In this scenario the return paths will be `['A','B'], ['A','B','A','B], ['A','B','C','B']`.
            Example 2: `start = 'A', end = 'A', general_max_visitations = 2`
                In this scenario the return paths will be `['A'], ['A','B','A'], ['A','B','C','B','A']`.
                Notice that the null cycle that runs through 'A' is return as `['A']`.
        """

        if max_iter is None: 
            max_iter = factorial(len(self))
        bad_nodes = {start, end} - self._nodes
        if bad_nodes:
            raise NodeNotFound(bad_nodes)

        found_paths = self._find_paths(
            start,
            end,
            general_max_visitations,
            specific_max_visitations,
            max_iter,
            max_paths,
        )
        return found_paths

    @deprecation_warning(
        "This method is deprecated and will be removed. Use 'find_paths' instead limiting the number of return paths to 1."
    )
    def find_path(self, start: str, end: str) -> Path | list:
        """Finds one path between start and end nodes."""

        found_paths = self.find_paths(start=start, end=end, max_paths=1)
        if found_paths:
            return found_paths[0]
        return []

    def get_node_cycles(self, node: str, max_cycles: int | None = None) -> list[Cycle]:
        """Returns a list of Cycle objects containing all the simple cycles that contain the given node."""
        return self._find_cycles(node, max_cycles)

    def path_weight(
        self, path: Path | list, default_value: "Group.element" = None
    ) -> "Group.element":
        """Returns the weight of traversing the given path in the graph. If the given
        path is an empty a list, a default value can be set.

        Parameters
        ----------
        path : Path | list
            The path to calculate the weight.
        default_value : Group.element, optional
            The default value to return if the path is empty. The default is None."""

        path_copy = path.copy()

        if not path_copy:
            return default_value

        if len(path_copy) == 1:
            return self.group.identity

        uknown_nodes = set(path_copy) - self.nodes
        if uknown_nodes:
            raise NodeNotFound(uknown_nodes)
        
        path_pairs = list(zip(path_copy, path_copy[1:]))
        if not all(node_f in self.parents(node_c) for node_f, node_c in path_pairs):
            raise ValueError("The given path is not a valid path in the graph.")
        
        path_edges_weights = [
            edge._weight for edge in self.edges if (edge.start, edge.end) in path_pairs
        ]
        result_weight = reduce(
            self.group.operation, path_edges_weights, self.group.identity  # type: ignore
        )
        return result_weight

    @deprecation_warning(
        "This method is deprecated and will be removed. Use 'path_weight' instead."
    )
    def weight_between(
        self, start: str, end: str, default: "Group.element" = None
    ) -> "Group.element":
        """Returns the weight of the shortest path between two nodes."""
        path = self.find_path(start, end)
        return self.path_weight(path, default)

    # region Classmethods
    @classmethod
    def from_dict(
        cls,
        dict: dict[str, dict[str, "Group.element"]],
        group: Group = real_multiplicative_group,
    ) -> "WeightedDirectedGraph":
        """Creates a graph from a dictionary."""
        nodes = set(dict.keys())
        edges = {
            WeightedDirectedEdge(start, end, weight, group)
            for start, end_dict in dict.items()
            for end, weight in end_dict.items()
        }
        return cls(nodes, edges, group)

    # region Dunder methods
    def __repr__(self) -> str:
        nodes_str = f"Nodes: {self.nodes}\n"
        edges_str = f"Edges:\n"
        for edge in self.edges:
            edges_str += f"{edge}\n"
        return nodes_str + edges_str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, WeightedDirectedGraph):
            return self._nodes == other._nodes and self._edges == other._edges
        return False

    def __len__(self) -> int:
        return len(self._nodes)

    # region Auxiliary methods
    def _iter_aux(
        self,
        explorer: PathExplorer,
        target: str,
        general_max_visitations: int,
        specific_max_visitations: dict[str, int],
    ) -> tuple[list[Path], list[PathExplorer]]:

        current_node = explorer.path[-1]
        visitations = explorer.visitations.copy()
        visitations[current_node] = visitations.get(current_node, 0) + 1
        current_node_vistiations = visitations[current_node]
        current_node_max_vistiations = specific_max_visitations.get(
            current_node, general_max_visitations
        )
        found_path: list[Path] = []
        new_explorers: list[PathExplorer] = []

        if current_node_vistiations > current_node_max_vistiations:
            return found_path, new_explorers

        if current_node == target:
            found_path = [explorer.path]

        children = self.children(current_node)
        forbidden_nodes = {
            node
            for node, rep in visitations.items()
            if rep >= specific_max_visitations.get(node, general_max_visitations)
        }
        unexplored_nodes = children - forbidden_nodes
        if not unexplored_nodes:
            return found_path, new_explorers

        new_explorers = [
            PathExplorer(Path(explorer.path + [node]), visitations)
            for node in unexplored_nodes
        ]
        return found_path, new_explorers

    def _find_paths(
        self,
        start: str,
        end: str,
        general_max_visitations: int = 1,
        specific_max_visitations: dict[str, int] = {},
        max_iter: int = 1_000,
        max_paths: int | None = None,
    ) -> list[Path]:
        if max_paths is None:
            m_paths: int | float = inf
        else:
            m_paths = max_paths
        explorers: list[PathExplorer] = [PathExplorer(Path([start]))]
        all_paths: list[Path] = []

        it = 1
        while explorers and (it < max_iter) and (len(all_paths) < m_paths):
            discovered_path, discovered_explorers = self._iter_aux(
                explorers.pop(0),
                end,
                general_max_visitations,
                specific_max_visitations,
            )
            all_paths.extend(discovered_path)
            new_explorers = list(set(discovered_explorers) - set(explorers))
            explorers.extend(new_explorers)

            it += 1

        if it == max_iter:
            warn(f"Max iterations reached ({max_iter})", Warning)

        return all_paths

    def _find_cycles(self, node: str, max_cycles: int | None) -> list[Cycle]:
        list_cycles = self._find_paths(
            start=node,
            end=node,
            general_max_visitations=1,
            specific_max_visitations={node: 2},
            max_paths=max_cycles,
        )
        return [Cycle(cycle) for cycle in list_cycles]
