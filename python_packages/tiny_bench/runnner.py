import gc

from python_packages.chrono import TimeSpan, from_seconds, from_milli_seconds
from python_packages.chrono import MonotonicChronograph

from typing import Callable, Any, List, Tuple
import math
from .benchmark_result import BenchmarkResult


def run_benchmark(bench: Callable[[], Any], category: str, iteration: int, n: int) -> List['BenchmarkResult']:
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
        result.append(BenchmarkResult(category, n, ret.elapsed))

    return result


def measurement(target: Callable[[int], Any], threshold: 'TimeSpan') -> int:
    pre_threshold = from_milli_seconds(100)
    iteration: int = 1
    chrono = MonotonicChronograph()
    elapsed = TimeSpan(0)
    flg = False

    for i in range(100):
        chrono.restart()
        target(iteration)
        elapsed = chrono.stop().elapsed

        print(f'iteration:{iteration} elapsed:{elapsed.total_milli_seconds()} ms')
        if elapsed >= pre_threshold:
            flg = True
            break

        iteration = math.ceil(iteration * 1.5)

    if not flg:
        raise RuntimeWarning('No solution')

    flg = False
    per = elapsed / iteration
    iteration = int(threshold / per)

    inclement = int(iteration / 100) + 1

    for i in range(100):
        chrono.restart()
        target(iteration)
        elapsed = chrono.stop().elapsed
        print(f'iteration:{iteration} elapsed:{elapsed.total_milli_seconds()} ms')
        if elapsed >= threshold:
            flg = True
            break

        inclement += inclement

    if not flg:
        raise RuntimeWarning('No solution')
    return iteration


def run_autofit_benchmark(target: Callable[[int], Any],
                          threshold: 'TimeSpan', env: str, category: str, iteration: int) \
        -> List[Tuple[str, str, int, 'TimeSpan']]:
    cnt = measurement(target, threshold)

    result = []

    chrono = MonotonicChronograph()

    for i in range(iteration):
        chrono.restart()
        target(cnt)
        elapsed = chrono.stop().elapsed
        print(f'{i} {cnt} {env} {category} {elapsed.total_milli_seconds()}')

        result.append((env, category, cnt, elapsed))

    return result
