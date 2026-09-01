from enum import Enum
from htmlnode import LeafNode
from extract_markdown_utils import extract_markdown_images, extract_markdown_links


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            True
            if (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
            else False
        )

    def __repr__(self) -> str:
        if self.url:
            return f'TextNode("{self.text}", TextType.{self.text_type.value.upper()}, {self.url})'
        else:
            return f'TextNode("{self.text}", TextType.{self.text_type.value.upper()})'


def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": f"{text_node.url}"})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            "img", None, props={"src": f"{text_node.url}", "alt": f"{text_node.text}"}
        )
    else:
        raise Exception("Unkown TextNode")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    output_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            # Check if the delimeter exists in the Given Node:
            if node.text.find(delimiter) != -1:
                node_split_text_list = node.text.split(delimiter)
                # print(node_split_text_list)
                for idx, split_text in enumerate(node_split_text_list):
                    if split_text == "":
                        continue
                    if idx % 2 != 0:
                        output_nodes.append(TextNode(split_text, TextType(text_type)))
                    else:
                        output_nodes.append(TextNode(split_text, TextType.TEXT))

            else:
                raise ValueError(
                    f"The given Node does not contain the given text_type: {text_type} TextNode."
                )
        else:
            output_nodes.append(node)

    return output_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            curr_node_text = node.text

            images = extract_markdown_images(curr_node_text)

            if images:
                for idx, image in enumerate(images):
                    text, curr_node_text = curr_node_text.split(
                        f"![{image[0]}]({image[1]})",
                        1,
                    )

                    if text != "":
                        new_nodes.append(TextNode(text, TextType.TEXT))

                    # Append the Image Node to the New Nodes list
                    new_nodes.append(
                        TextNode(
                            image[0],
                            TextType.IMAGE,
                            image[1],
                        )
                    )

                    # Only append the suceeding text if the last image has been reached.
                    # the intermediate text nodes get prcoessed in the next loop
                    if curr_node_text != "" and idx == len(images) - 1:
                        new_nodes.append(TextNode(curr_node_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            curr_node_text = node.text

            links = extract_markdown_links(curr_node_text)
            # print(f"---{links}*****")
            if links:
                for idx, link in enumerate(links):

                    text, curr_node_text = curr_node_text.split(
                        f"[{link[0]}]({link[1]})",
                        1,
                    )

                    if text != "":
                        new_nodes.append(TextNode(text, TextType.TEXT))

                    # Append the link Node to the New Nodes list
                    new_nodes.append(
                        TextNode(
                            link[0],
                            TextType.LINK,
                            link[1],
                        )
                    )

                    # Only append the suceeding text if the last link has been reached.
                    # the intermediate text nodes get prcoessed in the next loop
                    if curr_node_text != "" and idx == len(links) - 1:
                        new_nodes.append(TextNode(curr_node_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes
