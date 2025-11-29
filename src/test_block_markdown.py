from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

from generate_pages import extract_title
import unittest


class TestBlockMarkdown(unittest.TestCase):
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

        def test_extract_title(self):
            md = "### Starts with h3\n\n# This is a heading"
            self.assertEqual(
                extract_title(md),
                "This is a heading"
            )
