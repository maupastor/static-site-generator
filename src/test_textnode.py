import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.test.com")
        self.assertEqual("TextNode(This is a text node, bold, https://www.test.com)", repr(node))
    
    def test_not_equal_text(self):
        node = TextNode("First node", TextType.ITALIC, "https://www.test.com")
        node2 = TextNode("Second textnode", TextType.ITALIC, "https://www.test.com")
        self.assertNotEqual(node, node2)
    
    def test_not_equal_text_type(self):
        node = TextNode("Testing node", TextType.BOLD, "https://www.test.com")
        node2 = TextNode("Testing node", TextType.ITALIC, "https://www.test.com")
        self.assertNotEqual(node, node2)
    
    def test_not_equal_url(self):
        node = TextNode("Testing node", TextType.ITALIC, "https://www.test.com")
        node2 = TextNode("Testing node", TextType.ITALIC, "https://www.newtest.com")
        self.assertNotEqual(node, node2)
    
    def test_url_is_none(self):
        node = TextNode("Testing node", TextType.ITALIC)
        self.assertIsNone(node.url)
    
    def test_url_is_not_none(self):
        node = TextNode("Testing node", TextType.ITALIC, "https://www.test.com")
        self.assertIsNotNone(node.url)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_to_htmlnode_text(self):
        node = TextNode("Testing raw text node", TextType.TEXT)
        htmlnode = text_node_to_html_node(node)
        self.assertIsNone(htmlnode.tag)
        self.assertEqual(htmlnode.value, "Testing raw text node")
    
    def test_to_htmlnode_bold(self):
        node = TextNode("Testing bold text node", TextType.BOLD)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, "Testing bold text node")
    
    def test_to_htmlnode_italic(self):
        node = TextNode("Testing italic text node", TextType.ITALIC)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "i")
        self.assertEqual(htmlnode.value, "Testing italic text node")
    
    def test_to_htmlnode_code(self):
        node = TextNode("Testing code text node", TextType.CODE)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "code")
        self.assertEqual(htmlnode.value, "Testing code text node")
    
    def test_to_htmlnode_link(self):
        node = TextNode("Testing link text node", TextType.LINK, "https://www.test.com")
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "a")
        self.assertEqual(htmlnode.value, "Testing link text node")
        self.assertEqual(htmlnode.props, {
            "href": "https://www.test.com"
        })
    
    def test_to_htmlnode_image(self):
        node = TextNode("Testing image text node", TextType.IMAGE, "/path/to/image/img.png")
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "img")
        self.assertEqual(htmlnode.value, "")
        self.assertEqual(htmlnode.props, {
            "src": "/path/to/image/img.png",
            "alt": "Testing image text node"
        })
    
    def test_to_htmlnode_invalid(self):
        node = TextNode("This is an invalid text node", "invalid_type")
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        err = cm.exception
        self.assertEqual(str(err), "Invalid Textnode Type: invalid_type")



if __name__ == "__main__":
    unittest.main()