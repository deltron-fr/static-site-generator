from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list" 
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    converts markdown document to block markdown
    """
    lines = markdown.split("\n")
    new_markdown = ""
    for i in range(len(lines)):
        if i == 0:
            continue
        new_markdown += f"{lines[i].strip()}\n"

    new_blocks = []


    blocks = new_markdown.split("\n\n")
    for block in blocks:
        if block.strip() == "":
            continue

        new_blocks.append(block)

    return new_blocks

def block_to_block_type(block):
    """
    Takes a block of markdown and returns the type of block it is
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
