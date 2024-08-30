from unittest import TestCase

from trovaraggruppamenti import raggruppamenti


class TestTrovaraggruppamenti(TestCase):
    def test_raggruppamenti(self) -> None:
        for total_pages, expected in [
            (0, []),
            (1, [(4, 1)]),
            (2, [(4, 1)]),
            (3, [(4, 1)]),
            (4, [(4, 1)]),
            (5, [(4, 2), (8, 1)]),
            (6, [(4, 2), (8, 1)]),
            (7, [(4, 2), (8, 1)]),
            (8, [(4, 2), (8, 1)]),
            (9, [(4, 3), (8, 2), (12, 1)]),
        ]:
            with self.subTest(total_pages=total_pages, expected=expected):
                actual = list(raggruppamenti(total_pages))
                self.assertListEqual(expected, actual)
