import unittest
from textnode import (
    TextNode,
    TextType,
    split_nodes_link,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")


class TestSplitNodeCmd(unittest.TestCase):
    def test_basic_node_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        output_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(output_nodes, expected_output_nodes)

    def test_node_split_with_multiple_code_block(self):
        node = TextNode(
            "This is text with a `code block` word `./main.py`", TextType.TEXT
        )
        # node2 = TextNode("main.py", TextType.CODE)
        output_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word ", TextType.TEXT),
            TextNode("./main.py", TextType.CODE),
        ]
        self.assertEqual(output_nodes, expected_output_nodes)

    def test_multi_node_split_v1(self):
        node_1 = TextNode(
            "This is text with a `code block` word `./main.py`", TextType.TEXT
        )
        node_2 = TextNode("./test.py", TextType.CODE)
        output_nodes = split_nodes_delimiter([node_1, node_2], "`", TextType.CODE)
        expected_output_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word ", TextType.TEXT),
            TextNode("./main.py", TextType.CODE),
            TextNode("./test.py", TextType.CODE),
        ]
        self.assertEqual(output_nodes, expected_output_nodes)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image_middle(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
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

    def test_image_at_start_no_leading_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) leading only", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" leading only", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end_no_trailing_text(self):
        node = TextNode(
            "trailing only ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("trailing only ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_only_image_no_surrounding_text(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_no_images_returns_node_unchanged(self):
        node = TextNode("This text has no images at all", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_passthrough(self):
        node = TextNode("bolded text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_old_nodes_mixed(self):
        text_node = TextNode(
            "before ![image](https://i.imgur.com/zjjcJKZ.png) after", TextType.TEXT
        )
        bold_node = TextNode("bold text", TextType.BOLD)
        plain_node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_image([text_node, bold_node, plain_node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode("plain text", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link_middle(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) "
            "and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_link_at_start_no_leading_text(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) leading only", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" leading only", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end_no_trailing_text(self):
        node = TextNode(
            "trailing only [link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("trailing only ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_only_link_no_surrounding_text(self):
        node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_no_links_returns_node_unchanged(self):
        node = TextNode("This text has no links at all", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_passthrough(self):
        node = TextNode("bolded text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_old_nodes_mixed(self):
        text_node = TextNode(
            "before [link](https://i.imgur.com/zjjcJKZ.png) after", TextType.TEXT
        )
        bold_node = TextNode("bold text", TextType.BOLD)
        plain_node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_link([text_node, bold_node, plain_node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode("plain text", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitTextIntoTextNodes(unittest.TestCase):
    def test_text_with_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            [
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
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_text_with_multiple_bold_types(self):
        text = "This is **text** with a **bold2** word."
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" word.", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )


if __name__ == "__main__":
    unittest.main()
