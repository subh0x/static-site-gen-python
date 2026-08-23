import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(
            tag="a", props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html_node.props_to_html(), expected_result)

    def test_props_to_html_1(self):
        html_node = HTMLNode(tag="a", props={"href": "https://boot.dev"})
        expected_result = ' href="https://boot.dev"'
        self.assertEqual(html_node.props_to_html(), expected_result)

    def test_props_to_html_2(self):
        html_node = HTMLNode(tag="img", props={"src": "https://img.jpeg"})
        expected_result = ' src="https://img.jpeg"'
        self.assertEqual(html_node.props_to_html(), expected_result)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_returns_text_for_empty_tag(self):
        node = LeafNode(None, "Sample text")
        self.assertEqual(node.to_html(), "Sample text")

    # def test_leaf_to_html_valueerror(self):
    #     node = LeafNode("a", props={"href": "https://www.google.com"})
    #     self.assertRaises(ValueError)


class TestParentNode(unittest.TestCase):
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
