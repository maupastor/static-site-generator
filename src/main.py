from copy_static import copy_static_resources
from webpage_generation import generate_pages_recursive

path_static_resources = "./static/"
path_public_resources = "./public/"
path_content_resources = "./content"
template_path = "./template.html"

def main():
    copy_static_resources(path_static_resources, path_public_resources)
    generate_pages_recursive(path_content_resources, template_path, path_public_resources)


main()