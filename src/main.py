from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


def main():
    # TextNode:
    text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    # print(text_node)

    # HTMLNode:
    html_node = HTMLNode("a", props={"href": "https://boot.dev", "target": "_blank"})
    # print(html_node)
    # print(html_node.props_to_html())

    # LeafNode:
    leaf_node_2 = LeafNode(
        "a", "Click me!", props={"href": "https://boot.dev", "target": "_blank"}
    )
    # print(leaf_node_2.to_html())
    leaf_node_1 = LeafNode("a", props={"href": "https://boot.dev", "target": "_blank"})
    # print(leaf_node_1.to_html())
    # print(LeafNode("p", "This is a paragraph of text.").to_html())

    parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    # print(parent_node.to_html())

    node = TextNode("This is text with a `code block` word `./main.py`", TextType.TEXT)
    node2 = TextNode("main.py", TextType.CODE)
    new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
    print(new_nodes)


main()
