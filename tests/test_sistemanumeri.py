from unittest import TestCase

from sistemanumeri import find_integers
from sistemanumeri import find_integers2
from sistemanumeri import find_integers3


class TestSistemaNumeri(TestCase):
    def test_find_integers(self) -> None:
        for string, expected in [
            ('', ('',)),
            ('a', ('a',)),
            ('1', ('', 1, '')),
            ('a1', ('a', 1, '')),
            ('1a', ('', 1, 'a')),
            ('abc123def456', ('abc', 123, 'def', 456, '')),
        ]:
            with self.subTest(string=string, expected=expected):
                actual = find_integers(string)
                self.assertEqual(expected, actual)

    def test_find_integers2(self) -> None:
        for string, expected in [
            ('', ('',)),
            ('a', ('a',)),
            ('1', ('', 1)),
            ('a1', ('a', 1)),
            ('1a', ('', 1, 'a')),
            ('abc123def456', ('abc', 123, 'def', 456)),
        ]:
            with self.subTest(string=string, expected=expected):
                actual = find_integers2(string)
                self.assertEqual(expected, actual)

    def test_find_integers3(self) -> None:
        for string, expected in [
            ('', ('',)),
            ('a', ('a',)),
            ('1', ('', 1)),
            ('a1', ('a', 1)),
            ('1a', ('', 1, 'a')),
            ('abc123def456', ('abc', 123, 'def', 456)),
        ]:
            with self.subTest(string=string, expected=expected):
                actual = find_integers3(string)
                self.assertEqual(expected, actual)
