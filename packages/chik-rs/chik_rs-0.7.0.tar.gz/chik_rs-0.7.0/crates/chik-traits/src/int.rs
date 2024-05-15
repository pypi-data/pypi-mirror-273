use pyo3::types::{PyAny, PyBool, PyList, PyModule, PyString, PyTuple};
use pyo3::{IntoPy, PyResult, Python};

/// A custom to-python conversion trait that turns primitive integer types into
/// the chik-blockchain fixed-width integer types (uint8, int8, etc.)
pub trait ChikToPython {
    fn to_python<'a>(&self, py: pyo3::Python<'a>) -> pyo3::PyResult<&'a pyo3::types::PyAny>;
}

macro_rules! primitive_int {
    ($t:ty, $name:expr) => {
        impl ChikToPython for $t {
            fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
                let int_module = PyModule::import(py, "chik_rs.sized_ints")?;
                let ty = int_module.getattr($name)?;
                ty.call1((self.into_py(py),))
            }
        }
    };
}

primitive_int!(i8, "int8");
primitive_int!(u8, "uint8");
primitive_int!(i16, "int16");
primitive_int!(u16, "uint16");
primitive_int!(i32, "int32");
primitive_int!(u32, "uint32");
primitive_int!(i64, "int64");
primitive_int!(u64, "uint64");
primitive_int!(i128, "int128");
primitive_int!(u128, "uint128");

impl<T: ChikToPython> ChikToPython for Option<T> {
    fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        match &self {
            Some(v) => v.to_python(py),
            None => Ok(py.None().into_ref(py)),
        }
    }
}

impl<T: ChikToPython> ChikToPython for Vec<T> {
    fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        let ret = PyList::empty(py);
        for v in self {
            ret.append(v.to_python(py)?)?;
        }
        Ok(ret)
    }
}

impl ChikToPython for bool {
    fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        Ok(PyBool::new(py, *self))
    }
}

impl ChikToPython for String {
    fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        Ok(PyString::new(py, self.as_str()))
    }
}

impl<T: ChikToPython, U: ChikToPython> ChikToPython for (T, U) {
    fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        Ok(PyTuple::new(
            py,
            [self.0.to_python(py)?, self.1.to_python(py)?],
        ))
    }
}

impl<T: ChikToPython, U: ChikToPython, V: ChikToPython> ChikToPython for (T, U, V) {
    fn to_python<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        Ok(PyTuple::new(
            py,
            [
                self.0.to_python(py)?,
                self.1.to_python(py)?,
                self.2.to_python(py)?,
            ],
        ))
    }
}
