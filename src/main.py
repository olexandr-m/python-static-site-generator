from copystatic import clean_and_copy_directory
from gencontent import generate_pages_recursive


def main() -> None:
    source = "static"
    destination = "public"

    print("Starting static site generator...")
    clean_and_copy_directory(source, destination)
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="public",
    )
    print("Site generated successfully!")


if __name__ == "__main__":
    main()
