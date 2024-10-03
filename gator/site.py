"""
Kinda like an AST for the website
"""

from pathlib import Path
from typing import Any, Dict, List
from dataclasses import dataclass

@dataclass
class Page:
    """
    A page is a file that has frontmatter and can use the templating language
    """
    path: Path
    vars: Dict[str, Any]
    raw_content: str

    def __repr__(self) -> str:
        return f'Page({self.path})'

@dataclass
class File:
    """
    A file is something that gets copied over to the output directory as-is
    """
    path: Path

class Site:
    pages: Dict[str, Page]
    files: List[File]

    def pages_in_dir(self, dir: str) -> List[Page]:
        return [
            page
            for (path, page) in self.pages.items()
            if path.startswith(dir)
        ]
