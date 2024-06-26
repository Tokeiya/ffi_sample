import platform
from python_packages.chrono import from_seconds, from_milli_seconds, TimeSpan


def add(x: int, y: int) -> int:
    return x + y


def bench(cnt: int) -> int:
    accum = 0

    for i in range(cnt):
        accum = add(i, accum)

    return accum


def main():
    print(from_milli_seconds(500))
    print(from_seconds(2000))


if __name__ == "__main__":
    main()
