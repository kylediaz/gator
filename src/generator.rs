use pandoc::{OutputFormat, OutputKind};
use std::path::{Path, PathBuf};
use walkdir::{DirEntry, WalkDir};
use yaml_rust2::YamlLoader;

use crate::engine::{Data, Template};
use crate::utils::ScopedEnv;

struct Context {
    vars: ScopedEnv<Data>,
    components: ScopedEnv<Template>,
}

pub fn generate(in_dir: &Path, out_dir: &Path) {
    let mut templates: ScopedEnv<Template> = ScopedEnv::new();
    let mut vars: ScopedEnv<String> = ScopedEnv::new();

    let metadata_dir_buf = Path::new(in_dir).join(".gator");
    let metadata_dir = metadata_dir_buf.as_path();
    process_metadata(metadata_dir, &mut templates, &mut vars);

    for entry in WalkDir::new(in_dir)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| is_valid_file(e))
    {
        let path = entry.path();

        if path.is_dir() {
            continue;
        }

        let file_name = entry.file_name().to_str().unwrap();
        let out_path_buff = out_dir.join(path);
        let out_path = out_path_buff.as_path();

        if file_name.ends_with(".html") {
            handle_html(&path, &out_path);
        } else if file_name.ends_with(".md") {
            handle_md(&path, &out_path);
        } else if file_name.ends_with(".ipynb") {
        } else {
        }

        println!("{:?}", path);
    }
}

fn is_valid_file(entry: &DirEntry) -> bool {
    entry
        .file_name()
        .to_str()
        .map(|s| !s.starts_with(".") && !s.starts_with("_"))
        .unwrap()
}

fn process_metadata(dir: &Path, templates: &mut ScopedEnv<Template>, vars: &mut ScopedEnv<String>) {
    for entry in WalkDir::new(dir)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| !e.path().is_dir() && is_valid_file(e))
    {
        let path = entry.path();
        let file_name = entry.file_name().to_str().unwrap();

        if file_name.ends_with(".toml") {
            println!("{:?}: .toml not supported", path);
        } else if file_name.ends_with(".yaml") {
            load_config(vars, path);
        } else if file_name.ends_with(".html") {
            let res = Template::from_file(path);
            match res {
                Result::Ok(_) => println!("template parsed"),
                Result::Err(err) => println!("{:?}", err),
            }
        }
    }
}

fn load_config(vars: &mut ScopedEnv<String>, config_file: &Path) {
    let src = std::fs::read_to_string(config_file).unwrap().to_string();
    let docs = YamlLoader::load_from_str(&src);
    for doc in docs.unwrap() {
        for (key, value) in doc.as_hash().unwrap() {
            vars.set(
                key.as_str().unwrap().to_string(),
                value.as_str().unwrap().to_string(),
            );
        }
    }
}

fn handle_html(in_path: &Path, out_path: &Path) {}

fn handle_md(in_path: &Path, out_path: &Path) {
    let mut pandoc = pandoc::new();
    pandoc.add_input(in_path);
    pandoc.set_output_format(OutputFormat::Html, vec![]);
    let new_out_path = out_path.to_str().unwrap().replace(".md", ".html");
    let out_path_buf = PathBuf::from(new_out_path);
    pandoc.set_output(OutputKind::File(out_path_buf));

    //pandoc.add_filter(filter);
    pandoc.add_option(pandoc::PandocOption::MathML(Option::None));
    let res = pandoc.execute();

    match res {
        Err(err) => println!("{:?}", err),
        _ => println!("Successfully generated {:?}", in_path),
    }
}

/// Turns the ipynb into a directory with an index.html file, and its figures
/// as images in the directory
fn handle_ipynb(in_path: &Path, out_path: &Path) {}
