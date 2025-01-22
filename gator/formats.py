import pypandoc
import yaml
from pathlib import Path
from typing import Dict, Tuple, List
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
            md = "".join(cell["source"]) + "\n"
            if md.startswith("---"):
                data = Frontmatter.read(md)
                md = data["body"]
                frontmatter.update(data["attributes"])
            output.write("\n")
            output.write(md)
        elif cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if not source.startswith("#!OMIT_CODE"):
                output.write("\n```python\n")
                output.write(source)
                output.write("\n```\n")
            for output_cell in cell["outputs"]:
                output_cell_value = __format_output_cell(output_cell)
                if output_cell_value:
                    output.write(output_cell_value)
                else:
                    print(f'[WARNING] Unknown ipynb output type {output_cell['output_type']}')
        else:
            print(f'[WARNING] Unexpected .ipynb cell type {cell["cell_type"]}')
    output = output.flush()
    return frontmatter, output

def __format_output_cell(output_cell: Dict) -> str | None:
    if base64 := __is_img_type(output_cell):
        return f'\n<img src=\"data:image/png;base64,{base64}\" />\n'
    elif s := __is_html_type(output_cell):
        return s
    elif s := __is_pre_block_type(output_cell):
        return f'\n<pre class=\"cell_output\">{s}</pre>\n'
    return None

def __is_img_type(output_cell: Dict) -> str | None:
    if output_cell["output_type"] == "display_data":
        return output_cell["data"]["image/png"]
    return None

def __is_pre_block_type(output_cell: Dict) -> str | None:
    if output_cell["output_type"] == "stream":
        return "".join(output_cell["text"])
    elif output_cell["output_type"] == "execute_result" and "text/plain" in output_cell["data"]:
        return "".join(output_cell["data"]["text/plain"])
    return None

def __is_html_type(output_cell: Dict) -> str | None:
    if output_cell["output_type"] == "execute_result" and "text/html" in output_cell["data"]:
        return "".join(output_cell["data"]["text/html"])


def read_yaml(file: Path) -> Dict:
    with open(file) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return dict()
