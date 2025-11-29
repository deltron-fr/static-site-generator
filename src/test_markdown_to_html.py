import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
    - First item
    - Second item with **bold**
    - Third item with _italic_ and `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i> and <code>code</code></li></ul></div>"
        )


    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item with **bold**
    3. Third item with _italic_ and `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i> and <code>code</code></li></ol></div>"
        )


    def test_quote_block(self):
        md = """
    > This is a quote line
    > that continues on the next line
    > with **bold** text and `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a quote line that continues on the next line with <b>bold</b> text and <code>code</code></p></blockquote></div>"
        )


    def test_heading_h1(self):
        md = """
    # This is an H1 heading with _italic_ and **bold**
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an H1 heading with <i>italic</i> and <b>bold</b></h1></div>"
        )


    def test_heading_h3(self):
        md = """
    ### This is an H3 heading with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is an H3 heading with <code>code</code></h3></div>"
        )
