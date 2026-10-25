import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_default_values(self):
        node = LeafNode(tag="a", value="test")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_raise_if_value_is_none(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(str(context.exception), "value parameter is required")

    def test_to_html_with_empty_value(self):
        node = LeafNode("p", "")

        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_if_tag_is_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = 'LeafNode(\ntag: a,\n value: Click me!,\n props:  href="https://www.google.com"\n)'
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
