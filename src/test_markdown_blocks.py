import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownBlocks(unittest.TestCase):
    # --- markdown_to_blocks ---
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_with_whitespace_on_beginning(self):
        md = """
 This is **bolded** paragraph

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_line(self):
        md = """
 This is **bolded** paragraph


- This is a list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- This is a list",
            ],
        )

    def test_markdown_to_blocks_with_leading_and_trailing_whitespace(self):
        md = "   # This is a heading \n\n This is a paragraph with tabs and spaces.\t  "
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            ["# This is a heading", "This is a paragraph with tabs and spaces."],
        )

    def test_markdown_to_blocks_with_excessive_blank_lines_with_spaces(self):
        md = "Block 1\n\n   \n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_block_to_block_type_with_valid_headings(self):
        type1 = block_to_block_type("# Heading 1")
        type2 = block_to_block_type("###### Heading 6")

        self.assertEqual(type1, BlockType.HEADING)
        self.assertEqual(type2, BlockType.HEADING)

    def test_block_to_block_type_with_invalid_headings(self):
        type1 = block_to_block_type("####### Too many hashes")
        type2 = block_to_block_type("#NoSpace")

        self.assertEqual(type1, BlockType.PARAGRAPH)
        self.assertEqual(type2, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_valid_code_block(self):
        type1 = block_to_block_type("```\ndef test():\n    return 'world'\n```")

        self.assertEqual(type1, BlockType.CODE)

    def test_block_to_block_type_with_invalid_code_blocks(self):
        type1 = block_to_block_type("```\nx = 1\n``` inline text")
        type2 = block_to_block_type("```python x = 1\n```")
        type3 = block_to_block_type("```code```")

        self.assertEqual(type1, BlockType.PARAGRAPH)
        self.assertEqual(type2, BlockType.PARAGRAPH)
        self.assertEqual(type3, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_valid_quotes(self):
        type1 = block_to_block_type("> This is a quote")
        type2 = block_to_block_type(">No space quote")
        type3 = block_to_block_type("> Line 1\n>Line 2\n> Line 3")

        self.assertEqual(type1, BlockType.QUOTE)
        self.assertEqual(type2, BlockType.QUOTE)
        self.assertEqual(type3, BlockType.QUOTE)

    def test_block_to_block_type_with_invalid_quote(self):
        type1 = block_to_block_type(
            "> Line 1\nThis line misses the character\n> Line 3"
        )
        self.assertEqual(type1, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_valid_unordered_list(self):
        type1 = block_to_block_type("- Item 1\n- Item 2\n- Item 3")
        self.assertEqual(type1, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_with_invalid_unordered_list(self):
        type1 = block_to_block_type("-Item 1\n- Item 2")
        type2 = block_to_block_type("* Item 1\n* Item 2")

        self.assertEqual(type1, BlockType.PARAGRAPH)
        self.assertEqual(type2, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_valid_ordered_list(self):
        type1 = block_to_block_type("1. First\n2. Second\n3. Third")
        self.assertEqual(type1, BlockType.ORDERED_LIST)

    def test_block_to_block_type_with_invalid_ordered_list(self):
        type1 = block_to_block_type("2. First\n3. Second")
        type2 = block_to_block_type("1. First\n3. Third")
        type3 = block_to_block_type("1.First\n2.Second")

        self.assertEqual(type1, BlockType.PARAGRAPH)
        self.assertEqual(type2, BlockType.PARAGRAPH)
        self.assertEqual(type3, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_normal_paragraph(self):
        type1 = block_to_block_type(
            "This is just a normal paragraph of text that doesn't match anything."
        )
        self.assertEqual(type1, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
