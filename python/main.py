import ctypes
from time import monotonic_ns

import use_pyo3
from random import randint


def main():
    print(monotonic_ns())


if __name__ == "__main__":
    main()
