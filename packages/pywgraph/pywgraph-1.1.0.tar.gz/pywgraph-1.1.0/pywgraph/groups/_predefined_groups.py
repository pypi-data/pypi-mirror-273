from typing import Any
from ._groups import Group


def _reals_check(weight: Any) -> bool:
    return isinstance(weight, (int, float))


real_multiplicative_group = Group(
    name="Real numbers with multiplication",
    identity=1.0,
    operation=lambda x, y: x * y,
    inverse_function=lambda x: 1 / x,
    group_checker=_reals_check,
)
