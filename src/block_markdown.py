import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

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
        return "unordered_list"
    if __is_ordered_list(lines):
        return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []    
    for block in blocks:
        
        html_node = __block_to_htmlnode(block)
        # print(f"PARENT TAG:\n{block_node.tag}\n\nCHILDREN:\n{block_node.children}")
        children.append(html_node)
    
    return ParentNode("div", children, None)

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

    
def __block_to_htmlnode(block):
    block_type = block_to_block_type(block)
    tag = None
    children = None
    if block_type == "paragraph":
        tag = "p"
        children = text_to_children(block)
    if block_type == "heading":
        space_idx = block.find(" ", 0, 7)
        formatted_text = block[space_idx + 1:]
        tag = f"h{space_idx}"
        children = text_to_children(formatted_text)
    if block_type == "unordered_list":
        tag = "ul"
        children = list_to_children(block, __remove_md_syntax_ul)
    if block_type == "ordered_list":
        tag = "ol"
        children = list_to_children(block, __remove_idx_from_ordered_list)
    if block_type == "code":
        tag = "pre"
        text = block.removeprefix("```").removesuffix("```")
        children = text_to_children(text)
        children = [ParentNode("code", children)]
    if block_type == "quote":
        formatted_text = __remove_lines_prefix(block, ">")
        tag = "blockquote"
        children = text_to_children(formatted_text)

    if not tag:
        raise ValueError("Invalid block type")

    return ParentNode(tag, children)

def __remove_md_syntax_ul(text):
    formatted_text = text
    formatted_text = __remove_lines_prefix(formatted_text, "* ")
    formatted_text = __remove_lines_prefix(formatted_text, "- ")
    return formatted_text


def list_to_children(text, prefix_func):
    nodes = []
    new_text = prefix_func(text)
    lines = new_text.split("\n")
    for line in lines:
        item = ParentNode("li", text_to_children(line))
        nodes.append(item)
    
    return nodes


def __remove_lines_prefix(text, prefix):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.removeprefix(prefix))
    return "\n".join(new_lines)


def __remove_idx_from_ordered_list(text):
    i = 1
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.removeprefix(f"{i}. "))
        i += 1
    return "\n".join(new_lines)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes