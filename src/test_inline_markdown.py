import unittest

from textnode import TextNode, TextType
from inline_markdown import *

class TestTextNodeSplitter(unittest.TestCase):
    def test_simple(self):
        node = TextNode("*italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ])

    def test_multiple(self):
        node = TextNode("*italic block* word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node3 = TextNode("This is a **bold** text block with also some *italic text*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        new_nodes3 = split_nodes_delimiter(new_nodes2, "`", TextType.CODE)
        self.assertEqual(new_nodes3, [
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text block with also some ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC)
        ])
    
    def test_no_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        err = cm.exception
        self.assertEqual(str(err), "Invalid markdown syntax: No closing ` delimiter found in 'This is text with a `code block word'")
    
    def test_unchanged_textnode(self):
        node = TextNode("This is a **bold** textnode of type bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])


if __name__ == "__main__":
    unittest.main()
