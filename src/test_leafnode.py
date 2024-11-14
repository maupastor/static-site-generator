import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_node(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")

    def test_props_to_html(self):
        node = LeafNode("a", "Click here!", {
            "href": "https://www.test.com",
            "target": "_blank"
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.test.com" target="_blank"')
    
    def test_to_html(self):
        node = LeafNode("a", "Click here!", {
            "href": "https://www.test.com",
            "target": "_blank"
        })
        self.assertEqual(node.to_html(), '<a href="https://www.test.com" target="_blank">Click here!</a>')
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")
    
    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()



if __name__ == "__main__":
    unittest.main()