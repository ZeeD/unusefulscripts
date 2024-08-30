from datetime import UTC
from datetime import datetime
from unittest import TestCase

from estraidata import get_common_prefix


class TestEstraidata(TestCase):
    def test_get_common_prefix(self) -> None:
        for datetimes, expected in [
            (
                iter(
                    [
                        datetime(2009, 11, 29, tzinfo=UTC),
                        datetime(2009, 11, 30, tzinfo=UTC),
                    ]
                ),
                '2009-11-29+30',
            ),
            (
                iter(
                    [
                        datetime(2009, 11, 29, tzinfo=UTC),
                        datetime(2009, 11, 29, tzinfo=UTC),
                        datetime(2009, 11, 30, tzinfo=UTC),
                        datetime(2009, 12, 1, tzinfo=UTC),
                        datetime(2009, 12, 2, tzinfo=UTC),
                    ]
                ),
                '2009-11-29+30+12-01+02',
            ),
            (
                iter(
                    [
                        datetime(2009, 12, 31, tzinfo=UTC),
                        datetime(2010, 1, 1, tzinfo=UTC),
                    ]
                ),
                '2009-12-31+2010-01-01',
            ),
        ]:
            with self.subTest(datetimes=datetimes, expected=expected):
                actual = get_common_prefix(datetimes)
                self.assertEqual(expected, actual)
