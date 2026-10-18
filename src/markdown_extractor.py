import re


def extract_markdown_images(text) -> list[tuple]:
    images_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(images_regex, text)


def extract_markdown_links(text) -> list[tuple]:
    links_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(links_regex, text)
