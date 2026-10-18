import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter_happy_path(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_when_old_node_type_is_not_text(self):
        node = TextNode("This is text with a `code block` word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a `code block` word", TextType.BOLD),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_whith_invalid_markdown_syntax(self):
        old_node = TextNode("This is text with a ``code block` word", TextType.TEXT)

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([old_node], "`", TextType.CODE)

        self.assertEqual(
            str(context.exception),
            "Invalid Markdown syntax: closing delimiter '`' not found.",
        )

    def test_split_nodes_delimiter_do_not_strip_meaningful_whitespace(self):
        node = TextNode("This is text with a `code block` ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" ", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_whitespace_inside_delimiters(self):
        node = TextNode("This is text with a `` ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode(" ", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_multiple_delimited_sections(self):
        node = TextNode(
            "This is text with a `code block` word `another code block`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_delimiter_at_the_very_start_of_the_string(self):
        node = TextNode("`code block` This is text with a word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" This is text with a word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_bold_delimiter(self):
        node = TextNode("This is text with a *bold text* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_entire_text_is_delimited(self):
        node = TextNode("_This is text with a word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with a word", TextType.ITALIC),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_multiple_nodes(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("`Another code block`", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("Another code block", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
