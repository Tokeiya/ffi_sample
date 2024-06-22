import ctypes
import use_pyo3


def main():
    lib = ctypes.CDLL('../artifacts/primiive_ffi.dll')
    lib.add.argtypes = (ctypes.c_int, ctypes.c_int)
    lib.add.restype = ctypes.c_int

    result = lib.add(3, 4)
    print(f"Result of add(3, 4): {result}")

    print(use_pyo3.sub(20, 10))
    print(use_pyo3.answer())
    

if __name__ == "__main__":
    main()
