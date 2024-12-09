import os
import pathlib
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[1:]
            return title.strip()
    
    raise Exception("Undefined document title")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w") as dest_file:
        dest_file.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.isdir(dir_path_content):
        raise ValueError("Invalid source directory")
    
    os.makedirs(dest_dir_path, exist_ok=True)

    for entry in os.listdir(dir_path_content):
        from_path = pathlib.Path(dir_path_content, entry)
        to_path = pathlib.Path(dest_dir_path, entry)
        if from_path.is_file():
            if from_path.suffix == ".md":
                to_path = to_path.with_suffix(".html")
                generate_page(str(from_path), template_path, to_path)
        else:
            to_path = str(to_path)
            generate_pages_recursive(str(from_path), template_path, to_path)
    
