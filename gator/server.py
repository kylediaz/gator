import sys
from pathlib import Path

import socketserver
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import util
from gator.generator import generate

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, f) -> None:
        self.f = f
    def on_any_event(self, event: FileSystemEvent) -> None:
        self.f(event)

def serve(in_dir: Path, out_dir: Path, live_reload: bool = True, port: int = 8000) -> None:

    def reload(event: FileSystemEvent):
        source_path = str(event.src_path)
        event_originated_from_output_dir = str(out_dir) in source_path
        if not event.is_directory and not event_originated_from_output_dir:
            generate(in_dir, out_dir)

    observer: BaseObserver | None = None
    if live_reload:
        event_handler = MyEventHandler(reload)
        observer = Observer()
        observer.schedule(event_handler, path=str(in_dir), recursive=True)
        observer.start()

    with socketserver.TCPServer(("", port), util.handler_from(out_dir)) as httpd:
        print(f"serving at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()
            if observer != None:
                observer.stop()
                observer.join()
        sys.exit(0)
