from block_markdown import block_to_block_type, markdown_to_blocks, BlockType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

import re


def markdown_to_html_node(markdown):
    """
    Convert full markdown text into a ParentNode tree representing HTML.
    """
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
    """
    Map a markdown block string to a list of HTML child nodes based on its block type.
    """
    leafnodes = []

    if block_type == BlockType.PARAGRAPH:
        stripped_text = text.lstrip("\n").rstrip()
        new_text = " ".join(stripped_text.split())

        text_nodes = text_to_textnodes(new_text)

        child_nodes = [text_node_to_html_node(n) for n in text_nodes]
        leafnodes.append(ParentNode("p", child_nodes))

        return leafnodes
    
    elif block_type == BlockType.HEADING:
        new_text, h_no = html_header(text)
        text_nodes = text_to_textnodes(new_text)

        child_nodes = [text_node_to_html_node(n) for n in text_nodes]
        leafnodes.append(ParentNode(f"h{h_no}", child_nodes))

        return leafnodes
    
    elif block_type == BlockType.QUOTE:
        quote = html_quote(text)
        text_nodes = text_to_textnodes(quote)

        child_nodes = [text_node_to_html_node(n) for n in text_nodes]

        leafnodes.append(ParentNode("blockquote", [ParentNode("p", child_nodes)]))
        return leafnodes

    elif block_type == BlockType.UNORDERED_LIST:
        list_nodes = html_unordered_list(text)
        
        leafnodes.append(ParentNode("ul", list_nodes))
        return leafnodes
    
    elif block_type == BlockType.ORDERED_LIST:
        list_nodes = html_ordered_list(text)

        leafnodes.append(ParentNode("ol", list_nodes))
        return leafnodes


def html_code_block(text):
    """
    Convert a code block markdown into a <pre><code> ParentNode.
    """
    new_text = text.strip()[3:-3]

    html_node = text_node_to_html_node(TextNode(new_text, TextType.TEXT))
    code_node = ParentNode("code", [html_node])
    parent_node_pre = ParentNode("pre", [code_node])

    return parent_node_pre


def html_header(text):
    """
    Extract header text and number from a markdown heading line.
    """
    match = re.search(r"#{1,6}\s", text).span()

    actual_text, heading_no = text[match[1]:], match[1] - 1

    return actual_text, heading_no
        

def html_quote(text):
    """
    Turn markdown blockquote lines into a single string.
    """
    stripped_text = text.lstrip("\n").rstrip()
    quotes = stripped_text.split("\n")

    parsed_quotes = [q[1:].strip() for q in quotes]

    new_text = " ".join(parsed_quotes)
    return new_text


def html_unordered_list(text):
    """
    Convert markdown unordered list into a list of <li> ParentNodes.
    """
    items = text.split("\n")
    list_leafnodes = []

    for item in items:
        if item.startswith("- "):
            item = item[2:].strip()
        nodes = text_to_textnodes(item)

        child_nodes = [text_node_to_html_node(n) for n in nodes]
        list_leafnodes.append(ParentNode("li", child_nodes))

    return list_leafnodes


def html_ordered_list(text):
    """
    Convert markdown ordered list into a list of <li> ParentNodes.
    """
    items = text.split("\n")

    list_leafnodes = []

    for item in items:
        match = re.search(r"^\d+\. ", item).span()
        item = item[match[1]:].rstrip()
        nodes = text_to_textnodes(item)

        child_nodes = [text_node_to_html_node(n) for n in nodes]
        list_leafnodes.append(ParentNode("li", child_nodes))

    return list_leafnodes


