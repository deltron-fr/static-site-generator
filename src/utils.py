import os, shutil

def copy_files(src, dest, deleted=False, src_root="static/", dst_root="public/"):
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
    
    for file in files:
        file_path = os.path.join(src, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)

        else:
            source = file_path
            dst_path = os.path.relpath(file_path, src_root)

            destination = os.path.join(dst_root, dst_path)
            if not os.path.exists(destination):
                os.mkdir(destination)
            copy_files(source, destination, deleted=True)

