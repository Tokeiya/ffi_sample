import platform
from python_packages.chrono import TimeSpan
from dataclasses import dataclass
from typing import List

OS = platform.system()
ARCHITECTURE = platform.machine()
ENV = platform.architecture()[0]

RESULT_HEADER: List[str] = [
    'count',
    'os',
    'arch',
    'env',
    'category',
    'iteration',
    'elapse',
    'elapse_ns',
    'per_iteration_ns'
]


@dataclass
class BenchmarkResult:
    count: int
    category: str
    iteration: int
    elapsed: 'TimeSpan'
    os: str = OS
    arch: str = ARCHITECTURE
    env: str = ENV

    def to_string(self, delimiter: str):
        return delimiter.join([
            str(self.count),
            self.os,
            self.arch,
            self.env,
            self.category,
            str(self.iteration),
            str(self.elapsed),
            str(self.elapsed.total_nano_seconds()),
            str(self.elapsed.total_nano_seconds() / self.iteration)
        ])
