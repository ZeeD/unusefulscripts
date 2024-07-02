from collections.abc import Iterator
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from unittest import TestCase

from clocks import clocks


def times(
    start: str, end: str, delta: timedelta = timedelta(minutes=1)
) -> Iterator[time]:
    d = date.fromordinal(1)

    start_dt = datetime.combine(d, time.fromisoformat(start))
    end_dt = datetime.combine(d, time.fromisoformat(end))

    tmp = start_dt
    while tmp < end_dt:
        yield tmp.time()
        tmp += delta


class TestClocks(TestCase):
    def test_oclock(self) -> None:
        for time_string_am, time_string_pm, expected in [
            ('00:00', '12:00', '🕛'),
            ('00:30', '12:30', '🕧'),
            ('01:00', '13:00', '🕐'),
            ('01:30', '13:30', '🕜'),
            ('02:00', '14:00', '🕑'),
            ('02:30', '14:30', '🕝'),
            ('03:00', '15:00', '🕒'),
            ('03:30', '15:30', '🕞'),
            ('04:00', '16:00', '🕓'),
            ('04:30', '16:30', '🕟'),
            ('05:00', '17:00', '🕔'),
            ('05:30', '17:30', '🕠'),
            ('06:00', '18:00', '🕕'),
            ('06:30', '18:30', '🕡'),
            ('07:00', '19:00', '🕖'),
            ('07:30', '19:30', '🕢'),
            ('08:00', '20:00', '🕗'),
            ('08:30', '20:30', '🕣'),
            ('09:00', '21:00', '🕘'),
            ('09:30', '21:30', '🕤'),
            ('10:00', '22:00', '🕙'),
            ('10:30', '22:30', '🕥'),
            ('11:00', '23:00', '🕚'),
            ('11:30', '23:30', '🕦'),
        ]:
            with self.subTest(time_string=time_string_am, expected=expected):
                actual = clocks(time.fromisoformat(time_string_am))
                self.assertEqual(expected, actual)
            with self.subTest(time_string=time_string_pm, expected=expected):
                actual = clocks(time.fromisoformat(time_string_pm))
                self.assertEqual(expected, actual)

    def test_range_45_15(self) -> None:
        expected = '🕛'
        for time_ in times('11:45:00', '12:14:59'):
            with self.subTest(time_=time_):
                actual = clocks(time_)
                self.assertEqual(expected, actual)

    def test_range_15_45(self) -> None:
        expected = '🕦'
        for time_ in times('11:15:00', '11:44:59'):
            with self.subTest(time_=time_):
                actual = clocks(time_)
                self.assertEqual(expected, actual)
