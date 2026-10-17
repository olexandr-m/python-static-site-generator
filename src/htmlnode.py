class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        result = ""
        if self.props is None:
            return result

        for attr, value in self.props.items():
            result += f' {attr}="{value}"'

        return result

    def __repr__(self) -> str:
        return f"HTMLNode(\ntag: {self.tag},\n value: {self.value},\n children: {self.children},\n props: {self.props_to_html()}\n)"
