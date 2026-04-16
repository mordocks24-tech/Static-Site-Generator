from textnode import TextNode, TextType
from copystatic import copy_to
import shutil, os
from generate_page import generate_pages_recursive
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    

    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
    copy_to("static/",  "docs/")

    generate_pages_recursive(basepath, "content/", "template.html", "docs")






main()