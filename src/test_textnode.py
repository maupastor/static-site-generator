import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()