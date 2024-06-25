from dataclasses import dataclass
from .chronograph_status import Status
from .timespan import TimeSpan


@dataclass(frozen=True)
class Result:
    elapsed: TimeSpan
    recent: Status
    current: Status
