from utils import copy_files
from generate_pages import generate_pages_recursive
from pathlib import Path
import os, shutil

def main():

    copy_files("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")

main()