use crate::engine::Rule;
use pest::error::Error as PestError;
use std::io::Error as IOError;

#[derive(Debug)]
pub enum TemplateFileParseError {
    IOError(IOError),
    ParseError(PestError<Rule>),
}

impl From<TemplateParseError> for TemplateFileParseError {
    fn from(error: TemplateParseError) -> Self {
        match error {
            TemplateParseError::ParseError(e) => TemplateFileParseError::ParseError(e),
        }
    }
}

#[derive(Debug)]
pub enum TemplateParseError {
    ParseError(PestError<Rule>),
}
