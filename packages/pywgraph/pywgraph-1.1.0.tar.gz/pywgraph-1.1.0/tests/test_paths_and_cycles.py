import pytest 
from pywgraph import Path, Cycle


def list_path() -> list[str]:
    return ["A", "B", "C", "D"]

def list_cycle() -> list[str]:
    return ["A", "B", "C", "A"]

def list_equivalent_cycle() -> list[str]:
    return ["C","A", "B", "C"]

def list_invalid_path() -> list[str]:
    return ["A", "B", "B"]


class TestPathsAndCycles:

    def test_invalid_path(self):
        with pytest.raises(ValueError):
            Path(list_invalid_path())

    def test_empty_cycle(self):
        with pytest.raises(ValueError):
            Cycle([])

    def test_not_cycle(self):
        with pytest.raises(ValueError):
            Cycle(list_path())

    def test_cycle_from_path(self):
        path = Path(list_cycle())
        Cycle(path)

    def test_equal_cycles(self): 
        assert Cycle(list_cycle()) == Cycle(list_equivalent_cycle())

    def test_path_is_cycle(self):
        assert Path(list_cycle()).is_cycle

    def test_path_is_not_cycle(self):
        assert not Path(list_path()).is_cycle
    