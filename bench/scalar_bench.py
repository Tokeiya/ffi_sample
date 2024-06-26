from python_packages.tiny_bench import runnner

from ctypes import cdll, c_int
import use_pyo3

ITERATION = 5_000_000


def native_add(x: int, y: int) -> int:
    return x + y


def use_pyo3_add() -> int:
    accum = 0
    for i in range(ITERATION):
        accum = use_pyo3.add(accum, i)

    return accum


def call_native() -> int:
    accum = 0
    for i in range(ITERATION):
        accum = native_add(accum, i)
    return accum


def non_call() -> int:
    accum = 0
    for i in range(ITERATION):
        accum = accum + i
    return accum


def ffi_call() -> int:
    rustlib = cdll.LoadLibrary('./artifacts/primitive_ffi.dll')
    rustlib.add.argtypes = (c_int, c_int)
    rustlib.add.restype = c_int

    accum = 0

    for i in range(ITERATION):
        accum = rustlib.add(accum, i)

    return accum


def run_bench():
    runnner.run_benchmark(lambda: use_pyo3_add(), 'use_pyo3', 10)
    runnner.run_benchmark(lambda: call_native(), 'call_native', 10)
    runnner.run_benchmark(lambda: ffi_call(), 'ffi_call', 10)
