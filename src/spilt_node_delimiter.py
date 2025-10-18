from textnode import TextType, TextNode
from extract_markdown import extract_markdown_links, extract_markdown_images
from typing import List


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


# def split_nodes_delimiter(old_nodes: List[TextNode], delimiter, text_type):
#     word_list = []
#     for node in old_nodes:
#         if node.text_type is TextType.TEXT:
#             text_node = node.text.split(delimiter)
#             if len(text_node) % 2 == 0:
#                 raise Exception("unmatched delimiter")
#             for i, text in enumerate(text_node):
#                 if text == "":
#                     continue
#                 if i % 2 == 0:
#                     word_list.append(TextNode(text, text_type))
#                 else:
#                     word_list.append(TextNode(text, TextType.TEXT))
#     return word_list


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


# def split_nodes_image(old_nodes):
#     word_list = []
#     for node in old_nodes:
#         if node.text_type == TextType.TEXT:
#             word_list.append(old_nodes)
#         text = node.text
#         current_text = text
#         image = extract_markdown_images(text)
#
#         if len(image) == 0:
#             word_list.append(old_nodes)
#
#         for alt_text, url in image:
#             image_markdown = f"![{alt_text}]({url})"
#             sections = current_text.split(image_markdown, 1)
#             text_before = sections[0]
#             if text_before:
#                 word_list.append(TextNode(text_before, TextType.TEXT))
#
#             word_list.append(TextNode(alt_text, TextType.IMAGE, url))
#             current_text = sections[1]
#         if current_text:
#             word_list.append(TextNode(current_text, TextType.TEXT))
#
#     return word_list


def split_nodes_link(old_nodes):
    word_list = []
    for node in old_nodes:
        if node.text_type != TextType.LINK:
            word_list.append(old_nodes)
        text = node.text
        current_text = text
        link = extract_markdown_images(text)

        if len(link) == 0:
            word_list.append(old_nodes)
        for link_text, url in link:
            image_markdown = f"[{link_text}]({url})"
            sections = current_text.split(image_markdown, 1)
            text_before = sections[0]
            if text_before:
                word_list.append(TextNode(text_before, TextType.TEXT))

            word_list.append(TextNode(link_text, TextType.LINK, url))
            current_text = sections[1]
        if current_text:
            word_list.append(TextNode(current_text, TextType.TEXT))

    return word_list


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    first = split_nodes_delimiter([node], "**", TextType.BOLD)
    second = split_nodes_delimiter(first, "_", TextType.ITALIC)
    third = split_nodes_delimiter(second, "`", TextType.CODE)
    forth = split_nodes_image(third)
    fifth = split_nodes_link(forth)
    return fifth
