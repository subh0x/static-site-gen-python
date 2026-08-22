class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: HTMLNode | None = None,
        props: dict[str, str | dict] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        html_attrs = ""

        if self.props != None:
            for prop_key, prop_value in self.props.items():
                html_attrs += f' {prop_key}="{prop_value}"'

        return html_attrs

    def __repr__(self) -> str:
        representation_str = "HTMLNode("
        if self.tag:
            representation_str += "tag: " + str(self.tag) + ", "
        if self.value:
            representation_str += "value: " + str(self.value) + ", "
        if self.children:
            representation_str += "children: " + str(self.children) + ", "
        if self.props:
            representation_str += "props: " + str(self.props)

        return representation_str + ")"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str | dict] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):

        if self.value == None:
            raise ValueError("A LeafNode must have a value.")

        if self.tag == None and self.value:
            return self.value

        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        representation_str = "LeafNode("
        if self.tag:
            representation_str += "tag: " + str(self.tag) + ", "
        if self.value:
            representation_str += "value: " + str(self.value) + ", "
        if self.props:
            representation_str += "props: " + str(self.props)

        return representation_str + ")"
