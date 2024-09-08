mod engine;
mod error;
mod generator;
mod utils;

use clap::Parser;
use std::fs;
use std::path::Path;

use generator::generate;

/// Generate a static website from template files
#[derive(Parser, Debug)]
struct Cli {
    #[arg(short, long, default_value_t = false)]
    serve: bool,

    #[arg(short, long, default_value = "./")]
    in_dir: String,

    #[arg(short, long, default_value = "./_out/")]
    out_dir: String,
}

fn main() {
    let args = Cli::parse();
    let mut valid_input = true;

    let in_dir = Path::new(&args.in_dir);
    if !in_dir.exists() {
        println!("Input directory {} must exist!", in_dir.display());
        valid_input = false;
    } else if !in_dir.is_dir() {
        println!("Input directory {} must be a directory!", in_dir.display());
        valid_input = false;
    }

    let out_dir = Path::new(&args.out_dir);
    if !out_dir.exists() {
        let _result = fs::create_dir(out_dir);
    }
    if !out_dir.is_dir() {
        println!(
            "Output directory {} must be a directory!",
            out_dir.display()
        );
        valid_input = false;
    }

    if !valid_input {
        return;
    }

    generate(in_dir, out_dir);
}
