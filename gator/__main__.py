import argparse
import os
from pathlib import Path
from gator.generator import generate

import http.server
import socketserver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

PORT = 8000

def handler_from(directory):
    def _init(self, *args, **kwargs):
        return http.server.SimpleHTTPRequestHandler.__init__(self, *args, directory=self.directory, **kwargs)
    return type(f'HandlerFrom<{directory}>',
                (http.server.SimpleHTTPRequestHandler,),
                {'__init__': _init, 'directory': directory})

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, f) -> None:
        self.f = f
    def on_any_event(self, event: FileSystemEvent) -> None:
        self.f(event)

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
        return

    generate(in_dir, out_dir)

    if args.serve:
        with socketserver.TCPServer(("", PORT), handler_from(out_dir)) as httpd:
            print(f"serving at http://localhost:{PORT}")

            def reload(event: FileSystemEvent):
                if not event.is_directory and str(out_dir) not in event.src_path:
                    generate(in_dir, out_dir)

            event_handler = MyEventHandler(reload)
            observer = Observer()
            observer.schedule(event_handler, path=in_dir, recursive=True)
            observer.start()
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                httpd.server_close()
                observer.stop()
                observer.join()


if __name__ == '__main__':
    main()
