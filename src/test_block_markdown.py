import unittest

from block_markdown import *

class TestSplitBlocks(unittest.TestCase):
    def test_simple_blocks_split(self):
        markdown = (""
        "# This is a heading\n\n"
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
        "* This is the first list item in a list block\n"
        "* This is a list item\n"
        "* This is another list item")

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" +
                "* This is a list item\n" +
                "* This is another list item"
        ])
    
    def test_split_blocks_trailing_spaces(self):
        markdown = (""
        "# This is a heading  \n\n"
        " This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
        "   * This is the first list item in a list block\n"
        "* This is a list item\n"
        "* This is another list item   ")
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" +
                "* This is a list item\n" +
                "* This is another list item"
        ])
    
    def test_split_blocks_empty_lines(self):
        markdown = (""
        "# This is a heading  \n\n\n\n"
        " This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
        "\n\n   * This is the first list item in a list block\n"
        "* This is a list item\n"
        "* This is another list item   ")
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" +
                "* This is a list item\n" +
                "* This is another list item"
        ])


class TestBlockTypes(unittest.TestCase):
    def test_block_type_ehading(self):
        text = "### This is a heading"
        self.assertEqual(block_to_block_type(text), "heading")
    
    def test_block_type_not_heading(self):
        text = "####### This is a heading" # seven # characters
        self.assertNotEqual(block_to_block_type(text), "heading")
    
    def test_block_type_code(self):
        text = "``` This is a code block!! ```"
        self.assertEqual(block_to_block_type(text), "code")
    
    def test_block_type_quote(self):
        text = ("> First quote\n"
                "> Second quote\n"
                "> Third quote")
        self.assertEqual(block_to_block_type(text), "quote")
    
    def test_block_type_unordered_list(self):
        text = ("* First element of unordered list\n"
                "* Second element of unordered list\n"
                "* Third element of unordered list")
        self.assertEqual(block_to_block_type(text), "unordered_list")
    
    def test_block_type_unordered_list2(self):
        text = ("- First element of unordered list\n"
                "- Second element of unordered list\n"
                "- Third element of unordered list")
        self.assertEqual(block_to_block_type(text), "unordered_list")
    
    def test_block_type_not_unordered_list(self):
        text = ("- First element of unordered list\n"
                "* Second element of unordered list\n"
                "- Third element of unordered list")
        self.assertNotEqual(block_to_block_type(text), "unordered_list")
    
    def test_block_type_ordered_list(self):
        text = ("1. First element of ordered list\n"
                "2. Second element of ordered list\n"
                "3. Third element of ordered list")
        self.assertEqual(block_to_block_type(text), "ordered_list")
    
    def test_block_type_paragraph(self):
        text = ("This is a paragraph!!")
        self.assertEqual(block_to_block_type(text), "paragraph")



if __name__ == "__main__":
    unittest.main()
