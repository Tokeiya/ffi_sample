use pyo3::prelude::*;

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

    Ok(())
}
