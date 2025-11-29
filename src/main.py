from utils import copy_files

def main():
    copy_files("static/", "public/", src_root="static/", dst_root="public/")

main()