from textnode import TextNode, TextType


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
