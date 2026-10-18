import unittest

from markdown_extractor import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_multiple_images_in_text(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_with_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_no_image(self):
        matches = extract_markdown_images("This is just plain text.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_links_but_not_image(self):
        matches = extract_markdown_images(
            "This is text with a [a regular link](https://example.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_empty_alt_text(self):
        matches = extract_markdown_images(
            "This is text with a ![](https://example.com/logo.png)"
        )
        self.assertListEqual([("", "https://example.com/logo.png")], matches)

    def test_extract_markdown_images_with_alt_text_but_without_image(self):
        matches = extract_markdown_images("This is text with a ![alt text]()")
        self.assertListEqual([("alt text", "")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [anchor text](https://www.example.com)"
        )
        self.assertListEqual([("anchor text", "https://www.example.com")], matches)

    def test_extract_markdown_links_with_multiple_links_in_text(self):
        matches = extract_markdown_links(
            "This is text with a link [anchor text](https://www.example.com) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("anchor text", "https://www.example.com"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_with_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_no_link(self):
        matches = extract_markdown_links("This is just plain text.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_image_but_not_link(self):
        matches = extract_markdown_links(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_empty_anchor_text(self):
        matches = extract_markdown_links(
            "This is text with a [](https://www.example.com)"
        )
        self.assertListEqual([("", "https://www.example.com")], matches)

    def test_extract_markdown_links_with_anchor_text_but_without_link(self):
        matches = extract_markdown_links("This is text with a [anchor text]()")
        self.assertListEqual([("anchor text", "")], matches)


if __name__ == "__main__":
    unittest.main()
