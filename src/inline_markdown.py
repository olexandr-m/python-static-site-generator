from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(
                f"Invalid Markdown syntax: closing delimiter '{delimiter}' not found."
            )

        splited_text = node.text.split(delimiter)
        new_nodes = []

        for index, text in enumerate(splited_text):
            if index % 2 == 0:
                node_type = TextType.TEXT
            else:
                node_type = text_type
            if text != "":
                new_nodes.append(TextNode(text, node_type))

        result.extend(new_nodes)

    return result
