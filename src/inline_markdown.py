from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)

        else:
            text_nodes.append(old_node)

    for text_node in text_nodes:
        text_split = text_node.text.split(delimiter)
        
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




