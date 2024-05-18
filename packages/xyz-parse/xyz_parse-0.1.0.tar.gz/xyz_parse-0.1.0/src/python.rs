use crate::{atom::Atom, molecule::Molecule, xyz::Xyz};
use pyo3::{create_exception, exceptions::PyException, prelude::*, types::PyType};
use rust_decimal::Decimal;
use std::borrow::Cow;

create_exception!(xyz_parse, ParseError, PyException);

#[pymodule]
fn xyz_parse(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("ParseError", m.py().get_type_bound::<ParseError>())?;
    m.add_class::<PyAtom>()?;
    m.add_class::<PyMolecule>()?;
    m.add_class::<PyXyz>()?;
    m.add_function(wrap_pyfunction!(parse_xyz, m)?)?;
    Ok(())
}

#[pyclass(name = "Atom", module = "xyz_parse")]
#[derive(Debug, Clone)]
pub struct PyAtom(Atom<'static>);

#[pymethods]
impl PyAtom {
    #[new]
    fn new(symbol: String, x: Decimal, y: Decimal, z: Decimal) -> Self {
        PyAtom(Atom {
            symbol: Cow::Owned(symbol),
            x,
            y,
            z,
        })
    }

    #[classmethod]
    fn parse(_: &Bound<'_, PyType>, input: &str) -> PyResult<PyAtom> {
        Atom::parse(input)
            .map(|atom| PyAtom(atom.into_owned()))
            .map_err(|err| ParseError::new_err(err.to_string()))
    }

    #[getter]
    fn get_symbol(&self) -> Cow<'_, str> {
        self.0.symbol.clone()
    }

    #[setter]
    fn set_symbol(&mut self, symbol: String) {
        self.0.symbol = Cow::Owned(symbol);
    }

    #[getter]
    fn get_x(&self) -> Decimal {
        self.0.x
    }

    #[setter]
    fn set_x(&mut self, decimal: Decimal) {
        self.0.x = decimal;
    }

    #[getter]
    fn get_y(&self) -> Decimal {
        self.0.y
    }

    #[setter]
    fn set_y(&mut self, decimal: Decimal) {
        self.0.y = decimal;
    }

    #[getter]
    fn get_z(&self) -> Decimal {
        self.0.z
    }

    #[setter]
    fn set_z(&mut self, decimal: Decimal) {
        self.0.z = decimal;
    }

    #[getter]
    fn coordinates(&self) -> (Decimal, Decimal, Decimal) {
        (self.0.x, self.0.y, self.0.z)
    }

    fn __str__(&self) -> String {
        self.0.to_string()
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(name = "Molecule", module = "xyz_parse")]
#[derive(Debug, Clone)]
pub struct PyMolecule(Molecule<'static>);

#[pymethods]
impl PyMolecule {
    #[new]
    fn new(comment: String, atoms: Vec<PyAtom>) -> Self {
        PyMolecule(Molecule {
            comment: Cow::Owned(comment),
            atoms: atoms.into_iter().map(|atom| atom.0).collect(),
        })
    }

    #[classmethod]
    fn parse(_: &Bound<'_, PyType>, input: &str) -> PyResult<PyMolecule> {
        Molecule::parse(input)
            .map(|molecule| PyMolecule(molecule.into_owned()))
            .map_err(|err| ParseError::new_err(err.to_string()))
    }

    #[getter]
    fn get_comment(&self) -> Cow<'static, str> {
        self.0.comment.clone()
    }

    #[setter]
    fn set_comment(&mut self, comment: String) {
        self.0.comment = Cow::Owned(comment);
    }

    #[getter]
    fn get_atoms(&self) -> Vec<PyAtom> {
        self.0
            .atoms
            .iter()
            .map(|atom| PyAtom(atom.clone()))
            .collect()
    }

    #[setter]
    fn set_atoms(&mut self, atoms: Vec<PyAtom>) {
        self.0.atoms = atoms.into_iter().map(|atom| atom.0).collect();
    }

    fn __str__(&self) -> String {
        self.0.to_string()
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(name = "Xyz", module = "xyz_parse")]
#[derive(Debug, Clone)]
pub struct PyXyz(Xyz<'static>);

#[pymethods]
impl PyXyz {
    #[new]
    fn new(molecules: Vec<PyMolecule>) -> Self {
        PyXyz(Xyz {
            molecules: molecules.into_iter().map(|molecule| molecule.0).collect(),
        })
    }

    #[classmethod]
    fn parse(_: &Bound<'_, PyType>, input: &str) -> PyResult<PyXyz> {
        Xyz::parse(input)
            .map(|xyz| PyXyz(xyz.into_owned()))
            .map_err(|err| ParseError::new_err(err.to_string()))
    }

    #[getter]
    fn get_molecules(&self) -> Vec<PyMolecule> {
        self.0
            .molecules
            .iter()
            .map(|molecule| PyMolecule(molecule.clone()))
            .collect()
    }

    #[setter]
    fn set_molecules(&mut self, molecules: Vec<PyMolecule>) {
        self.0.molecules = molecules.into_iter().map(|molecule| molecule.0).collect();
    }

    fn __str__(&self) -> String {
        self.0.to_string()
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyfunction]
fn parse_xyz(input: &str) -> PyResult<PyXyz> {
    Xyz::parse(input)
        .map(|xyz| PyXyz(xyz.into_owned()))
        .map_err(|err| ParseError::new_err(err.to_string()))
}
