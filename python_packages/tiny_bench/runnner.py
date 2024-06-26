import gc

from python_packages.chrono import TimeSpan
from python_packages.chrono import MonotonicChronograph

from typing import Callable, Any, List, Tuple


def run_benchmark(bench: Callable[[], Any], category: str, iteration: int) -> List[Tuple[str, 'TimeSpan']]:
    result = []

    if iteration <= 0:
        raise ValueError(f'{iteration} is unexpected')
    chrono = MonotonicChronograph()

    for i in range(iteration):
        gc.collect()
        chrono.restart()
        bench()
        ret = chrono.stop()
        print(f'{i} {category} {ret.elapsed.total_milli_seconds()}')
        result.append((category, ret.elapsed))

    return result
