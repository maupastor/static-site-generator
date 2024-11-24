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



if __name__ == "__main__":
    unittest.main()
