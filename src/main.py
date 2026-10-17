from textnode import TextNode, TextType


def main() -> None:
    text = "This is some anchor text"
    type = TextType.LINK
    url = "https://www.boot.dev"
    print(TextNode(text, type, url))


if __name__ == "__main__":
    main()
