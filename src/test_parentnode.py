import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_default_values(self):
        node = ParentNode(tag="a", children=[])
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, None)

    def test_to_html_raise_if_there_is_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])

        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        self.assertEqual(str(context.exception), "tag parameter is required")

    def test_to_html_raise_if_there_is_no_children(self):
        parent_node = ParentNode("p", [])

        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        self.assertEqual(str(context.exception), "children are required")

    def test_to_html_raise_if_tag_is_none(self):
        node = ParentNode(None, [LeafNode("span", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raise_if_children_is_none(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_parent_node_as_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_parent_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_parent_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )


if __name__ == "__main__":
    unittest.main()
