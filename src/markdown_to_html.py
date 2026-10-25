from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        node = _create_node_from_block(block, block_type)
        block_nodes.append(node)

    return ParentNode("div", block_nodes)


def _text_to_children(text) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def _create_node_from_block(block, block_type) -> ParentNode:
    if block_type == BlockType.PARAGRAPH:
        return _create_paragraph_node(block)
    elif block_type == BlockType.HEADING:
        return _create_heading_node(block)
    elif block_type == BlockType.CODE:
        return _create_code_node(block)
    elif block_type == BlockType.QUOTE:
        return _create_quote_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return _create_unordered_list_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return _create_ordered_list_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def _create_paragraph_node(block) -> ParentNode:
    clean_text = " ".join(line.strip() for line in block.splitlines())
    return ParentNode("p", _text_to_children(clean_text))


def _create_heading_node(block) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    text = block[level:].strip()
    clean_text = " ".join(line.strip() for line in text.splitlines())
    return ParentNode(f"h{level}", _text_to_children(clean_text))


def _create_code_node(block) -> ParentNode:
    content = block[3:-3]
    text = content.strip("\n")
    if text:
        text += "\n"

    raw_text_node = TextNode(text, TextType.TEXT)
    code_html_node = text_node_to_html_node(raw_text_node)

    code_parent = ParentNode("code", [code_html_node])
    return ParentNode("pre", [code_parent])


def _create_quote_node(block) -> ParentNode:
    lines = block.splitlines()
    clean_lines = []

    for line in lines:
        clean_line = line.strip().removeprefix(">").strip()
        clean_lines.append(clean_line)

    text = " ".join(clean_lines)
    return ParentNode("blockquote", _text_to_children(text))


def _create_unordered_list_node(block) -> ParentNode:
    lines = block.splitlines()
    list_items = []

    for line in lines:
        item_text = line.removeprefix("- ").strip()
        list_items.append(ParentNode("li", _text_to_children(item_text)))

    return ParentNode("ul", list_items)


def _create_ordered_list_node(block) -> ParentNode:
    lines = block.splitlines()
    list_items = []

    for line in lines:
        parts = line.split(". ", 1)
        item_text = parts[1].strip()

        list_items.append(ParentNode("li", _text_to_children(item_text)))

    return ParentNode("ol", list_items)
