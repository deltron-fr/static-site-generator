from block_markdown import block_to_block_type, markdown_to_blocks, BlockType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

import re

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    all_nodes = []

    for block in md_blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            node = html_code_block(block)
            if node:
                all_nodes.append(node)

        else:
            nodes = text_to_children(block, block_type)
            if nodes:
                all_nodes.extend(nodes)

    full_md_node = ParentNode("div", all_nodes)
    return full_md_node

def text_to_children(text, block_type):
    leafnodes = []

    if block_type == BlockType.PARAGRAPH:
        stripped_text = text.lstrip("\n").rstrip()
        new_text = " ".join(stripped_text.split())
        text_nodes = text_to_textnodes(new_text)
        child_nodes = []

        for text_node in text_nodes:
            child_nodes.append(text_node_to_html_node(text_node))

        leafnodes.append(ParentNode("p", child_nodes))

        return leafnodes
    
    elif block_type == BlockType.HEADING:
        new_text, h_no = get_header(text)
        text_nodes = text_to_textnodes(new_text)
        child_nodes = []

        for text_node in text_nodes:
            child_nodes.append(text_node_to_html_node(text_node))

        leafnodes.append(ParentNode(f"h{h_no}", child_nodes))

        return leafnodes
    
    elif block_type == BlockType.QUOTE:
        quote = get_quote(text)
        text_nodes = text_to_textnodes(quote)

        child_nodes = []

        for text_node in text_nodes:
            child_nodes.append(text_node_to_html_node(text_node))

        leafnodes.append(ParentNode("blockquote", [ParentNode("p", child_nodes)]))
        return leafnodes

    elif block_type == BlockType.UNORDERED_LIST:
        list_nodes = parse_unordered_list(text)
        
        leafnodes.append(ParentNode("ul", list_nodes))
        return leafnodes
    
    elif block_type == BlockType.ORDERED_LIST:
        list_nodes = parse_ordered_list(text)
        leafnodes.append(ParentNode("ol", list_nodes))
        return leafnodes

def html_code_block(text):
    new_text = text.strip()[3:-3]
    html_node = text_node_to_html_node(TextNode(new_text, TextType.TEXT))
    code_node = ParentNode("code", [html_node])
    parent_node_pre = ParentNode("pre", [code_node])
    return parent_node_pre

def get_header(text):
    match = re.search(r"#{1,6}\s", text).span()

    actual_text = text[match[1]:]
    heading_no = match[1] - 1

    return actual_text, heading_no
        
def get_quote(text):
    stripped_text = text.lstrip("\n").rstrip()
    quotes = stripped_text.split("\n")

    parsed_quotes = []

    for q in quotes:
        q = q[1:].strip()
        parsed_quotes.append(q)
    new_text = " ".join(parsed_quotes)
    return new_text

def parse_unordered_list(text):
    items = text.split("\n")
    list_leafnodes = []

    for item in items:
        if item.startswith("- "):
            item = item[2:].strip()
        nodes = text_to_textnodes(item)

        child_nodes = [text_node_to_html_node(n) for n in nodes]
        list_leafnodes.append(ParentNode("li", child_nodes))

    return list_leafnodes

def parse_ordered_list(text):
    items = text.split("\n")

    list_leafnodes = []

    for item in items:
        match = re.search(r"^\d+\. ", item).span()
        item = item[match[1]:].rstrip()
        nodes = text_to_textnodes(item)

        child_nodes = [text_node_to_html_node(n) for n in nodes]
        list_leafnodes.append(ParentNode("li", child_nodes))

    return list_leafnodes


