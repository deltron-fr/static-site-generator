from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

import unittest


class TestBlockMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


        def test_blocktype_heading(self):
            md = "### This is a heading"
            self.assertEqual(
                block_to_block_type(md),
                BlockType.HEADING
            )

        def test_blocktype_code(self):
            md = "```print('Hello World')```"
            self.assertEqual(
                block_to_block_type(md),
                BlockType.CODE
            )

        def test_blocktype_quote(self):
            md = ">manners maketh man\n> Martin Zubimendi"
            self.assertEqual(
                  block_to_block_type(md),
                  BlockType.QUOTE
             )

        def test_blocktype_unordered(self):
            md = "- This is a list\n- with items"
            self.assertEqual(
                block_to_block_type(md),
                BlockType.UNORDERED_LIST
            )

        def test_blocktype_ordered(self):
            md  = "1. one\n2. two\n3. three"
            self.assertEqual(
                block_to_block_type(md),
                BlockType.ORDERED_LIST
            )

        def test_blocktype_paragraph(self):
            md  = "1. one\n2. two\n6. three"
            self.assertEqual(
                block_to_block_type(md),
                BlockType.PARAGRAPH
            )
