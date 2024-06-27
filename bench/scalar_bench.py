from python_packages.tiny_bench import run_autofit_benchmark, BenchmarkResult
from python_packages.chrono import from_seconds
from ctypes import cdll, c_int
import use_pyo3


def native_add(x: int, y: int) -> int:
    return x + y


def use_pyo3_add(n: int) -> int:
    accum = 0
    for i in range(n):
        accum = use_pyo3.add(accum, i)

    return accum


def call_native(n: int) -> int:
    accum = 0
    for i in range(n):
        accum = native_add(accum, i)
    return accum


def non_call(n: int) -> int:
    accum = 0
    for i in range(n):
        accum = accum + i
    return accum


def ffi_call(n: int) -> int:
    rustlib = cdll.LoadLibrary('./artifacts/primitive_ffi.dll')
    rustlib.add.argtypes = (c_int, c_int)
    rustlib.add.restype = c_int

    accum = 0

    for i in range(n):
        accum = rustlib.add(accum, i)

    return accum


def run_bench():
    run_autofit_benchmark(lambda c: use_pyo3_add(c), from_seconds(1), 'use_pyo3', 10)
    run_autofit_benchmark(lambda c: call_native(c), from_seconds(1), 'call_native', 10)
    run_autofit_benchmark(lambda c: ffi_call(c), from_seconds(1), 'ffi_call', 10)
