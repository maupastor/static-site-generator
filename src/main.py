from copy_static import copy_static_resources
from webpage_generation import generate_page

path_static_resources = "./static/"
path_public_resources = "./public/"

path_content_resource = "content/index.md"
path_html_template = "template.html"
destination_resource = "public/index.html"

def main():
    copy_static_resources(path_static_resources, path_public_resources)
    generate_page(path_content_resource, path_html_template, destination_resource)



main()