from copystatic import clean_and_copy_directory


def main() -> None:
    source = "static"
    destination = "public"

    print("Starting static site generator...")
    clean_and_copy_directory(source, destination)
    print("Site generated successfully!")


if __name__ == "__main__":
    main()
