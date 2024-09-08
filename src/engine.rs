use crate::error::{TemplateFileParseError, TemplateParseError};
use pest::Parser;
use pest_derive::Parser;
use std::fmt;
use std::fs;
use std::path::Path;

#[derive(Parser)]
#[grammar = "grammars/template.pest"] // relative to src
struct TemplateParser;

pub struct Template {}

impl Template {
    fn new() -> Template {
        Template {}
    }

    pub fn from_file(input: &Path) -> Result<Template, TemplateFileParseError> {
        let res = fs::read_to_string(input);
        let src: String;
        match res {
            Result::Ok(str) => src = str,
            Result::Err(err) => {
                println!("{:?}", err);
                let wrapped_err = TemplateFileParseError::IOError(err);
                return Result::Err(wrapped_err);
            }
        }
        let res = Template::from_str(&src);
        match res {
            Result::Ok(template) => return Result::Ok(template),
            Result::Err(err) => return Result::Err(TemplateFileParseError::from(err)),
        }
    }

    fn from_str(input: &str) -> Result<Template, TemplateParseError> {
        let res = TemplateParser::parse(Rule::root, &input);
        match res {
            Result::Ok(res) => println!("{:?}", res),
            Result::Err(err) => {
                println!("{:?}", err);
                let wrapped_err = TemplateParseError::ParseError(err);
                return Result::Err(wrapped_err);
            }
        }
        let output = Template {};
        return Result::Ok(output);
    }
}

#[derive(Debug)]
pub enum Data {
    Number(i32),
    Boolean(bool),
    Text(String),
    Array(Vec<Data>),
}

impl fmt::Display for Data {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Text(x) => write!(f, "{}", x),
            Self::Number(x) => write!(f, "{}", x),
            Self::Boolean(x) => write!(f, "{}", x),
            Self::Array(x) => write!(f, "{:?}", x),
        }
    }
}
