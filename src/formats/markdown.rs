use pandoc::{OutputFormat, OutputKind, Pandoc};

pub fn markdown_to_html() {}

fn create_pandoc() -> Pandoc {
    let output = pandoc::new();

    pandoc.add_option(pandoc::PandocOption::MathML(Option::None));

    //pandoc.add_filter(filter);

    pandoc.set_output_format(OutputFormat::Html, vec![]);
    return output;
}
