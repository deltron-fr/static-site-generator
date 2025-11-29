from markdown_to_html import markdown_to_html_node
import os

def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}\n")

    with open(from_path, "r") as f:
        contents_md = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    title = extract_title(contents_md)
    node = markdown_to_html_node(contents_md)
    html_node = node.to_html()
    
    edited_template_content = template_content.replace("{{ Title }}", title)
    edited_html_content = edited_template_content.replace("{{ Content }}", html_node)

    with open(dest_path, "w") as f:
        f.write(edited_html_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, content_base="content/", dst_root="public/"):
    files = os.listdir(dir_path_content)

    if not files:
        return
    
    for file_name in files:
        file_path = os.path.join(dir_path_content, file_name)
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(file_path)
            if extension == ".md":
                dst_file = os.path.relpath(file_path, content_base)
                dst_file_name = dst_file.replace(".md", ".html")

                dst_file_path = os.path.join(dst_root, dst_file_name)

                os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
                generate_page(file_path, template_path, dst_file_path)
            else:
                print(f"skipping {file_name}...")

        else:
            source = file_path

            destination = os.path.join(dest_dir_path, file_name)
            if not os.path.exists(destination):
                os.mkdir(destination)
            
            generate_pages_recursive(source, template_path, destination)
            

        