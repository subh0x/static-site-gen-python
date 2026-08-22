import unittest
from htmlnode import HTMLNode


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
