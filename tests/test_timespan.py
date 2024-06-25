import pytest
from chrono.timespan import TimeSpan
from random import randint
from dataclasses import dataclass


@dataclass(frozen=True)
class Sample:
    fixture: TimeSpan
    is_negative: bool
    nano: int
    micro: int
    milli: int
    sec: int
    minutes: int
    hour: int

    def total_nano_seconds(self) -> int:
        tmp = (self.nano + self.micro * 1_000 + self.milli * 1_000_000
               + self.sec * 1_000_000_000 + self.minutes * 60_000_000_000 + self.hour * 3_600_000_000_000)

        return -tmp if self.is_negative else tmp

    def total_micro_seconds(self) -> float:
        return self.total_nano_seconds() / 1_000

    def total_milli_seconds(self) -> float:
        return self.total_nano_seconds() / 1_000_000

    def total_seconds(self) -> float:
        return self.total_nano_seconds() / 1_000_000_000

    def total_minutes(self) -> float:
        return self.total_nano_seconds() / 60_000_000_000

    def total_hours(self) -> float:
        return self.total_nano_seconds() / 3_600_000_000_000


class TestTimeSpan:
    @pytest.fixture
    def random_positive_sample(self) -> Sample:
        nano = 82
        micro = 679
        milli = 394
        sec = 12
        minutes = 45
        hour = 42

        total_nano = (nano + micro * 1_000 + milli * 1_000_000 + sec * 1_000_000_000
                      + minutes * 60_000_000_000 + hour * 3_600_000_000_000)

        fixture = TimeSpan(total_nano)
        return Sample(fixture, False, nano, micro, milli, sec, minutes, hour)

    @pytest.fixture
    def random_negative_sample(self) -> Sample:
        nano = 488
        micro = 825
        milli = 437
        sec = 59
        minutes = 44
        hour = 88

        total_nano = -(nano + micro * 1_000 + milli * 1_000_000 + sec * 1_000_000_000
                       + minutes * 60_000_000_000 + hour * 3_600_000_000_000)
        fixture = TimeSpan(total_nano)
        return Sample(fixture, True, nano, micro, milli, sec, minutes, hour)

    @pytest.fixture
    def large(self) -> (TimeSpan, int):
        return TimeSpan(1_000), 1_000

    @pytest.fixture
    def small(self) -> (TimeSpan, int):
        return TimeSpan(100), 100

    def test_is_negative(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.is_negative() is False
        assert random_negative_sample.fixture.is_negative() is True
        assert random_positive_sample.is_negative is False
        assert random_negative_sample.is_negative is True

    def test_total_nano_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.total_nano_seconds() == random_positive_sample.total_nano_seconds()
        assert random_negative_sample.fixture.total_nano_seconds() == random_negative_sample.total_nano_seconds()

    def test_total_micro_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.total_micro_seconds() == random_positive_sample.total_micro_seconds()
        assert random_negative_sample.fixture.total_micro_seconds() == random_negative_sample.total_micro_seconds()

    def test_total_milli_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.total_milli_seconds() == random_positive_sample.total_milli_seconds()
        assert random_negative_sample.fixture.total_milli_seconds() == random_negative_sample.total_milli_seconds()

    def test_total_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.total_seconds() == random_positive_sample.total_seconds()
        assert random_negative_sample.fixture.total_seconds() == random_negative_sample.total_seconds()

    def test_total_minutes(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.total_minutes() == random_positive_sample.total_minutes()
        assert random_negative_sample.fixture.total_minutes() == random_negative_sample.total_minutes()

    def test_total_hours(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.total_hours() == random_positive_sample.total_hours()
        assert random_negative_sample.fixture.total_hours() == random_negative_sample.total_hours()

    def test_nano_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert -random_negative_sample.fixture.nano_seconds() == random_negative_sample.nano
        assert random_positive_sample.fixture.nano_seconds() == random_positive_sample.nano

    def test_micro_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert -random_negative_sample.fixture.micro_seconds() == random_negative_sample.micro
        assert random_positive_sample.fixture.micro_seconds() == random_positive_sample.micro

    def test_milli_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.milli_seconds() == random_positive_sample.milli
        assert -random_negative_sample.fixture.milli_seconds() == random_negative_sample.milli

    def test_seconds(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.seconds() == random_positive_sample.sec
        assert -random_negative_sample.fixture.seconds() == random_negative_sample.sec

    def test_minutes(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.minutes() == random_positive_sample.minutes
        assert -random_negative_sample.fixture.minutes() == random_negative_sample.minutes

    def test_hours(self, random_positive_sample: Sample, random_negative_sample: Sample):
        assert random_positive_sample.fixture.hours() == random_positive_sample.hour
        assert -random_negative_sample.fixture.hours() == random_negative_sample.hour

    def test_add(self):
        x = TimeSpan(1_000)
        y = TimeSpan(500)
        assert (x + y).total_nano_seconds() == 1_500
        assert (y + x).total_nano_seconds() == 1_500

        y = TimeSpan(-500)
        assert (x + y).total_nano_seconds() == 500
        assert (y + x).total_nano_seconds() == 500

    def test_sub(self):
        x = TimeSpan(1_000)
        y = TimeSpan(500)
        assert (x - y).total_nano_seconds() == 500
        assert (y - x).total_nano_seconds() == -500

        y = TimeSpan(-500)
        assert (x - y).total_nano_seconds() == 1_500
        assert (y - x).total_nano_seconds() == -1_500

    def test_eq(self):
        x = TimeSpan(1_000)
        y = TimeSpan(1_000)
        z = TimeSpan(1_000)
        other = TimeSpan(500)

        assert x == y
        assert y == z
        assert z == x
        assert x == x

        assert not (x == other)

    def test_ne(self):
        x = TimeSpan(1_000)
        y = TimeSpan(1_000)
        z = TimeSpan(500)

        assert x != z
        assert y != z
        assert not (x != y)

    def test_lt(self):
        x = TimeSpan(1_000)
        y = TimeSpan(1_000)
        z = TimeSpan(500)

        assert not (x < y)
        assert not (y < x)
        assert not (x < z)
        assert not (x < x)
        assert (z < x)

    def test_le(self):
        x = TimeSpan(1_000)
        y = TimeSpan(1_000)
        z = TimeSpan(500)

        assert (x <= y)
        assert (y <= x)
        assert not (x <= z)
        assert (x <= x)
        assert (z <= x)

    def test_gt(self):
        x = TimeSpan(1_000)
        y = TimeSpan(1_000)
        z = TimeSpan(500)

        assert not (x > y)
        assert not (y > x)
        assert (x > z)
        assert not (x > x)
        assert not (z > x)

    def test_ge(self):
        x = TimeSpan(1_000)
        y = TimeSpan(1_000)
        z = TimeSpan(500)

        assert (x >= y)
        assert (y >= x)
        assert (x >= z)
        assert (x >= x)
        assert not (z >= x)

    def test_copy(self):
        x = TimeSpan(500)
        y = x.copy()

        x._nano = 0
        assert x.total_nano_seconds() == 0
        assert y.total_nano_seconds() == 500
