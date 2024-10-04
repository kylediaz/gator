from pathlib import Path
from typing import Dict, Tuple
import os
import shutil
from frontmatter import Frontmatter
import sass

from gator.site import Site, Page, File
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

    site = __map_site(in_dir)
    __render_site(site, out_dir, env)

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

def __map_site(in_dir: Path) -> Site:
    pages = {}
    files = []

    for file in util.walk_files(in_dir):
        rel_path = file.relative_to(in_dir)

        if file.name.startswith("_") or file.name.startswith(".") \
                or Path(".gator") in rel_path.parents:
            continue

        vars, html = {}, None
        if file.name.endswith('.md'):
            vars, content = __parse_page(file)
            html = formats.md_to_html(content)
        elif file.name.endswith('.ipynb'):
            ipynb = util.get_file_content(file)
            vars, markdown = formats.ipynb_to_md(ipynb)
            html = markdown
        elif file.name.endswith('.html'):
            vars, html = __parse_page(file)

        if html != None:
            page = Page(rel_path, vars, html)
            pages[rel_path.as_posix()] = page
        else:
            files.append(File(file))

    output = Site()
    output.pages = pages
    output.files = files
    return output

def __parse_page(path: Path) -> Tuple[Dict, str]:
    """parses the frontmatter and body content of a file"""
    page = Frontmatter.read_file(path)
    vars = page['attributes']
    content = page['body']
    return (vars, content)

def __render_site(site: Site, out_dir: Path, env: Environment) -> None:

    for file in site.files:
        try:
            __render_file(file, out_dir)
        except Exception as e:
            print('[ERROR] When rendering', file.path, e)

    for page in site.pages.values():
        try:
            __render_page(page, out_dir, env)
        except Exception as e:
            print('[ERROR] When rendering', page.path, e)


def __render_file(file: File, out_dir: Path) -> None:
    if file.path.name.endswith('.scss'):
        raw_scss = util.get_file_content(file.path)
        converted_css = sass.compile(string=raw_scss, output_style='compressed')
        out_path = out_dir.joinpath(file.path.with_suffix(".css")).as_posix()
        util.write_file(out_path, converted_css)
    else:
        out_path = out_dir.joinpath(file.path).as_posix()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        shutil.copyfile(file.path, out_path)

def __render_page(page: Page, out_dir: Path, env: Environment) -> None:
    out_path = out_dir.joinpath(page.path.with_suffix(".html"))

    env.var.push()
    env.var.update(page.vars)

    content_template = Template.from_str(page.raw_content)

    template_name = env.var["template"]
    if template_name != None:
        if template_name in env.template:
            template = env.template[template_name]
            output = util.FileOutputStream(out_path.as_posix())
            html = template.render(output, env, content_template)
            output.flush()
        else:
            print("[ERROR] In", page, " template", template_name, "not found")
    else:
        content_template.render_to_file(out_path, env)

    env.var.pop()
