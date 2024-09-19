import pypandoc
import yaml
from pathlib import Path
from typing import Dict, Tuple
import json
from frontmatter import Frontmatter

from gator.util import StringBuffer

def md_to_html(content: str) -> str:
    filters = []
    extra_args = ['--mathml']
    html = pypandoc.convert_text(
        content,
        'html',
        format='md',
        filters=filters,
        extra_args=extra_args
    )
    return html

def ipynb_to_md(content: str) -> Tuple[Dict, str]:
    notebook = json.loads(content)
    output = StringBuffer()
    frontmatter = {}
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            md = "".join(cell["source"])
            if md.startswith("---"):
                data = Frontmatter.read(md)
                md = data["body"]
                frontmatter.update(data["attributes"])
            output.append(md)
        elif cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if not source.startswith("#!OMIT_CODE"):
                output.append("\n```python\n")
                output.append(source)
                output.append("\n```\n")
            for output_cell in cell["outputs"]:
                if output_cell["output_type"] == "display_data":
                    data = output_cell["data"]["image/png"]
                    output.append("\n<img src=\"data:image/png;base64,")
                    output.append(data)
                    output.append("\" />\n")
                elif output_cell["output_type"] == "stream":
                    stream_data = "".join(output_cell["text"])
                    output.append("\n<pre class='cell_output'>\n")
                    output.append(stream_data)
                    output.append("</pre>\n")
        else:
            print(f'[WARNING] Unexpected .ipynb cell type {cell["cell_type"]}')
    output = output.flush()
    return frontmatter, output

def read_yaml(file: Path) -> Dict:
    with open(file) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return dict()
