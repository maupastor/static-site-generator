import os
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