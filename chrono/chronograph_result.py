from dataclasses import dataclass
from .chronograph_status import Status
from .timespan import TimeSpan


@dataclass(frozen=True)
class Result:
    recent: Status
    current: Status
    elapsed: TimeSpan
