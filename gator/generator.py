from pathlib import Path
from typing import Dict, Tuple
import os
import shutil
from frontmatter import Frontmatter
import sass

import gator.util as util
from gator.engine import Template, Environment
import gator.formats as formats

def generate(in_dir: Path, out_dir: Path):
    gator_dir = in_dir.joinpath(".gator")
    env = __setup_env(gator_dir)

    try:
        shutil.rmtree(out_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    os.makedirs(out_dir, exist_ok=True)

    def to_output_path(in_path, new_ext=None) -> str:
        out_path = path.removeprefix(str(in_dir))
        out_path = str(out_dir) + out_path
        if new_ext != None:
            out_path = util.change_file_extension(out_path, new_ext)
        return out_path

    for root, dirs, files in os.walk(in_dir):
        # Skip ".gator" directories
        dirs[:] = [
            d for d in dirs
            if d != '.gator'
            and not d.startswith("_")
            and not d.startswith(".")
        ]

        # traverse files
        for file in files:
            env.var.push()
            path = os.path.join(root, file)

            def get_rendered_content() -> Tuple[Dict, str]:
                page = Frontmatter.read_file(path)
                template = Template.from_str(page['body'])
                fm = page['attributes']
                env.var.update(fm)
                content = template.render(env)
                return fm, content

            fm, html = {}, None
            if file.endswith('.md'):
                fm, content = get_rendered_content()
                html = formats.md_to_html(content)
            elif file.endswith('.ipynb'):
                ipynb = util.get_file_content(path)
                fm, md = formats.ipynb_to_md(ipynb)
                env.var.update(fm)
                content = Template.from_str(md).render(env)
                html = formats.md_to_html(content)
            elif file.endswith('.html'):
                fm, html = get_rendered_content()

            if html != None:
                out_path = to_output_path(path, new_ext='html')

                template = env.var["template"]
                if template != None:
                    if template in env.template:
                        template = env.template[template]
                        sink = util.FileSink(out_path)
                        html = template.render_with_content(sink, env, html)
                        sink.flush()
                    else:
                        print("[ERROR] Template", template, "not found")
                else:
                    util.write_file(out_path, html)

            elif file.endswith('.scss'):
                raw_scss = util.get_file_content(path)
                converted_css = sass.compile(string=raw_scss, output_style='compressed')
                out_path = to_output_path(path, new_ext='css')
                util.write_file(out_path, converted_css)
            else:
                out_path = to_output_path(path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                shutil.copyfile(path, out_path)
            env.var.pop()


def __setup_env(env_dir: Path) -> Environment:
    output = Environment()
    for file in util.walk_files(env_dir):
        if file.name.endswith(".yaml"):
            vars = formats.read_yaml(file)
            output.var.update(vars)
        else:
            new_template = Template.from_file(file)
            output.template[file.name] = new_template

    return output
