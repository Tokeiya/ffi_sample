import time

from .chronograph_result import Result
from .chronograph_status import Status
from .timespan import TimeSpan


class MonotonicChronograph:
    _pivot: int
    _current: Status
    _accum: TimeSpan

    def __init__(self):
        self._pivot = 0
        self._current = Status.RESET
        self._accum = TimeSpan(0)

    def status(self) -> Status:
        return self._current

    def start(self) -> Result:
        if self._current == Status.RUNNING:
            return self.elapsed()
        elif self._current == Status.STOPPED:
            self._current = Status.RUNNING
            self._pivot = time.monotonic_ns()
            return Result(self._accum, Status.STOPPED, Status.RUNNING)
        elif self._current == Status.RESET:
            self._current = Status.RUNNING
            self._pivot = time.monotonic_ns()
            return Result(TimeSpan(0), Status.RESET, Status.RUNNING)

    def stop(self) -> Result:
        recent = self._current

        if self._current == Status.RUNNING:
            self._accum = TimeSpan(time.monotonic_ns() - self._pivot) + self._accum
            self._pivot = 0
            self._current = Status.STOPPED
            return Result(self._accum.copy(), Status.RUNNING, Status.STOPPED)
        else:
            return self.elapsed()

    def restart(self) -> Result:
        recent = self.elapsed()

        self._accum = TimeSpan(0)
        self._current = Status.RUNNING
        self._pivot = time.monotonic_ns()

        return Result(recent.elapsed, recent.recent, Status.RUNNING)

    def reset(self) -> Result:
        recent = self.elapsed()

        self._accum = TimeSpan(0)
        self._pivot = 0
        self._current = Status.RESET

        return Result(recent.elapsed, recent.recent, self._current)

    def elapsed(self) -> Result:
        if self._current == Status.RESET:
            return Result(TimeSpan(0), Status.RESET, Status.RESET)

        elif self._current == Status.STOPPED:
            return Result(self._accum.copy(), Status.STOPPED, Status.STOPPED)

        elif self._current == Status.RUNNING:
            tmp = TimeSpan(time.monotonic_ns() - self._pivot) + self._accum
            return Result(tmp, Status.RUNNING, Status.RUNNING)

        else:
            raise NotImplementedError(f'{self._current} is unexpected')
