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
