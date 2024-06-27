import platform
from python_packages.chrono import from_seconds, from_milli_seconds, TimeSpan
from python_packages.tiny_bench import run_autofit_benchmark, BenchmarkResult
import bench.scalar_bench as sb


def add(x: int, y: int) -> int:
    return x + y


def bench(cnt: int) -> int:
    accum = 0

    for i in range(cnt):
        accum = add(i, accum)

    return accum


def main():
    sb.run_bench()


if __name__ == "__main__":
    main()
