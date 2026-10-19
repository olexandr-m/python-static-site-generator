from markdown_extractor import extract_markdown_images, extract_markdown_links
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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        for image in images:
            image_alt, image_link = image
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        for link in links:
            anchor_text, url = link
            sections = original_text.split(f"[{anchor_text}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            original_text = sections[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    new_nodes: list[TextNode] = [node]

    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    return new_nodes
