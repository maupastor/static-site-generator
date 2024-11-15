import unittest

from htmlnode import *


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


class TestParentNode(unittest.TestCase):

    def test_node(self):
        node = ParentNode("div", [
            LeafNode("p", "This is a paragraph"),
            LeafNode("a", "Click me!", {"href": "https://www.test.com"})
        ])
        self.assertEqual(node.tag, "div")
    
    def test_to_html_no_tag(self):
        node = ParentNode(None, [
            LeafNode("p", "This is a paragraph"),
            LeafNode("a", "Click me!", {"href": "https://www.test.com"})
        ])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        err = cm.exception
        self.assertEqual(str(err), "Invalid HTML: No HTML Tag was defined")
    
    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        err = cm.exception
        self.assertEqual(str(err), "Invalid HTML: No children were defined")
    
    def test_html_no_children_of_nested_parentnode(self):
        nested_node = ParentNode("p", None, {"width": "100px"})
        node = ParentNode("div", [
            LeafNode("p", "This is a leafnode paragraph"),
            nested_node,
            LeafNode("a", "This is a link", {
                "href": "https://www.test.com",
                "target": "_blank"
                })
        ])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        err = cm.exception
        self.assertEqual(str(err), "Invalid HTML: No children were defined")

    def test_to_html_with_only_leafnodes(self):
        node = ParentNode("div", [
            LeafNode("p", "This is a paragraph"),
            LeafNode("a", "Click me!", {
                "href": "https://www.test.com",
                "target": "_blank"
                })
        ])
        self.assertEqual(node.to_html(), '<div><p>This is a paragraph</p><a href="https://www.test.com" target="_blank">Click me!</a></div>')

    def test_to_html_with_nested_parentnodes_single_level(self):
        nested_node = ParentNode("p", [
            LeafNode(None, "This is a "),
            LeafNode("a", "parentnode", {
                "href": "https://www.test.com",
                "target": "_blank"
                }),
            LeafNode(None, " paragraph")
        ], {"width": "100px"})
        node = ParentNode("div", [
            LeafNode("p", "This is a leafnode paragraph"),
            nested_node,
            LeafNode("a", "This is a link", {
                "href": "https://www.test.com",
                "target": "_blank"
                })
        ])
        expected = '<div><p>This is a leafnode paragraph</p>'
        expected += '<p width="100px">This is a <a href="https://www.test.com" target="_blank">parentnode</a> paragraph</p>'
        expected += '<a href="https://www.test.com" target="_blank">This is a link</a></div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_nested_parentnodes_multiple_levels(self):
        nested_nested_node = ParentNode("p", [
            LeafNode(None, "Second "),
            LeafNode("a", "level", {
                "href": "https://www.test.com",
                "target": "_blank"
                }),
            LeafNode(None, " paragraph")
        ])
        nested_node = ParentNode("div", [
            LeafNode("p", "First level paragraph"),
            nested_nested_node,
            LeafNode("p", "First level paragraph ended")
        ], {"width": "100px"})
        node = ParentNode("div", [
            LeafNode("p", "This is the root paragraph"),
            nested_node,
            LeafNode("p", "This is the root paragraph end")
        ])
        expected = '<div><p>This is the root paragraph</p>'
        expected_nested_nested_node = '<p>Second <a href="https://www.test.com" target="_blank">level</a> paragraph</p>'
        expected_nested_node = '<div width="100px"><p>First level paragraph</p>'
        expected_nested_node += expected_nested_nested_node
        expected_nested_node += '<p>First level paragraph ended</p></div>'
        expected += expected_nested_node
        expected += '<p>This is the root paragraph end</p></div>'
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()