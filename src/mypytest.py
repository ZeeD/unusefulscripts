from functools import wraps
from typing import TYPE_CHECKING
from typing import Unpack
from unittest.case import TestCase

if TYPE_CHECKING:
    from collections.abc import Callable
    from contextlib import AbstractContextManager


def depends_on[T, *Ts](
    ctx: 'Callable[[], AbstractContextManager[T]]',
) -> (
    'Callable[[Callable[[T, Unpack[Ts]], None]], Callable[[Unpack[Ts]], None]]'
):
    def deco(
        fun: 'Callable[[T, Unpack[Ts]], None]',
    ) -> 'Callable[[Unpack[Ts]], None]':
        @wraps(fun)
        def ret(*ts: Unpack[Ts]) -> None:  # noqa: UP044
            with ctx() as t:
                fun(t, *ts)

        return ret

    return deco


def test(fun: 'Callable[[], None]') -> type[TestCase]:
    class TC(TestCase):
        @wraps(fun)
        def test_fun(self) -> None:
            fun()

    return TC
