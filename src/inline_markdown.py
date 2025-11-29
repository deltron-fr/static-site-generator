from textnode import TextType, TextNode
import re

def text_to_textnodes(text):
    """
    converts text to a list of text nodes
    """
    node = TextNode(text, TextType.TEXT)

    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    new_nodes = split_nodes_images(new_nodes)

    new_nodes = split_nodes_links(new_nodes)

    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    splits text nodes by delimiters such as - _(italics), **(bold), `(code)
    """
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        text_split = old_node.text.split(delimiter)
        
        if len(text_split) % 2 != 1:
            raise Exception("Invalid text, missing delimiter")
        
        for i in range(len(text_split)):
            if i % 2 == 0:
                if not text_split[i]:
                    continue
                new_nodes.append(TextNode(text_split[i], TextType.TEXT))
            else:
                if not text_split[i]:
                    continue
                new_nodes.append(TextNode(text_split[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_images(old_nodes):
    """
    splits nodes by images using its regex pattern
    """
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue


        original_text = old_node.text
        matches = extract_markdown_images(original_text)
        if not matches:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            continue

        for i in range(len(matches)):
            image_text, image_url  = matches[i][0], matches[i][1]
            sections = original_text.split(f"![{image_text}]({image_url})", 1)
            if not sections:
                break
            
            if sections[0]:
                if not extract_markdown_images(sections[0]):
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))

            if sections[1]:
                if not extract_markdown_images(sections[1]):
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))

            original_text = sections[1]

    return new_nodes

def split_nodes_links(old_nodes):
    """
    splits nodes by links using its regex pattern
    """
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue


        original_text = old_node.text
        matches = extract_markdown_links(old_node.text)
        if not matches:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            continue

        for i in range(len(matches)):
            link_text, link_url  = matches[i][0], matches[i][1]
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            if not sections:
                break
            
            if sections[0]:
                if not extract_markdown_links(sections[0]):
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            if sections[1]:
                if not extract_markdown_links(sections[1]):
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))

            original_text = sections[1]

    return new_nodes



