import re
from enum import Enum


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def _is_ordered_list(lines: list[str]) -> bool:
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            return False
    return True


def markdown_to_blocks(markdown) -> list[str]:
    result: list[str] = []

    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip():
            result.append(block.strip())

    return result


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif _is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
