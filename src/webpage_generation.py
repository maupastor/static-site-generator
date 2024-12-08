import re

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[1:]
            return title.strip()
    
    raise Exception("Undefined document title")