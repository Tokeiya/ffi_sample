from typing import Union


def from_seconds(value: float) -> 'TimeSpan':
    nano = int(value * 1_000_000_000)
    return TimeSpan(nano)


def from_milli_seconds(value: float) -> 'TimeSpan':
    nano = int(value * 1_000_000)
    return TimeSpan(nano)


class TimeSpan:
    _nano: int

    def __init__(self, value: int):
        self._nano = value

    def is_negative(self) -> bool:
        return self._nano < 0

    def total_nano_seconds(self) -> int:
        return self._nano

    def total_micro_seconds(self) -> float:
        return self._nano / 1_000

    def total_milli_seconds(self) -> float:
        return self._nano / 1_000_000

    def total_seconds(self) -> float:
        return self._nano / 1_000_000_000

    def total_minutes(self) -> float:
        return self._nano / 60_000_000_000

    def total_hours(self) -> float:
        return self._nano / 3_600_000_000_000

    def nano_seconds(self) -> int:
        piv = abs(self._nano)
        tmp = piv - ((piv // 1_000) * 1_000)
        return -tmp if self.is_negative() else tmp

    def micro_seconds(self) -> int:
        piv = abs(self._nano) // 1_000
        tmp = piv - ((piv // 1_000) * 1_000)
        return -tmp if self.is_negative() else tmp

    def milli_seconds(self) -> int:
        piv = abs(self._nano) // 1_000_000
        tmp = piv - ((piv // 1_000) * 1_000)
        return -tmp if self.is_negative() else tmp

    def seconds(self) -> int:
        sec = abs(self._nano) // 1_000_000_000
        tmp = sec - ((sec // 60) * 60)
        return -tmp if self.is_negative() else tmp

    def minutes(self) -> int:
        minutes = abs(self._nano) // 60_000_000_000
        tmp = minutes - ((minutes // 60) * 60)
        return -tmp if self.is_negative() else tmp

    def hours(self) -> int:
        hours = abs(self._nano) // 3_600_000_000_000
        return -hours if self.is_negative() else hours

    def copy(self) -> 'TimeSpan':
        return TimeSpan(self._nano)

    def __add__(self, other: 'TimeSpan') -> 'TimeSpan':
        return TimeSpan(self._nano + other._nano)

    def __sub__(self, other: 'TimeSpan') -> 'TimeSpan':
        return TimeSpan(self._nano - other._nano)

    def __mul__(self, other: float) -> 'TimeSpan':
        return TimeSpan(int(self._nano * other))

    def __truediv__(self, other: Union[float, 'TimeSpan']) -> Union[float, 'TimeSpan']:
        if isinstance(other, float):
            return TimeSpan(int(self._nano / other))
        elif isinstance(other, int):
            return TimeSpan(int(self._nano / other))
        elif isinstance(other, TimeSpan):
            return self._nano / other._nano
        else:
            raise TypeError

    def __eq__(self, other: 'TimeSpan') -> bool:
        return self._nano == other._nano

    def __ne__(self, other: 'TimeSpan') -> bool:
        return self._nano != other._nano

    def __lt__(self, other: 'TimeSpan') -> bool:
        return self._nano < other._nano

    def __le__(self, other: 'TimeSpan') -> bool:
        return self._nano <= other._nano

    def __gt__(self, other: 'TimeSpan') -> bool:
        return self._nano > other._nano

    def __ge__(self, other: 'TimeSpan') -> bool:
        return self._nano >= other._nano
