import argparse
import os
import sys
from pathlib import Path

import server
from gator.generator import generate

PORT = 8000

class Cli:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Generate a static website from template files"
        )

        parser.add_argument(
            "-s",
            "--serve",
            default=False,
            action='store_true',
            help="serve the output as a local HTTP server"
        )

        parser.add_argument(
            "-i",
            "--in_dir",
            default="./",
            help="input directory (default: current directory)"
        )

        parser.add_argument(
            "-o",
            "--out_dir",
            default="./_out/",
            help="output directory (default: './_out/')"
        )

        args = parser.parse_args()

        self.serve = args.serve
        self.in_dir = args.in_dir
        self.out_dir = args.out_dir


def main():
    args = Cli()
    valid_input = True

    in_dir = Path(args.in_dir)
    if not in_dir.exists():
        print(f"Input directory {in_dir} must exist!")
        valid_input = False
    elif not in_dir.is_dir():
        print(f"Input directory {in_dir} must be a directory!")
        valid_input = False

    out_dir = Path(args.out_dir)
    if not out_dir.exists():
        os.makedirs(out_dir)
    if not out_dir.is_dir():
        print(f"Output directory {out_dir} must be a directory!")
        valid_input = False

    if not valid_input:
        sys.exit(1)

    try:
        generate(in_dir, out_dir)
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

    if args.serve:
        server.serve(in_dir, out_dir, port=PORT)


if __name__ == '__main__':
    main()
