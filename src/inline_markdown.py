import re
from textnode import *
from functools import reduce

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    node_splitter = splitter(delimiter, text_type)
    splitted_nodes = map(node_splitter, old_nodes)
    nodes = reduce(lambda l, nodes: l + nodes, splitted_nodes)
    return nodes

def splitter(delimiter, text_type):

    def split_node(node):
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            return [node]
        nodes = []
        splitted_node = node.text.split(delimiter)
        if len(splitted_node) < 3:
            raise ValueError(f"Invalid markdown syntax: No closing {delimiter} delimiter found in '{node.text}'")
        for i in range(0, len(splitted_node)):
            if len(splitted_node[i]) > 0:
                if (i + 1) % 2 != 0:
                    nodes.append(TextNode(splitted_node[i], TextType.TEXT))
                else:
                    nodes.append(TextNode(splitted_node[i], text_type))
        return nodes
    
    return split_node

def extract_markdown_images(text):
    images = []
    if text:
        images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)    
    return images

def extract_markdown_links(text):
    links = []
    if text:
        links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def __split_nodes_entites(old_nodes, split_func, starting_pattern, text_type):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        entities = split_func(text)
        for entity in entities:
            new_txt = entity[0]
            path = entity[1]
            splitted_text = text.split(f"{starting_pattern}{new_txt}]({path})", 1)
            if len(splitted_text) != 2:
                raise ValueError(f"Invalid markdown syntax: {text_type.value()} section not closed")
            if splitted_text[0]:
                new_nodes.append(TextNode(splitted_text[0], node.text_type, node.url))
            new_nodes.append(TextNode(new_txt, text_type, path))
            text = splitted_text[1]
        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))
    return new_nodes

def split_nodes_image(old_nodes):
    return __split_nodes_entites(old_nodes, extract_markdown_images, "![", TextType.IMAGE)

def split_nodes_link(old_nodes):
    return __split_nodes_entites(old_nodes, extract_markdown_links, "[", TextType.LINK)

def text_to_textnodes(text):
    main_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([main_node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes