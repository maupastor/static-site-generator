import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_node(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")

    def test_props_to_html(self):
        node = HTMLNode("a", "Click here!", None, {
            "href": "https://www.test.com",
            "target": "_blank"
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.test.com" target="_blank"')
    
    def test_props_to_html_not_equal(self):
        node = HTMLNode("a", "Click here!", None, {
            "href": "https://www.test.com"
        })
        self.assertNotEqual(node.props_to_html(), ' href="https://www.test.com" target="_blank"')
    
    def test_repr(self):
        node = HTMLNode("p", "node value", None, {
            "href": "https://www.test.com"
        })
        self.assertEqual('HTMLNode(p, node value, None,  href="https://www.test.com")', repr(node))



if __name__ == "__main__":
    unittest.main()