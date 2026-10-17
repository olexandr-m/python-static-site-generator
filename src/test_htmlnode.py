import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_when_props_is_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode(tag="p", value="test paragraph", props={"target": "_blank"})
        expected = 'HTMLNode(\ntag: p,\n value: test paragraph,\n children: None,\n props:  target="_blank"\n)'
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
