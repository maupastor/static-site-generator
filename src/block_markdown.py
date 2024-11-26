import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block : block.strip(), blocks))
    blocks = list(filter(lambda block : len(block) > 0, blocks))
    return blocks

def block_to_block_type(text):
    #text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))
    if len(re.findall(r"^#{1,6}\s+\w+", text)) > 0:
        return "heading"
    if text.startswith("```") and text.endswith("```"):
        return "code"
    lines = text.split("\n")
    if __all_lines_startwith(">", lines):
        return "quote"
    if __all_lines_startwith("* ", lines) or __all_lines_startwith("- ", lines):
        return "unordered list"
    if __is_ordered_list(lines):
        return "ordered list"
    return "paragraph"

def __all_lines_startwith(chars, lines):
    if isinstance(chars, str):
        chars = (chars,)
    if not lines or len(lines) == 0:
        return False
    for line in lines:
        if not line.startswith(chars):
            return False
    return True

def __is_ordered_list(lines):
    if not lines or len(lines) == 0:
        return False
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            return False
    return True
