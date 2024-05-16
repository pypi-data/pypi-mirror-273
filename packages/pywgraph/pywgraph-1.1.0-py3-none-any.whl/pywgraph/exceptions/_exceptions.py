class NodeNotFound(Exception):
    """Exception raised when a node is not found in a graph."""

    def __init__(self, nodes: str | set[str]) -> None:
        super().__init__(f"Nodes {nodes} not found in the graph.")

class NodeAlreadyExists(Exception):
    """Exception raised when a node already exists in a graph."""

    def __init__(self, node: str) -> None:
        super().__init__(f"Node {node} already exists in the graph.")

class EdgeAlreadyExists(Exception):
    """Exception raised when an edge already exists in a graph."""

    def __init__(self, start: str, end: str) -> None:
        super().__init__(f"Edge {start} -> {end} already exists in the graph.")

class EdgeNotFound(Exception):
    """Exception raised when an edge is not found in a graph."""
    def __init__(self, start: str, end: str) -> None:
        super().__init__(f"Edge {start} -> {end} not found in the graph.")