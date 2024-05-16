

use pyo3::prelude::*;
use pyo3::exceptions::{PyFileNotFoundError, PyValueError};
use std::collections::HashSet;
use html_escape::decode_html_entities;
use std::path::Path;
use csv::ReaderBuilder;
use xlsxwriter::Workbook;
use regex::Regex;
use lazy_static::lazy_static;


lazy_static! {
    static ref LT_GT_PATTERN: Regex = Regex::new(
        r"(?x)
        (?P<start>^|\s|>)
        (?P<symbol>[<>])
        (?P<matched_char>[^\s/>])
        "
    ).unwrap();
}

#[pyfunction]
fn combine_dedupe_values(values: Vec<&str>, separator: &str) -> String {
    let mut output: HashSet<&str> = HashSet::new();

    for value in values {
        let terms: HashSet<&str> = value.split(separator).collect();
        output.extend(terms);
    }

    let mut sorted_output: Vec<&str> = output.into_iter().collect();
    sorted_output.sort();

    sorted_output.join(", ")
}


#[pyfunction]
fn fix_lt_gt(value: &str) -> PyResult<String> {
    Ok(LT_GT_PATTERN.replace_all(value, "$start$symbol $matched_char").into_owned())
}

#[pyfunction]
fn unescape_html_chars(value: &str) -> PyResult<String> {
    Ok(decode_html_entities(value).into_owned())
}


lazy_static! {
    static ref TEMPERATURE_PATTERN: Regex = Regex::new(
        r"(?i)(-?\d+\.?\d*)(\s*[^°]C)"
    ).unwrap();
}


#[pyfunction]
fn clean_temperature(value: &str) -> PyResult<String> {
    let value = TEMPERATURE_PATTERN.replace_all(value, "$1°C");
    Ok(value.replace("℃", "°C"))
}

lazy_static! {
    static ref CHINESE_CHARS: Regex = Regex::new(r"[\p{Script=Han}]").unwrap();
}

#[pyfunction]
fn remove_chinese_chars(value: &str) -> PyResult<String> {
    Ok(CHINESE_CHARS.replace_all(value, "").to_string())
}

lazy_static! {
    static ref HTML_PATTERN: Regex = Regex::new(r"<.*?>").unwrap();
}

#[pyfunction]
fn strip_html_tags(value: &str) -> PyResult<String> {
    let result = HTML_PATTERN.replace_all(value, "");
    Ok(result.to_string())
}

lazy_static! {
    static ref FORMULA_PATTERN: Regex = Regex::new(r"([A-Za-z])(\d+)").unwrap();
}

#[pyfunction]
fn add_chemical_formula_subscript(value: &str) -> PyResult<String> {
    let result = FORMULA_PATTERN.replace_all(value, r"$1<sub>$2</sub>");
    Ok(result.to_string())
}

/// Convert a CSV file to an Excel file.
///
/// # Panics
///
/// Panics if the CSV file does not exist or if the file is not a CSV file.
///
/// # Errors
///
/// This function will return an error if the CSV file does not exist or if the file is not a CSV file.
#[pyfunction]
fn convert_to_xlsx(csv_path: &str) -> PyResult<()> {
    // Convert the str path to a path object
    let csv_path = Path::new(csv_path);

    if !csv_path.exists() {
        // Raise a Python FileNotFoundError exception
        let error_message = format!("File not found: {}", csv_path.display());
        let error = PyFileNotFoundError::new_err(error_message);
        return Err(error);
    }

    if csv_path.extension() != Some("csv".as_ref()) {
        // Raise a Python ValueError exception
        let error_message = format!("File is not a CSV file: {}", csv_path.display());
        let error = PyValueError::new_err(error_message);
        return Err(error);
    }

    // Setting up Excel file
    let xlsx_path = csv_path.with_extension("xlsx");
    let workbook = Workbook::new(&xlsx_path.to_str().unwrap()).unwrap();
    let mut sheet = workbook.add_worksheet(Some("data")).unwrap();

    // Reading CSV file and writing to Excel file
    let mut csv_reader = ReaderBuilder::new()
        .has_headers(false)
        .flexible(true)
        .from_path(csv_path).unwrap();
    for (row_number, row) in csv_reader.records().enumerate() {
        let row_data = row.unwrap();
        for (column, cell) in row_data.iter().enumerate() {
            sheet.write_string(row_number as u32, column as u16, cell, None).unwrap();
        }
    }

    // Finishing up
    workbook.close().unwrap();

    Ok(())
}


/// A Python module implemented in Rust.
#[pymodule]
fn tdi_rust_python_tools(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(combine_dedupe_values, m)?)?;
    m.add_function(wrap_pyfunction!(fix_lt_gt, m)?)?;
    m.add_function(wrap_pyfunction!(unescape_html_chars, m)?)?;
    m.add_function(wrap_pyfunction!(clean_temperature, m)?)?;
    m.add_function(wrap_pyfunction!(remove_chinese_chars, m)?)?;
    m.add_function(wrap_pyfunction!(strip_html_tags, m)?)?;
    m.add_function(wrap_pyfunction!(add_chemical_formula_subscript, m)?)?;
    m.add_function(wrap_pyfunction!(convert_to_xlsx, m)?)?;
    Ok(())
}
