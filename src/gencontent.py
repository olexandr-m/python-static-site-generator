import os
from pathlib import Path

from markdown_extractor import extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    html_str = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_str
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dest_path)
        elif os.path.isfile(item_path) and item.endswith(".md"):
            dest_html_path = str(Path(dest_path).with_suffix(".html"))
            generate_page(item_path, template_path, dest_html_path)
