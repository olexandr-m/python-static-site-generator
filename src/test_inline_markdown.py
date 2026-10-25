import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    # --- split_nodes_delimiter ---
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

    # --- split_nodes_image ---
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_when_old_node_type_is_not_text(self):
        node = TextNode(
            "This is text with a `code block` word and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.CODE,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode(
                "This is text with a `code block` word and ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.CODE,
            ),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_do_not_strip_meaningful_whitespace(self):
        node = TextNode(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" ", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_with_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_same_image_added_twice(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and one more time ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and one more time ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_image_at_the_very_start_of_the_string(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with a word",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" This is text with a word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_with_entire_text_is_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_with_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT,
            ),
            TextNode("This is text with a `code block`", TextType.CODE),
        ]

        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is text with a `code block`", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    # --- split_nodes_link ---
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [anchor text](https://www.example.com) and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("anchor text", TextType.LINK, "https://www.example.com"),
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_when_old_node_type_is_not_text(self):
        node = TextNode(
            "This is text with a `code block` word and [anchor text](https://www.example.com)",
            TextType.CODE,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode(
                "This is text with a `code block` word and [anchor text](https://www.example.com)",
                TextType.CODE,
            ),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_do_not_strip_meaningful_whitespace(self):
        node = TextNode(
            "This is text with a [anchor text](https://www.example.com) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "https://www.example.com"),
            TextNode(" ", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_with_multiple_links(self):
        node = TextNode(
            "This is text with an [anchor text](https://www.example.com) and another [anchor](https://www.test.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("anchor text", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "https://www.test.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_same_link_added_twice(self):
        node = TextNode(
            "This is text with an [anchor text](https://www.example.com) and one more time [anchor text](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("anchor text", TextType.LINK, "https://www.example.com"),
                TextNode(" and one more time ", TextType.TEXT),
                TextNode("anchor text", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_link_at_the_very_start_of_the_string(self):
        node = TextNode(
            "[anchor text](https://www.example.com) This is text with a word",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("anchor text", TextType.LINK, "https://www.example.com"),
            TextNode(" This is text with a word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_with_entire_text_is_link(self):
        node = TextNode("[anchor text](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("anchor text", TextType.LINK, "https://www.example.com"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_with_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is text with a [anchor text](https://www.example.com)",
                TextType.TEXT,
            ),
            TextNode("This is text with a `code block`", TextType.CODE),
        ]

        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "https://www.example.com"),
            TextNode("This is text with a `code block`", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    # --- text_to_textnodes ---
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://example.com)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_to_textnodes_with_empty_string(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        expected = []
        self.assertListEqual(new_nodes, expected)

    def test_text_to_textnodes_with_only_text_string(self):
        text = "Just text"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("Just text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_to_textnodes_with_entire_text_is_code(self):
        text = "`Just code`"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("Just code", TextType.CODE),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_to_textnodes_if_link_contains_italic_markdown(self):
        text = "Some text [link](https://example_italic.com)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example_italic.com"),
        ]
        self.assertListEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
