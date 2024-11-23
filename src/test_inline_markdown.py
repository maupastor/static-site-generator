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


class TestExtractImagesAndLinks(unittest.TestCase):
    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_images_and_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text += " - This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_images_and_links_none(self):
        self.assertEqual(extract_markdown_images(None), [])
        self.assertEqual(extract_markdown_links(None), [])


class TestTextnodeSplitterImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ])
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). Let's see how it goes!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(". Let's see how it goes!", TextType.TEXT)
        ])
    
    def test_split_no_images_or_links(self):
        node = TextNode("This is a textnode without ![images] or (links)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is a textnode without ![images] or (links)", TextType.TEXT)
        ])
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is a textnode without ![images] or (links)", TextType.TEXT)
        ])
    
    def test_split_img_link_without_text(self):
        node = TextNode(None, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [])
    
    def test_split_with_multiple_nodes(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and an " +
                "image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        node2 = TextNode("This is just a text node", TextType.TEXT)
        node3 = TextNode("There is an image here ![rick roll](https://i.imgur.com/aKaOqIh.gif). Check this one out!", TextType.TEXT)
        new_nodes = split_nodes_image([node, node2, node3])
        new_nodes2 = split_nodes_link(new_nodes)
        self.assertListEqual(new_nodes2, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is just a text node", TextType.TEXT),
            TextNode("There is an image here ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(". Check this one out!", TextType.TEXT)
        ])

if __name__ == "__main__":
    unittest.main()
