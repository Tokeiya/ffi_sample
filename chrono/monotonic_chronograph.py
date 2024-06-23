from timespan import TimeSpan
from chronograph_status import Status
from .chronograph_result import Result


class MonotonicChronograph:
    def __init__(self):
        raise NotImplementedError

    def status(self) -> Status:
        raise NotImplementedError

    def start(self) -> Result:
        raise NotImplementedError

    def stop(self) -> Result:
        raise NotImplementedError

    def restart(self) -> Result:
        raise NotImplementedError

    def reset(self) -> Result:
        raise NotImplementedError

    def elapsed(self) -> Result:
        raise NotImplementedError
