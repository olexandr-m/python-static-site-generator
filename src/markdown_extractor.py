import re


def extract_markdown_images(text) -> list[tuple]:
    images_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(images_regex, text)


def extract_markdown_links(text) -> list[tuple]:
    links_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(links_regex, text)


def extract_title(md: str) -> str:
    lines = md.split("\n")
    title = ""

    for line in lines:
        if line.startswith("# "):
            title = line[1:].strip()
            break

    if not title:
        raise ValueError("Title is required")

    return title
