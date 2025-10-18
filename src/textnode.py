from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value, /) -> bool:
        return self.text == value.text

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
