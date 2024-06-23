class TimeSpan:
    _nano: int

    def __init__(self, value: int):
        raise NotImplementedError()

    def is_negative(self) -> bool:
        raise NotImplementedError()

    def total_nano_seconds(self) -> float:
        raise NotImplementedError()

    def total_micro_seconds(self) -> float:
        raise NotImplementedError()

    def total_milli_seconds(self) -> float:
        raise NotImplementedError()

    def total_seconds(self) -> float:
        raise NotImplementedError()

    def total_minutes(self) -> float:
        raise NotImplementedError()

    def total_hours(self) -> float:
        raise NotImplementedError()

    def nano_seconds(self) -> int:
        raise NotImplementedError()

    def micro_seconds(self) -> int:
        raise NotImplementedError()

    def milli_seconds(self) -> int:
        raise NotImplementedError()

    def seconds(self) -> int:
        raise NotImplementedError()

    def minutes(self) -> int:
        raise NotImplementedError()

    def hours(self) -> int:
        raise NotImplementedError()

    def __add__(self, other: 'TimeSpan') -> 'TimeSpan':
        raise NotImplementedError()

    def __sub__(self, other: 'TimeSpan') -> 'TimeSpan':
        raise NotImplementedError()

    def __eq__(self, other: 'TimeSpan') -> bool:
        raise NotImplementedError()

    def __ne__(self, other: 'TimeSpan') -> bool:
        raise NotImplementedError()

    def __lt__(self, other: 'TimeSpan') -> bool:
        raise NotImplementedError()

    def __le__(self, other: 'TimeSpan') -> bool:
        raise NotImplementedError()

    def __gt__(self, other: 'TimeSpan') -> bool:
        raise NotImplementedError()

    def __ge__(self, other: 'TimeSpan') -> bool:
        raise NotImplementedError()
