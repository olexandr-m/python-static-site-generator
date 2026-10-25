import unittest
from textwrap import dedent

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraph_single_line(self):
        md = "This is a simple single-line paragraph."
        expected = "<div><p>This is a simple single-line paragraph.</p></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_paragraph_multi_line_and_inline(self):
        md = dedent("""
                This is **bolded** paragraph
                text in a p
                tag here
                """).strip()
        expected = (
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_paragraph_multiple_paragraphs(self):
        md = dedent("""
                This is the first paragraph block.
                It spans multiple lines.

                This is the second paragraph block.
                It is separated by two newlines.
                """).strip()
        expected = (
            "<div>"
            "<p>This is the first paragraph block. It spans multiple lines.</p>"
            "<p>This is the second paragraph block. It is separated by two newlines.</p>"
            "</div>"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_headings(self):
        md = "### Heading"
        expected = "<div><h3>Heading</h3></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_heading_with_newlines(self):
        md = dedent("""
                ## Heading with
                a newline
                """).strip()
        expected = "<div><h2>Heading with a newline</h2></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_headings_with_level_more_then_six(self):
        md = "####### Heading"
        expected = "<div><p>####### Heading</p></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_codeblock_standard(self):
        md = dedent("""
                ```
                This is text that _should_ remain
                the **same** even with inline stuff
                ```
                """).strip()
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_codeblock_empty(self):
        md = "```\n```"
        expected = "<div><pre><code></code></pre></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_codeblock_single_line(self):
        md = dedent("""
                ```
                print('hello')
                ```
                """).strip()
        expected = "<div><pre><code>print('hello')\n</code></pre></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_quoteblock(self):
        md = dedent("""
            > This is a quote
            > that spans
            > multiple lines
            """).strip()
        expected = "<div><blockquote>This is a quote that spans multiple lines</blockquote></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_quoteblock_with_special_words(self):
        md = dedent("""
            > Greater than before
            > Double check this
            """).strip()
        expected = (
            "<div><blockquote>Greater than before Double check this</blockquote></div>"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_unordered_list(self):
        md = dedent("""
            - Item 1
            - Item 2 with **bold**
            - Item 3
            """).strip()
        expected = "<div><ul><li>Item 1</li><li>Item 2 with <b>bold</b></li><li>Item 3</li></ul></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = dedent("""
            1. First item
            2. Second item with **bold**
            3. Third item
            """).strip()
        expected = "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item</li></ol></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_ordered_list_multi_digit_and_internal_dots(self):
        md = dedent("""
            1. Buy some milk. And bread.
            10. Tenth item on the list.
            """).strip()
        expected = "<div><ol><li>Buy some milk. And bread.</li><li>Tenth item on the list.</li></ol></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_ordered_list_invalid_start(self):
        md = dedent("""
                2. This should not be an ordered list
                3. Because it starts with 2
                """).strip()
        expected = "<div><p>2. This should not be an ordered list 3. Because it starts with 2</p></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_multiple_mixed_blocks(self):
        md = dedent("""
            # Main Heading

            This is a paragraph with `code` inline.

            > A wise quote here

            - List item 1
            - List item 2
            """).strip()
        expected = (
            "<div>"
            "<h1>Main Heading</h1>"
            "<p>This is a paragraph with <code>code</code> inline.</p>"
            "<blockquote>A wise quote here</blockquote>"
            "<ul><li>List item 1</li><li>List item 2</li></ul>"
            "</div>"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_inline_markdown_in_quotes_and_headings(self):
        md = dedent("""
                ## Heading with `inline code` and **bold**

                > Quote with _italic_ and a [link](https://boot.dev)
                """).strip()
        expected = (
            "<div>"
            "<h2>Heading with <code>inline code</code> and <b>bold</b></h2>"
            '<blockquote>Quote with <i>italic</i> and a <a href="https://boot.dev">link</a></blockquote>'
            "</div>"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_entirely_empty_document(self):
        md = "   \n  \n   "
        expected = "<div></div>"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
