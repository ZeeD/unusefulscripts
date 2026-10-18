from contextlib import contextmanager
from logging import getLogger
from typing import TYPE_CHECKING

from mypytest import depends_on
from mypytest import test

if TYPE_CHECKING:
    from collections.abc import Iterator


def fun(a: int, b: int) -> int:
    return a + b


logger = getLogger(__name__)


@contextmanager
def gen_a() -> 'Iterator[int]':
    logger.warning('gen_a - BEFORE')
    try:
        yield 1
    finally:
        logger.warning('gen_a - AFTER')


@contextmanager
def gen_b() -> 'Iterator[int]':
    logger.warning('gen_b - BEFORE')
    try:
        yield 2
    finally:
        logger.warning('gen_b - AFTER')


@contextmanager
@depends_on(gen_b)
def gen_c(b: int) -> 'Iterator[int]':
    logger.warning('gen_c - BEFORE')
    try:
        yield 3 * b
    finally:
        logger.warning('gen_c - AFTER')


@test
@depends_on(gen_c)
@depends_on(gen_a)
def test_fun(a: int, c: int) -> None:
    logger.warning('a: %s, c: %s', a, c)
    expected = a + c
    actual = fun(a, c)
    if expected != actual:
        raise ValueError(expected, actual)
