import platform
from python_packages.chrono import TimeSpan
from dataclasses import dataclass

OS = platform.system()
ARCHITECTURE = platform.machine()
ENV = platform.architecture()[0]


@dataclass
class BenchmarkResult:
    category: str
    iteration: int
    elapsed: 'TimeSpan'
    os: str = OS
    arch: str = ARCHITECTURE
    env: str = ENV
