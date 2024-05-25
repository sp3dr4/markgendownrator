import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.splitlines()
    try:
        h1_header = next(x for x in lines if x.startswith("# "))
        return h1_header[2:]
    except StopIteration:
        raise Exception("page requires main header")


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_content = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_parent = os.path.dirname(dest_path)
    if not os.path.exists(dest_parent):
        os.makedirs(dest_parent)
    with dest_path.open("w") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path
):
    for v in os.listdir(dir_path_content):
        x = dir_path_content / v
        if x.is_file() and x.suffix == ".md":
            dest = dest_dir_path.joinpath(*x.parts[1:]).with_suffix(".html")
            generate_page(x, template_path, dest)
        if x.is_dir():
            generate_pages_recursive(x, template_path, dest_dir_path)
