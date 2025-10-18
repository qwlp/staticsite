import os
import shutil
import sys
from copy_helper import copy_to_public
from template_gen import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"
basepath = sys.argv[1]


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_to_public()
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


main()
