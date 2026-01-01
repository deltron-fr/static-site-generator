from enum import Enum
import re


class BlockType(Enum):
    """
    High-level markdown block categories used by the parser.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list" 
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Split a markdown document into high-level blocks separated by blank lines.
    """
    lines = markdown.split("\n\n")
    new_blocks = []

    for block in lines:
        if block == "":
            continue
        new_blocks.append(block.strip())

    return new_blocks


def block_to_block_type(block):
    """
    Determine the BlockType of a given markdown block string.
    """
    blocks = block.split("\n")
    
    quote = False
    unordered_list = False

    ordered_list_count = 1
    ordered_list = False


    if re.search(r"#{1,6}\s", block):
        return BlockType.HEADING
    
    if block[:3] == "```" and block[::-1][:3] == "```":
        return BlockType.CODE
    
    for inner_line in blocks:
        if not inner_line:
            quote = False
            break

        if inner_line[0] != ">":
            quote = False
            break
        quote = True

    if quote:
        return BlockType.QUOTE
    
    for inner_line in blocks:
        if not inner_line:
            unordered_list = False
            break

        if not inner_line.startswith("- "):
            unordered_list = False
            break
        unordered_list = True

    if unordered_list:
        return BlockType.UNORDERED_LIST

    for i in range(len(blocks)):
        match = re.search(r"^\d+\. ", blocks[i])
        if not blocks[0].startswith("1."):
            ordered_list = False
            break
        
        if not match:
            ordered_list = False
            break

        pos = match.span()
        start, stop = pos[0], pos[1] - 2

        if int(blocks[i][start:stop]) != ordered_list_count:
            ordered_list = False
            break

        ordered_list_count += 1
        ordered_list = True

    if ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH