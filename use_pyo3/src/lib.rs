use numpy::PyReadonlyArrayDyn;
use pyo3::prelude::*;

#[pyfunction]
fn sum<'py>(_py: Python<'py>, arr: PyReadonlyArrayDyn<'py, i64>) -> i64 {
    let view = arr.as_array();
    let mut accum = 0i64;

    for elem in view.iter() {
        accum += elem
    }

    accum
}
#[pyfunction]
fn add(x: i64, y: i64) -> i64 {
    x + y
}

#[pyfunction]
fn sub(x: i64, y: i64) -> i64 {
    x - y
}

#[pyfunction]
fn answer() -> i32 {
    42
}

#[pymodule]
fn use_pyo3(m: &Bound<'_, PyModule>) -> PyResult<()> {
    println!("called");

    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(sub, m)?)?;
    m.add_function(wrap_pyfunction!(answer, m)?)?;
    m.add_function(wrap_pyfunction!(sum, m)?)?;

    Ok(())
}
