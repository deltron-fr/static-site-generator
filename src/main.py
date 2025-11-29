from markdown_to_html import markdown_to_html_node
import os, sys, shutil

def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 title found in markdown")

def copy_files(src, dest, deleted=False):
    """
    Recursively copies files and subdirectories from 
    """
    if not os.path.exists(src):
        raise FileNotFoundError
    
    if not deleted:
        for item in os.listdir(dest):
            item_path = os.path.join(dest, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
    files = os.listdir(src)
    if not files:
        return
    
    for file_name in files:
        file_path = os.path.join(src, file_name)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)

        else:
            source = file_path
            destination = os.path.join(dest, file_name)
            if not os.path.exists(destination):
                os.mkdir(destination)
            copy_files(source, destination, deleted=True)

def generate_page(
        from_path, 
        template_path, 
        dest_path, 
        basepath="/"
        ):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}\n")

    with open(from_path, "r") as f:
        contents_md = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    title = extract_title(contents_md)
    html_node = markdown_to_html_node(contents_md).to_html()
    
    edited_template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_node)
    edited_html_content = edited_template_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(edited_html_content)


def generate_pages_recursive(
        dir_path_content,
        template_path, 
        dest_dir_path, 
        content_base="content/", 
        dst_root="public/", 
        basepath="/"
        ):
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
                generate_page(file_path, template_path, dst_file_path, basepath=basepath)
            else:
                print(f"skipping {file_name}...")

        else:
            source = file_path

            destination = os.path.join(dest_dir_path, file_name)
            if not os.path.exists(destination):
                os.mkdir(destination)
            
            generate_pages_recursive(source, template_path, destination, dst_root=dst_root, basepath=basepath)


def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    public = "docs/"
    source = "content/"

    if not os.path.isdir(public):
        os.makedirs(os.path.dirname(public), exist_ok=True)
    
    copy_files("static/", public)
    generate_pages_recursive(source, "template.html", public, dst_root=public, basepath=basepath)

if __name__ == "__main__":
    main()