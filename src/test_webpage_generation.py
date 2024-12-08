import unittest

from webpage_generation import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = (""
        "# This is the title\n\n"
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
        "* This is the first list item in a list block\n"
        "* This is a list item\n"
        "* This is another list item")

        expected = "This is the title"

        self.assertEqual(expected, extract_title(markdown))
    
    def test_extract_title_in_between_lines(self):
        markdown = (""
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
        "# This is the title in between some lines\n\n"
        "* This is the first list item in a list block\n"
        "* This is a list item\n"
        "* This is another list item")

        expected = "This is the title in between some lines"

        self.assertEqual(expected, extract_title(markdown))
    
    def test_no_title(self):
        markdown = (""
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
        "* This is the first list item in a list block\n"
        "* This is a list item\n"
        "* This is another list item")

        expected = "This is the title in between some lines"

        with self.assertRaises(Exception) as cm:
            extract_title(markdown)
        err = cm.exception

        self.assertEqual(str(err), "Undefined document title")


if __name__ == "__main__":
    unittest.main()
