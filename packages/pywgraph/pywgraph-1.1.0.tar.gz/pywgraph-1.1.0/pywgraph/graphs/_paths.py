from functools import cached_property


def _cycle_representations(cycle: list[str]) -> list[list[str]]:
    return [cycle[-i:] + cycle[:-i] for i in range(len(cycle))]


def _canonic_representation(cycle: list[str]) -> list[str]:
    first = min(cycle)
    canonic_representation = [
        representation
        for representation in _cycle_representations(cycle)
        if representation[0] == first
    ][0]
    return canonic_representation


class Path(list[str]):
    """Class that represents a path."""

    def __init__(self, path: list[str]) -> None:
        if any(path[i] == path[i + 1] for i in range(len(path) - 1)):
            raise ValueError("A path can not contain equal consecutive elements")
        super().__init__(path)

    @property
    def is_cycle(self) -> bool:
        return self[0] == self[-1]

    def __hash__(self) -> int:  # type: ignore
        return hash(
            tuple(self)
        )  # Mypy don't allow to override hash for list since lists are not hashable

    def __bool__(self) -> bool:
        return True


class Cycle(Path):
    """Class that represents a cycle. This is, a path that starts and ends with the same element.
    Two cycles are equivalent if they follow the same nodes in the same order. The representation
    of a cycle is given by a canonic representation, which consists of the representation that 
    starts with the 'smallest' node."""

    def __init__(self, cycle: Path | list[str]) -> None:
        if not cycle:
            raise ValueError("A cycle can not be empty")
        if cycle[0] != cycle[-1]:
            raise ValueError("A cycle must start and end with the same element")
        super().__init__(cycle)

        if len(cycle) == 1:
            self._clean_cycle = cycle
        else:
            self._clean_cycle = cycle[:-1]

    @cached_property
    def canonic_representation(self) -> list[str]:
        return _canonic_representation(self._clean_cycle)

    @cached_property
    def equivalent_representations(self) -> list[list[str]]:
        return _cycle_representations(self._clean_cycle)

    def __hash__(self) -> int:  # type: ignore
        return hash(
            tuple(self.canonic_representation)
        )  # Mypy don't allow to override hash for list since lists are not hashable

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cycle):
            if len(other) != len(self):
                return False
            return other.canonic_representation == self.canonic_representation
        return False

    def __repr__(self) -> str:
        return f"Cycle({self.canonic_representation})"


class PathExplorer:
    """Auxiliary object to help in the searching of paths on a graph"""

    def __init__(self, path: Path, visitations: dict[str, int] = {}) -> None:
        self._path = path
        self._visitations = visitations

    @property
    def path(self) -> Path:
        return self._path

    @property
    def visitations(self) -> dict[str, int]:
        return self._visitations

    def __hash__(self) -> int:
        hash_list = hash(tuple(self.path))
        hash_dict = hash(
            tuple(sorted(list(self.visitations.items()), key=lambda x: x[0]))
        )
        return hash_list ^ hash_dict

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PathExplorer):
            return (self.path, self.visitations) == (other.path, other.visitations)
        return False

    def __len__(self) -> int:
        return len(self.path)

    def __repr__(self) -> str:
        return f"PathExplorer({self.path}, {self.visitations})"
