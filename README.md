## static-site-generator

A lightweight Python static site generator that converts Markdown files from `content/` into HTML pages in `docs/` (or `public/`) using a simple HTML `template.html`. It supports common block-level markdown and a basic set of inline formatting options.

### Motivation
---
This was a guided project on [Boot.dev](https://boot.dev). This project aims to be easy to read and easy to modify for personal use.

### Goal
----
Keep the generator minimal and predictable:

- Parse top-level markdown blocks and convert them to HTML nodes
- Support headings, paragraphs, blockquotes, fenced code blocks, ordered and unordered lists
- Support inline bold, italic, inline code, links and images (non-nested)

### Quick start
-----------

1. Put Markdown files under `content/` (each file should include an H1 title `# Title`).
2. Edit `template.html` and add `{{ Title }}` and `{{ Content }}` placeholders.
3. Run the generator (from the project root):

```bash
# to run locally
chmod u+x main.sh

./main.sh
```

```bash
# to setup for github pages
chmod u+x build.sh

./build.sh
```

By default the generator copies `static/` contents to `docs/` and converts markdown into `docs/` (or `public/`) HTML files using `template.html`.

### Examples
--------
See the `content/` and `docs/` folders in this repository for sample input and output HTML.


### Limitations and important notes
-------------------------------

- The project expects well-written Markdown files. It does not try to correct malformed Markdown (for example, unmatched inline delimiters like `**` or `_`).
- Nested inline markdown is not supported.
- I still plan to refactor some parts of the code for readability.

### Transient dependencies
----------------------

No external runtime dependencies; pure Python and small helper modules inside `src/`.

